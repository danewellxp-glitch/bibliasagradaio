import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/study_provider.dart';

class CommentaryScreen extends ConsumerStatefulWidget {
  const CommentaryScreen({super.key});

  @override
  ConsumerState<CommentaryScreen> createState() => _CommentaryScreenState();
}

class _CommentaryScreenState extends ConsumerState<CommentaryScreen> {
  int _book = 1;
  int? _chapter;
  int? _verse;

  @override
  Widget build(BuildContext context) {
    final params = (book: _book, chapter: _chapter, verse: _verse);
    final async = ref.watch(commentariesProvider(params));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Comentarios'),
        actions: [
          IconButton(
            icon: const Icon(Icons.tune),
            onPressed: () => _showFilters(context),
          ),
        ],
      ),
      body: async.when(
        data: (list) {
          if (list.isEmpty) {
            return const Center(
              child: Text('Nenhum comentario encontrado para esta referencia.'),
            );
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: list.length,
            itemBuilder: (_, i) {
              final c = list[i];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Text(
                            c.author,
                            style: Theme.of(context).textTheme.titleSmall,
                          ),
                          if (c.source != null) ...[
                            const SizedBox(width: 8),
                            Text(
                              '(${c.source})',
                              style: Theme.of(context).textTheme.bodySmall,
                            ),
                          ],
                        ],
                      ),
                      if (c.chapter != null || c.verseStart != null)
                        Padding(
                          padding: const EdgeInsets.only(top: 4),
                          child: Text(
                            'Cap. ${c.chapter ?? "?"}'
                                '${c.verseStart != null ? ", v. ${c.verseStart}${c.verseEnd != null && c.verseEnd != c.verseStart ? "-${c.verseEnd}" : ""}" : ""}',
                            style: Theme.of(context).textTheme.bodySmall,
                          ),
                        ),
                      const SizedBox(height: 8),
                      Text(c.commentary),
                    ],
                  ),
                ),
              );
            },
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Erro: $e'),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () => ref.invalidate(commentariesProvider(params)),
                child: const Text('Tentar novamente'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showFilters(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Filtrar'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                decoration: const InputDecoration(labelText: 'Livro (numero 1-66)'),
                keyboardType: TextInputType.number,
                onChanged: (v) => setState(() => _book = int.tryParse(v) ?? 1),
              ),
              TextField(
                decoration: const InputDecoration(labelText: 'Capitulo (opcional)'),
                keyboardType: TextInputType.number,
                onChanged: (v) =>
                    setState(() => _chapter = int.tryParse(v)),
              ),
              TextField(
                decoration: const InputDecoration(labelText: 'Versiculo (opcional)'),
                keyboardType: TextInputType.number,
                onChanged: (v) =>
                    setState(() => _verse = int.tryParse(v)),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Fechar'),
          ),
          FilledButton(
            onPressed: () {
              ref.invalidate(commentariesProvider((book: _book, chapter: _chapter, verse: _verse)));
              Navigator.pop(ctx);
            },
            child: const Text('Aplicar'),
          ),
        ],
      ),
    );
  }
}
