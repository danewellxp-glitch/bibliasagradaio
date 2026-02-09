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
import '../widgets/verse_of_the_day_card.dart';
import '../widgets/verse_study_sheet.dart';
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

    final selectedVersion = ref.watch(selectedVersionProvider);
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
          GestureDetector(
            onTap: () => _showVersionSelector(context, ref),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 12),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    selectedVersion,
                    style: TextStyle(
                      fontSize: 14,
                      color: Theme.of(context).colorScheme.onPrimary.withOpacity(0.9),
                    ),
                  ),
                  const Icon(Icons.arrow_drop_down, size: 20),
                ],
              ),
            ),
          ),
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
              if (value == 'change_version') {
                _showVersionSelector(context, ref);
              } else if (value == 'download_offline') {
                _startDownloadVersion(context, ref);
              }
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'change_version',
                child: ListTile(
                  leading: Icon(Icons.menu_book),
                  title: Text('Alterar versão da Bíblia'),
                ),
              ),
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
              const VerseOfTheDayCard(),
              Expanded(
                child: ListView.builder(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  itemCount: verses.length,
                  itemBuilder: (context, index) {
                    final verse = verses[index];
                    final versionId = ref.watch(selectedVersionIdProvider);
                    final highlightColor = getHighlightForVerse(
                      highlights,
                      versionId,
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
        error: (e, _) => _buildLoadError(context, ref, e),
      ),
    );
  }

  Widget _buildLoadError(BuildContext context, WidgetRef ref, Object e) {
    final isTimeout = e.toString().toLowerCase().contains('timeout') ||
        e.toString().toLowerCase().contains('connection');
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.cloud_off, size: 56, color: Colors.grey),
            const SizedBox(height: 16),
            Text(
              isTimeout
                  ? 'Não foi possível conectar ao servidor. Verifique se o backend está rodando e se o app está usando o endereço correto da API.'
                  : 'Erro ao carregar o capítulo.',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            if (!isTimeout) ...[
              const SizedBox(height: 8),
              Text(
                '$e',
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Colors.grey,
                    ),
              ),
            ],
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: () => ref.invalidate(chapterVersesProvider),
              icon: const Icon(Icons.refresh),
              label: const Text('Tentar novamente'),
            ),
            const SizedBox(height: 12),
            TextButton.icon(
              onPressed: () => _startDownloadVersion(context, ref),
              icon: const Icon(Icons.download),
              label: const Text('Baixar Bíblia para uso offline'),
            ),
          ],
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
    final versionId = ref.read(selectedVersionIdProvider);
    showModalBottomSheet(
      context: context,
      builder: (_) => HighlightMenu(
        verse: verse,
        onHighlight: (color) async {
          Navigator.of(context).pop();
          try {
            final repo = ref.read(userContentRepositoryProvider);
            await repo.createHighlight(Highlight(
              versionId: versionId,
              bookNumber: verse.bookNumber,
              chapter: verse.chapter,
              verse: verse.verse,
              color: color,
            ));
            ref.invalidate(highlightsProvider);
            if (context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Versículo grifado.')),
              );
            }
          } catch (e) {
            if (context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Não foi possível grifar. Tente novamente.')),
              );
            }
          }
        },
        onAnnotate: () async {
          Navigator.of(context).pop();
          final note = await showDialog<String>(
            context: context,
            builder: (_) => AnnotationDialog(verse: verse),
          );
          if (note != null) {
            try {
              final repo = ref.read(userContentRepositoryProvider);
              await repo.createAnnotation(Annotation(
                versionId: versionId,
                bookNumber: verse.bookNumber,
                chapter: verse.chapter,
                verse: verse.verse,
                note: note,
              ));
              ref.invalidate(annotationsProvider);
              if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Anotação salva.')),
                );
              }
            } catch (e) {
              if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Não foi possível salvar a anotação. Tente novamente.')),
                );
              }
            }
          }
        },
        onBookmark: () async {
          Navigator.of(context).pop();
          try {
            final repo = ref.read(userContentRepositoryProvider);
            await repo.createBookmark(Bookmark(
              versionId: versionId,
              bookNumber: verse.bookNumber,
              chapter: verse.chapter,
              verse: verse.verse,
            ));
            ref.invalidate(bookmarksProvider);
            if (context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Versículo favoritado!')),
              );
            }
          } catch (e) {
            if (context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Não foi possível favoritar. Tente novamente.')),
              );
            }
          }
        },
        onShare: () {
          Navigator.of(context).pop();
          ShareVerseSheet.show(context, verse);
        },
        onStudy: () {
          Navigator.of(context).pop();
          VerseStudySheet.show(context, verse);
        },
      ),
    );
  }

  void _showVersionSelector(BuildContext context, WidgetRef ref) {
    final versionsAsync = ref.read(versionsProvider);
    final currentVersion = ref.read(selectedVersionProvider);
    showModalBottomSheet(
      context: context,
      builder: (_) => versionsAsync.when(
        data: (versions) {
          final list = versions.isNotEmpty
              ? versions
              : <BibleVersion>[
                  const BibleVersion(id: 1, code: 'NVI', name: 'Nova Versão Internacional', language: 'pt-BR', isPremium: false),
                  const BibleVersion(id: 2, code: 'ARC', name: 'Almeida Corrigida e Revisada', language: 'pt-BR', isPremium: false),
                  const BibleVersion(id: 3, code: 'ACF', name: 'Almeida Corrigida Fiel', language: 'pt-BR', isPremium: false),
                  const BibleVersion(id: 4, code: 'KJV', name: 'King James Version', language: 'en', isPremium: false),
                ];
          return SafeArea(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Padding(
                  padding: EdgeInsets.all(16),
                  child: Text(
                    'Versão da Bíblia',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
                ...list.map((v) => ListTile(
                  title: Text(v.name),
                  subtitle: Text(v.code),
                  trailing: currentVersion == v.code
                      ? const Icon(Icons.check, color: AppColors.primary)
                      : null,
                  onTap: () {
                    ref.read(selectedVersionProvider.notifier).state = v.code;
                    ref.invalidate(chapterVersesProvider);
                    Navigator.of(context).pop();
                  },
                )),
              ],
            ),
          );
        },
        loading: () => const Padding(
          padding: EdgeInsets.all(24),
          child: Center(child: CircularProgressIndicator()),
        ),
        error: (_, __) => SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Padding(padding: EdgeInsets.all(16), child: Text('Versão da Bíblia', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold))),
              for (final code in ['NVI', 'ARC', 'ACF', 'KJV'])
                ListTile(
                  title: Text(code),
                  trailing: currentVersion == code ? const Icon(Icons.check, color: AppColors.primary) : null,
                  onTap: () {
                    ref.read(selectedVersionProvider.notifier).state = code;
                    ref.invalidate(chapterVersesProvider);
                    Navigator.of(context).pop();
                  },
                ),
            ],
          ),
        ),
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
