import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/constants/bible_books.dart';
import '../../../core/theme/app_colors.dart';
import '../../../data/models/bible_models.dart';
import '../providers/bible_provider.dart';
import '../widgets/verse_card.dart';

class BibleSearchScreen extends ConsumerStatefulWidget {
  const BibleSearchScreen({super.key});

  @override
  ConsumerState<BibleSearchScreen> createState() => _BibleSearchScreenState();
}

class _BibleSearchScreenState extends ConsumerState<BibleSearchScreen> {
  final _searchController = TextEditingController();
  Timer? _debounce;

  @override
  void dispose() {
    _searchController.dispose();
    _debounce?.cancel();
    super.dispose();
  }

  void _onSearchChanged(String query) {
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 500), () {
      ref.read(searchQueryProvider.notifier).state = query.trim();
    });
  }

  @override
  Widget build(BuildContext context) {
    final resultsAsync = ref.watch(searchResultsProvider);
    final version = ref.watch(selectedVersionProvider);

    return Scaffold(
      appBar: AppBar(
        title: TextField(
          controller: _searchController,
          autofocus: true,
          onChanged: _onSearchChanged,
          style: const TextStyle(color: Colors.white),
          decoration: const InputDecoration(
            hintText: 'Buscar na Biblia...',
            hintStyle: TextStyle(color: Colors.white70),
            border: InputBorder.none,
          ),
        ),
        actions: [
          if (_searchController.text.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.clear),
              onPressed: () {
                _searchController.clear();
                ref.read(searchQueryProvider.notifier).state = '';
              },
            ),
        ],
      ),
      body: Column(
        children: [
          // Version chip
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            alignment: Alignment.centerLeft,
            child: Wrap(
              spacing: 8,
              children: [
                ChoiceChip(
                  label: Text(version),
                  selected: true,
                  selectedColor: AppColors.primary.withOpacity(0.2),
                  onSelected: (_) => _showVersionSelector(context, ref),
                ),
              ],
            ),
          ),
          // Results
          Expanded(
            child: resultsAsync.when(
              data: (results) {
                if (ref.read(searchQueryProvider).isEmpty) {
                  return const Center(
                    child: Text(
                      'Digite para buscar versiculos',
                      style: TextStyle(color: Colors.grey),
                    ),
                  );
                }
                if (results.isEmpty) {
                  return const Center(
                    child: Text(
                      'Nenhum resultado encontrado',
                      style: TextStyle(color: Colors.grey),
                    ),
                  );
                }
                return ListView.separated(
                  padding: const EdgeInsets.all(16),
                  itemCount: results.length,
                  separatorBuilder: (_, __) => const Divider(height: 1),
                  itemBuilder: (context, index) {
                    final verse = results[index];
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: const EdgeInsets.only(top: 8, bottom: 4),
                          child: Text(
                            verse.reference,
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                              color: AppColors.primary,
                            ),
                          ),
                        ),
                        VerseCard(
                          verse: verse,
                          onTap: () => _navigateToVerse(ref, verse),
                        ),
                      ],
                    );
                  },
                );
              },
              loading: () =>
                  const Center(child: CircularProgressIndicator()),
              error: (e, _) => Center(child: Text('Erro: $e')),
            ),
          ),
        ],
      ),
    );
  }

  void _navigateToVerse(WidgetRef ref, Verse verse) {
    ref.read(selectedBookProvider.notifier).state = verse.bookNumber;
    ref.read(selectedChapterProvider.notifier).state = verse.chapter;
    // Pop back to reader which will show the chapter
    Navigator.of(context).pop();
  }

  void _showVersionSelector(BuildContext context, WidgetRef ref) {
    showModalBottomSheet(
      context: context,
      builder: (_) => ListView(
        shrinkWrap: true,
        children: [
          for (final v in ['ARA', 'ARC', 'ACF', 'KJV'])
            ListTile(
              title: Text(v),
              trailing: ref.read(selectedVersionProvider) == v
                  ? const Icon(Icons.check, color: AppColors.primary)
                  : null,
              onTap: () {
                ref.read(selectedVersionProvider.notifier).state = v;
                Navigator.of(context).pop();
              },
            ),
        ],
      ),
    );
  }
}
