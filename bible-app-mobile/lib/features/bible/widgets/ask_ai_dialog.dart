import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../data/models/bible_models.dart';
import '../../auth/providers/auth_provider.dart';
import '../../study/providers/study_provider.dart';
import '../providers/bible_provider.dart';

class AskAIDialog extends ConsumerStatefulWidget {
  final Verse verse;

  const AskAIDialog({super.key, required this.verse});

  @override
  ConsumerState<AskAIDialog> createState() => _AskAIDialogState();
}

class _AskAIDialogState extends ConsumerState<AskAIDialog> {
  final _controller = TextEditingController();
  bool _loading = false;
  String? _answer;
  String? _error;
  int? _remaining;
  bool? _fromCache;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    final question = _controller.text.trim();
    if (question.isEmpty) return;

    setState(() {
      _loading = true;
      _error = null;
      _answer = null;
    });

    try {
      final api = ref.read(apiServiceProvider);
      final version = ref.read(selectedVersionProvider);
      final result = await askAboutVerse(
        api,
        version: version,
        book: widget.verse.bookNumber,
        chapter: widget.verse.chapter,
        verse: widget.verse.verse,
        question: question,
      );
      setState(() {
        _answer = result.answer;
        _fromCache = result.fromCache;
        _remaining = result.remainingQuestions;
        _loading = false;
      });
    } on DioException catch (e) {
      final statusCode = e.response?.statusCode;
      String msg;
      if (statusCode == 429) {
        msg = 'Limite diario de perguntas atingido. Tente novamente amanha.';
      } else if (statusCode == 503) {
        msg = 'Servico de IA indisponivel. Tente novamente mais tarde.';
      } else {
        msg = 'Erro ao processar sua pergunta. Tente novamente.';
      }
      setState(() {
        _error = msg;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _error = 'Erro inesperado. Tente novamente.';
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      insetPadding: const EdgeInsets.all(16),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 500, maxHeight: 600),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Header
              Row(
                children: [
                  const Icon(Icons.auto_awesome, color: Colors.deepPurple),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Perguntar sobre ${widget.verse.reference}',
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close, size: 20),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              // Question input
              TextField(
                controller: _controller,
                maxLines: 2,
                maxLength: 500,
                enabled: !_loading,
                decoration: const InputDecoration(
                  hintText: 'Ex: Qual o contexto historico deste versiculo?',
                  border: OutlineInputBorder(),
                  contentPadding:
                      EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                ),
                onSubmitted: (_) => _submit(),
              ),
              const SizedBox(height: 8),

              // Submit button
              FilledButton.icon(
                onPressed: _loading ? null : _submit,
                icon: _loading
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white,
                        ),
                      )
                    : const Icon(Icons.send),
                label: Text(_loading ? 'Consultando IA...' : 'Enviar'),
              ),

              // Error
              if (_error != null) ...[
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red[50],
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.error_outline, color: Colors.red[700], size: 20),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          _error!,
                          style: TextStyle(color: Colors.red[700], fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              ],

              // Answer
              if (_answer != null) ...[
                const SizedBox(height: 16),
                Flexible(
                  child: Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.deepPurple[50],
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              const Icon(Icons.auto_awesome,
                                  size: 16, color: Colors.deepPurple),
                              const SizedBox(width: 4),
                              const Text(
                                'Resposta',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  fontSize: 13,
                                  color: Colors.deepPurple,
                                ),
                              ),
                              const Spacer(),
                              if (_fromCache == true)
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 6, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: Colors.grey[200],
                                    borderRadius: BorderRadius.circular(4),
                                  ),
                                  child: const Text(
                                    'cache',
                                    style: TextStyle(
                                        fontSize: 10, color: Colors.grey),
                                  ),
                                ),
                            ],
                          ),
                          const SizedBox(height: 8),
                          Text(
                            _answer!,
                            style: const TextStyle(
                                fontSize: 14, height: 1.5),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],

              // Remaining questions
              if (_remaining != null) ...[
                const SizedBox(height: 8),
                Text(
                  '$_remaining perguntas restantes hoje',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
