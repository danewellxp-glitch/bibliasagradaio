import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/constants/bible_books.dart';
import '../../../core/theme/app_colors.dart';
import '../providers/bible_provider.dart';

class BookSelectorScreen extends ConsumerStatefulWidget {
  const BookSelectorScreen({super.key});

  @override
  ConsumerState<BookSelectorScreen> createState() =>
      _BookSelectorScreenState();
}

class _BookSelectorScreenState extends ConsumerState<BookSelectorScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Selecionar Livro'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Antigo Testamento'),
            Tab(text: 'Novo Testamento'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildBookGrid(oldTestamentBooks),
          _buildBookGrid(newTestamentBooks),
        ],
      ),
    );
  }

  Widget _buildBookGrid(List<BibleBook> books) {
    return GridView.builder(
      padding: const EdgeInsets.all(12),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 4,
        childAspectRatio: 1.5,
        crossAxisSpacing: 8,
        mainAxisSpacing: 8,
      ),
      itemCount: books.length,
      itemBuilder: (context, index) {
        final book = books[index];
        final isSelected = ref.watch(selectedBookProvider) == book.number;
        return InkWell(
          onTap: () => _showChapterSelector(book),
          borderRadius: BorderRadius.circular(8),
          child: Container(
            decoration: BoxDecoration(
              color: isSelected
                  ? AppColors.primary.withOpacity(0.15)
                  : Colors.grey.withOpacity(0.08),
              borderRadius: BorderRadius.circular(8),
              border: isSelected
                  ? Border.all(color: AppColors.primary, width: 2)
                  : null,
            ),
            alignment: Alignment.center,
            child: Text(
              book.abbreviation,
              style: TextStyle(
                fontSize: 14,
                fontWeight:
                    isSelected ? FontWeight.bold : FontWeight.normal,
                color: isSelected ? AppColors.primary : null,
              ),
              textAlign: TextAlign.center,
            ),
          ),
        );
      },
    );
  }

  void _showChapterSelector(BibleBook book) {
    showModalBottomSheet(
      context: context,
      builder: (context) => _ChapterSelectorSheet(book: book),
    );
  }
}

class _ChapterSelectorSheet extends ConsumerWidget {
  final BibleBook book;

  const _ChapterSelectorSheet({required this.book});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            book.name,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),
          Flexible(
            child: GridView.builder(
              shrinkWrap: true,
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 7,
                childAspectRatio: 1,
                crossAxisSpacing: 6,
                mainAxisSpacing: 6,
              ),
              itemCount: book.chapters,
              itemBuilder: (context, index) {
                final chapter = index + 1;
                return InkWell(
                  onTap: () {
                    ref.read(selectedBookProvider.notifier).state =
                        book.number;
                    ref.read(selectedChapterProvider.notifier).state =
                        chapter;
                    Navigator.of(context).pop(); // close sheet
                    Navigator.of(context).pop(); // close selector
                  },
                  borderRadius: BorderRadius.circular(6),
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.grey.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    alignment: Alignment.center,
                    child: Text(
                      '$chapter',
                      style: const TextStyle(fontSize: 14),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
