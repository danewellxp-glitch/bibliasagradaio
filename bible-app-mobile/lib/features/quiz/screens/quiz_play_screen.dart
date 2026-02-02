import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/services/api_service.dart';
import '../../auth/providers/auth_provider.dart';
import '../providers/quiz_provider.dart';
import '../widgets/question_card.dart';

class QuizPlayScreen extends ConsumerStatefulWidget {
  const QuizPlayScreen({super.key});

  @override
  ConsumerState<QuizPlayScreen> createState() => _QuizPlayScreenState();
}

class _QuizPlayScreenState extends ConsumerState<QuizPlayScreen> {
  QuizQuestionModel? _question;
  bool _loading = true;
  String? _error;
  bool _answered = false;
  bool? _correct;
  String? _correctAnswer;
  String? _explanation;
  int _xpEarned = 0;
  int _streak = 0;

  @override
  void initState() {
    super.initState();
    _loadQuestion();
  }

  Future<void> _loadQuestion() async {
    setState(() {
      _loading = true;
      _error = null;
      _question = null;
      _answered = false;
    });
    try {
      final api = ref.read(apiServiceProvider);
      final q = await fetchNextQuestion(api);
      if (!mounted) return;
      setState(() {
        _question = q;
        _loading = false;
        _error = q == null ? 'Nenhuma pergunta disponivel' : null;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _loading = false;
        _error = e.toString();
      });
    }
  }

  Future<void> _onAnswer(String answer) async {
    if (_question == null || _answered) return;
    setState(() => _answered = true);
    try {
      final api = ref.read(apiServiceProvider);
      final res = await submitAnswer(
        api,
        questionId: _question!.id,
        answer: answer,
      );
      if (!mounted) return;
      setState(() {
        _correct = res['is_correct'] as bool;
        _correctAnswer = res['correct_answer'] as String?;
        _explanation = res['explanation'] as String?;
        _xpEarned = res['xp_earned'] as int? ?? 0;
        _streak = res['streak'] as int? ?? 0;
      });
      ref.invalidate(quizStatsProvider);
    } catch (e) {
      if (!mounted) return;
      setState(() => _error = e.toString());
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading && _question == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Quiz')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }
    if (_error != null && _question == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Quiz')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Erro: $_error'),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () => context.pop(),
                child: const Text('Voltar'),
              ),
            ],
          ),
        ),
      );
    }
    if (_question == null) return const SizedBox.shrink();

    return Scaffold(
      appBar: AppBar(title: const Text('Quiz')),
      body: Column(
        children: [
          if (_answered) ...[
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              color: _correct! ? Colors.green.shade100 : Colors.red.shade100,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        _correct! ? Icons.check_circle : Icons.cancel,
                        color: _correct! ? Colors.green : Colors.red,
                        size: 32,
                      ),
                      const SizedBox(width: 12),
                      Text(
                        _correct! ? 'Correto!' : 'Incorreto',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                    ],
                  ),
                  if (_correctAnswer != null)
                    Padding(
                      padding: const EdgeInsets.only(top: 8),
                      child: Text('Resposta correta: $_correctAnswer'),
                    ),
                  if (_explanation != null)
                    Padding(
                      padding: const EdgeInsets.only(top: 8),
                      child: Text(_explanation!),
                    ),
                  if (_xpEarned > 0)
                    Padding(
                      padding: const EdgeInsets.only(top: 8),
                      child: Text('+$_xpEarned XP${_streak > 0 ? ' | Streak: $_streak dias' : ''}'),
                    ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      ElevatedButton(
                        onPressed: () => context.pop(),
                        child: const Text('Voltar'),
                      ),
                      const SizedBox(width: 12),
                      FilledButton(
                        onPressed: () => _loadQuestion(),
                        child: const Text('Proxima pergunta'),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ] else
            Expanded(
              child: SingleChildScrollView(
                child: QuestionCard(
                  question: _question!,
                  onAnswer: _onAnswer,
                ),
              ),
            ),
        ],
      ),
    );
  }
}
