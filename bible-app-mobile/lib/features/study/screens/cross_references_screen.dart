import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/constants/bible_books.dart';
import '../providers/study_provider.dart';

class CrossReferencesScreen extends ConsumerStatefulWidget {
  const CrossReferencesScreen({super.key});

  @override
  ConsumerState<CrossReferencesScreen> createState() =>
      _CrossReferencesScreenState();
}

class _CrossReferencesScreenState extends ConsumerState<CrossReferencesScreen> {
  int _book = 1;
  int _chapter = 1;
  int _verse = 1;

  @override
  Widget build(BuildContext context) {
    final params = (book: _book, chapter: _chapter, verse: _verse);
    final async = ref.watch(crossRefsProvider(params));

    return Scaffold(
      appBar: AppBar(title: const Text('Referencias cruzadas')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: DropdownButtonFormField<int>(
                    value: _book,
                    decoration: const InputDecoration(labelText: 'Livro'),
                    items: bibleBooks
                        .map((b) => DropdownMenuItem(value: b.number, child: Text(b.name)))
                        .toList(),
                    onChanged: (v) => setState(() => _book = v ?? 1),
                  ),
                ),
                const SizedBox(width: 8),
                SizedBox(
                  width: 70,
                  child: TextFormField(
                    initialValue: '$_chapter',
                    decoration: const InputDecoration(labelText: 'Cap'),
                    keyboardType: TextInputType.number,
                    onChanged: (v) =>
                        setState(() => _chapter = int.tryParse(v) ?? 1),
                  ),
                ),
                const SizedBox(width: 8),
                SizedBox(
                  width: 70,
                  child: TextFormField(
                    initialValue: '$_verse',
                    decoration: const InputDecoration(labelText: 'V'),
                    keyboardType: TextInputType.number,
                    onChanged: (v) =>
                        setState(() => _verse = int.tryParse(v) ?? 1),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: async.when(
              data: (list) {
                if (list.isEmpty) {
                  return const Center(
                    child: Text(
                        'Nenhuma referencia cruzada para este versiculo.'),
                  );
                }
                return ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  itemCount: list.length,
                  itemBuilder: (_, i) {
                    final r = list[i];
                    final toBook = getBookByNumber(r.toBook);
                    return ListTile(
                      title: Text('${toBook.name} ${r.toChapter}:${r.toVerse}'),
                      subtitle: r.relationshipType != null
                          ? Text(r.relationshipType!)
                          : null,
                      trailing: const Icon(Icons.open_in_new),
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
                    ElevatedButton(
                      onPressed: () =>
                          ref.invalidate(crossRefsProvider(params)),
                      child: const Text('Tentar novamente'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
