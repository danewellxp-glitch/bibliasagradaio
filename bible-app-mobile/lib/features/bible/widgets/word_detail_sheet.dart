import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/constants/bible_books.dart';
import '../../study/providers/study_provider.dart';
import '../providers/bible_provider.dart';

class WordDetailSheet extends ConsumerStatefulWidget {
  final String word;

  const WordDetailSheet({super.key, required this.word});

  static void show(BuildContext context, String word) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      builder: (_) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        minChildSize: 0.4,
        maxChildSize: 0.95,
        expand: false,
        builder: (_, controller) => _WordDetailSheetContent(
          word: word,
          scrollController: controller,
        ),
      ),
    );
  }

  @override
  ConsumerState<WordDetailSheet> createState() => _WordDetailSheetState();
}

class _WordDetailSheetState extends ConsumerState<WordDetailSheet> {
  @override
  Widget build(BuildContext context) {
    return const SizedBox.shrink();
  }
}

class _WordDetailSheetContent extends ConsumerWidget {
  final String word;
  final ScrollController scrollController;

  const _WordDetailSheetContent({
    required this.word,
    required this.scrollController,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final searchAsync = ref.watch(lexiconSearchProvider(word));

    return Column(
      children: [
        // Handle bar
        Container(
          margin: const EdgeInsets.only(top: 8),
          width: 40,
          height: 4,
          decoration: BoxDecoration(
            color: Colors.grey[300],
            borderRadius: BorderRadius.circular(2),
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(16),
          child: Text(
            'Lexico: "$word"',
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ),
        Expanded(
          child: searchAsync.when(
            data: (entries) {
              if (entries.isEmpty) {
                return Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.search_off, size: 48, color: Colors.grey),
                        const SizedBox(height: 12),
                        Text(
                          'Nenhuma entrada encontrada para "$word".',
                          textAlign: TextAlign.center,
                          style: const TextStyle(color: Colors.grey),
                        ),
                      ],
                    ),
                  ),
                );
              }
              return ListView.builder(
                controller: scrollController,
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: entries.length,
                itemBuilder: (context, index) {
                  final entry = entries[index];
                  return _LexiconEntryCard(
                    entry: entry,
                    onTap: () => _showEntryDetail(context, ref, entry.strongNumber),
                  );
                },
              );
            },
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (e, _) => Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline, size: 48, color: Colors.grey),
                  const SizedBox(height: 12),
                  const Text('Erro ao buscar no lexico.'),
                  const SizedBox(height: 16),
                  FilledButton.icon(
                    onPressed: () => ref.invalidate(lexiconSearchProvider(word)),
                    icon: const Icon(Icons.refresh),
                    label: const Text('Tentar novamente'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }

  void _showEntryDetail(BuildContext context, WidgetRef ref, String strongNumber) {
    Navigator.of(context).pop();
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      builder: (_) => DraggableScrollableSheet(
        initialChildSize: 0.75,
        minChildSize: 0.4,
        maxChildSize: 0.95,
        expand: false,
        builder: (_, controller) => _LexiconDetailView(
          strongNumber: strongNumber,
          scrollController: controller,
        ),
      ),
    );
  }
}

class _LexiconEntryCard extends StatelessWidget {
  final LexiconEntry entry;
  final VoidCallback onTap;

  const _LexiconEntryCard({required this.entry, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        onTap: onTap,
        title: Row(
          children: [
            if (entry.originalWord != null) ...[
              Text(
                entry.originalWord!,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(width: 8),
            ],
            Text(
              entry.strongNumber,
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey[600],
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (entry.transliteration != null)
              Text(
                entry.transliteration!,
                style: TextStyle(fontSize: 13, color: Colors.grey[700]),
              ),
            if (entry.basicMeaning != null)
              Text(
                entry.basicMeaning!,
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
              ),
          ],
        ),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: BoxDecoration(
                color: entry.language == 'hebrew'
                    ? Colors.amber[100]
                    : Colors.blue[100],
                borderRadius: BorderRadius.circular(4),
              ),
              child: Text(
                entry.language == 'hebrew' ? 'HEB' : 'GR',
                style: TextStyle(
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                  color: entry.language == 'hebrew'
                      ? Colors.amber[900]
                      : Colors.blue[900],
                ),
              ),
            ),
            const SizedBox(height: 2),
            const Icon(Icons.chevron_right, size: 20),
          ],
        ),
      ),
    );
  }
}

class _LexiconDetailView extends ConsumerWidget {
  final String strongNumber;
  final ScrollController scrollController;

  const _LexiconDetailView({
    required this.strongNumber,
    required this.scrollController,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final detailAsync = ref.watch(lexiconProvider(strongNumber));

    return Column(
      children: [
        Container(
          margin: const EdgeInsets.only(top: 8),
          width: 40,
          height: 4,
          decoration: BoxDecoration(
            color: Colors.grey[300],
            borderRadius: BorderRadius.circular(2),
          ),
        ),
        Expanded(
          child: detailAsync.when(
            data: (detail) {
              final entry = detail.entry;
              return ListView(
                controller: scrollController,
                padding: const EdgeInsets.all(16),
                children: [
                  // Header with original word
                  Center(
                    child: Column(
                      children: [
                        if (entry.originalWord != null)
                          Text(
                            entry.originalWord!,
                            style: const TextStyle(
                              fontSize: 32,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        Text(
                          entry.strongNumber,
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),
                  // Info cards
                  if (entry.transliteration != null)
                    _InfoRow(label: 'Transliteracao', value: entry.transliteration!),
                  if (entry.pronunciation != null)
                    _InfoRow(label: 'Pronuncia', value: entry.pronunciation!),
                  if (entry.basicMeaning != null)
                    _InfoRow(label: 'Significado', value: entry.basicMeaning!),
                  if (entry.extendedDefinition != null) ...[
                    const SizedBox(height: 8),
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(12),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Definicao',
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                                color: Colors.grey,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              entry.extendedDefinition!,
                              style: const TextStyle(fontSize: 14, height: 1.5),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                  if (entry.usageCount != null)
                    _InfoRow(
                      label: 'Ocorrencias',
                      value: '${entry.usageCount}x na Biblia',
                    ),
                  if (entry.language.isNotEmpty)
                    _InfoRow(
                      label: 'Idioma',
                      value: entry.language == 'hebrew'
                          ? 'Hebraico'
                          : entry.language == 'greek'
                              ? 'Grego'
                              : entry.language,
                    ),
                  // Occurrences
                  if (detail.occurrences.isNotEmpty) ...[
                    const SizedBox(height: 16),
                    const Text(
                      'Versiculos onde aparece',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    ...detail.occurrences.map((occ) {
                      final book = getBookByNumber(occ.bookNumber);
                      return ListTile(
                        dense: true,
                        leading: const Icon(Icons.navigate_next, size: 18),
                        title: Text('${book.name} ${occ.chapter}:${occ.verse}'),
                        subtitle: occ.wordInVerse != null
                            ? Text(
                                occ.wordInVerse!,
                                style: TextStyle(
                                  fontSize: 12,
                                  color: Colors.grey[600],
                                ),
                              )
                            : null,
                        onTap: () {
                          Navigator.of(context).pop();
                          ref.read(selectedBookProvider.notifier).state =
                              occ.bookNumber;
                          ref.read(selectedChapterProvider.notifier).state =
                              occ.chapter;
                        },
                      );
                    }),
                  ],
                ],
              );
            },
            loading: () => const Center(child: CircularProgressIndicator()),
            error: (e, _) => Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline, size: 48, color: Colors.grey),
                  const SizedBox(height: 12),
                  const Text('Erro ao carregar detalhes.'),
                  const SizedBox(height: 16),
                  FilledButton.icon(
                    onPressed: () =>
                        ref.invalidate(lexiconProvider(strongNumber)),
                    icon: const Icon(Icons.refresh),
                    label: const Text('Tentar novamente'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class _InfoRow extends StatelessWidget {
  final String label;
  final String value;

  const _InfoRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(
              label,
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w500,
                color: Colors.grey[600],
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(fontSize: 14),
            ),
          ),
        ],
      ),
    );
  }
}
