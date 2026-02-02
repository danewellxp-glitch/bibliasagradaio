import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/constants/bible_books.dart';
import '../../../core/services/offline_service.dart';
import '../../../core/theme/app_colors.dart';
import '../../../data/models/bible_models.dart';
import '../providers/bible_provider.dart';
import '../providers/user_content_provider.dart';
import '../widgets/annotation_dialog.dart';
import '../widgets/highlight_menu.dart';
import '../widgets/share_verse_sheet.dart';
import '../widgets/verse_card.dart';
import 'bible_search_screen.dart';
import 'book_selector_screen.dart';

class BibleReaderScreen extends ConsumerWidget {
  const BibleReaderScreen({super.key});

  static const _highlightColors = {
    'yellow': AppColors.highlightYellow,
    'green': AppColors.highlightGreen,
    'blue': AppColors.highlightBlue,
    'red': AppColors.highlightRed,
    'purple': AppColors.highlightPurple,
  };

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final versesAsync = ref.watch(chapterVersesProvider);
    final highlightsAsync = ref.watch(highlightsProvider);
    final bookNumber = ref.watch(selectedBookProvider);
    final chapter = ref.watch(selectedChapterProvider);
    final bookInfo = getBookByNumber(bookNumber);

    return Scaffold(
      appBar: AppBar(
        title: GestureDetector(
          onTap: () => Navigator.of(context).push(
            MaterialPageRoute(
              builder: (_) => const BookSelectorScreen(),
            ),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('${bookInfo.name} $chapter'),
              const Icon(Icons.arrow_drop_down),
            ],
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () => Navigator.of(context).push(
              MaterialPageRoute(
                builder: (_) => const BibleSearchScreen(),
              ),
            ),
          ),
          PopupMenuButton<String>(
            icon: const Icon(Icons.more_vert),
            onSelected: (value) {
              if (value == 'download_offline') {
                _startDownloadVersion(context, ref);
              }
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'download_offline',
                child: ListTile(
                  leading: Icon(Icons.download),
                  title: Text('Baixar para uso offline'),
                ),
              ),
            ],
          ),
        ],
      ),
      body: versesAsync.when(
        data: (verses) {
          final highlights = highlightsAsync.valueOrNull ?? [];
          return Column(
            children: [
              Expanded(
                child: ListView.builder(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  itemCount: verses.length,
                  itemBuilder: (context, index) {
                    final verse = verses[index];
                    final highlightColor = getHighlightForVerse(
                      highlights,
                      1, // version_id - simplified
                      bookNumber,
                      chapter,
                      verse.verse,
                    );
                    return VerseCard(
                      verse: verse,
                      highlightColor: highlightColor != null
                          ? _highlightColors[highlightColor]
                          : null,
                      onTap: () => _showVerseMenu(context, ref, verse),
                    );
                  },
                ),
              ),
              _buildChapterNavigation(context, ref, bookInfo, chapter),
            ],
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.cloud_off, size: 48, color: Colors.grey),
              const SizedBox(height: 16),
              Text('Erro ao carregar: $e'),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () => ref.invalidate(chapterVersesProvider),
                child: const Text('Tentar novamente'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _startDownloadVersion(BuildContext context, WidgetRef ref) async {
    final version = ref.read(selectedVersionProvider);
    final repo = ref.read(offlineBibleRepositoryProvider);
    final isDownloaded = await repo.isVersionDownloaded(version);
    if (isDownloaded && context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('$version ja esta disponivel offline.')),
      );
      return;
    }
    final progress = ValueNotifier<(int, int)>((0, OfflineService.totalChapters));
    if (!context.mounted) return;
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => ValueListenableBuilder<(int, int)>(
        valueListenable: progress,
        builder: (_, value, __) {
          final (done, total) = value;
          return AlertDialog(
            title: const Text('Baixando Biblia'),
            content: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text('$done / $total capitulos'),
                const SizedBox(height: 12),
                LinearProgressIndicator(
                  value: total > 0 ? done / total : 0,
                ),
              ],
            ),
          );
        },
      ),
    );
    try {
      await repo.downloadVersion(version, onProgress: (d, t) {
        progress.value = (d, t);
      });
      progress.dispose();
      if (context.mounted) {
        Navigator.of(context).pop();
        ref.invalidate(downloadedVersionsProvider);
        ref.invalidate(chapterVersesProvider);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('$version baixado para uso offline!')),
        );
      }
    } catch (e) {
      progress.dispose();
      if (context.mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro ao baixar: $e')),
        );
      }
    }
  }

  void _showVerseMenu(BuildContext context, WidgetRef ref, Verse verse) {
    showModalBottomSheet(
      context: context,
      builder: (_) => HighlightMenu(
        verse: verse,
        onHighlight: (color) async {
          Navigator.of(context).pop();
          final repo = ref.read(userContentRepositoryProvider);
          await repo.createHighlight(Highlight(
            versionId: 1,
            bookNumber: verse.bookNumber,
            chapter: verse.chapter,
            verse: verse.verse,
            color: color,
          ));
          ref.invalidate(highlightsProvider);
        },
        onAnnotate: () async {
          Navigator.of(context).pop();
          final note = await showDialog<String>(
            context: context,
            builder: (_) => AnnotationDialog(verse: verse),
          );
          if (note != null) {
            final repo = ref.read(userContentRepositoryProvider);
            await repo.createAnnotation(Annotation(
              versionId: 1,
              bookNumber: verse.bookNumber,
              chapter: verse.chapter,
              verse: verse.verse,
              note: note,
            ));
            ref.invalidate(annotationsProvider);
          }
        },
        onBookmark: () async {
          Navigator.of(context).pop();
          final repo = ref.read(userContentRepositoryProvider);
          await repo.createBookmark(Bookmark(
            versionId: 1,
            bookNumber: verse.bookNumber,
            chapter: verse.chapter,
            verse: verse.verse,
          ));
          ref.invalidate(bookmarksProvider);
          if (context.mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Versiculo favoritado!')),
            );
          }
        },
        onShare: () {
          Navigator.of(context).pop();
          ShareVerseSheet.show(context, verse);
        },
      ),
    );
  }

  Widget _buildChapterNavigation(
    BuildContext context,
    WidgetRef ref,
    BibleBook bookInfo,
    int currentChapter,
  ) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: Theme.of(context).scaffoldBackgroundColor,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 4,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          TextButton.icon(
            onPressed: currentChapter > 1
                ? () {
                    ref.read(selectedChapterProvider.notifier).state =
                        currentChapter - 1;
                  }
                : bookInfo.number > 1
                    ? () {
                        final prev = getBookByNumber(bookInfo.number - 1);
                        ref.read(selectedBookProvider.notifier).state =
                            prev.number;
                        ref.read(selectedChapterProvider.notifier).state =
                            prev.chapters;
                      }
                    : null,
            icon: const Icon(Icons.chevron_left),
            label: const Text('Anterior'),
          ),
          Text(
            '${bookInfo.abbreviation} $currentChapter',
            style: const TextStyle(fontWeight: FontWeight.w500),
          ),
          TextButton.icon(
            onPressed: currentChapter < bookInfo.chapters
                ? () {
                    ref.read(selectedChapterProvider.notifier).state =
                        currentChapter + 1;
                  }
                : bookInfo.number < 66
                    ? () {
                        ref.read(selectedBookProvider.notifier).state =
                            bookInfo.number + 1;
                        ref.read(selectedChapterProvider.notifier).state = 1;
                      }
                    : null,
            icon: const Icon(Icons.chevron_right),
            label: const Text('Proximo'),
          ),
        ],
      ),
    );
  }
}
