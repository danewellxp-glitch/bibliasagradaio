import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/constants/bible_books.dart';
import '../../../data/models/bible_models.dart';
import '../../study/providers/study_provider.dart';
import '../providers/bible_provider.dart';
import 'ask_ai_dialog.dart';

class VerseStudySheet extends ConsumerWidget {
  final Verse verse;

  const VerseStudySheet({super.key, required this.verse});

  static void show(BuildContext context, Verse verse) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      builder: (_) => DraggableScrollableSheet(
        initialChildSize: 0.75,
        minChildSize: 0.4,
        maxChildSize: 0.95,
        expand: false,
        builder: (_, controller) => VerseStudySheet._(
          verse: verse,
          scrollController: controller,
        ),
      ),
    );
  }

  const VerseStudySheet._({
    required this.verse,
    required this.scrollController,
  });

  final ScrollController? scrollController;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final version = ref.watch(selectedVersionProvider);
    final contextAsync = ref.watch(
      verseContextProvider((
        version: version,
        book: verse.bookNumber,
        chapter: verse.chapter,
        verse: verse.verse,
      )),
    );

    return DefaultTabController(
      length: 3,
      child: Column(
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
          // Verse reference header
          Padding(
            padding: const EdgeInsets.all(16),
            child: Text(
              verse.reference,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          // Verse text
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Text(
              verse.text,
              style: TextStyle(
                fontSize: 14,
                fontStyle: FontStyle.italic,
                color: Colors.grey[700],
              ),
              textAlign: TextAlign.center,
            ),
          ),
          const SizedBox(height: 8),
          // Ask AI button
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: OutlinedButton.icon(
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (_) => AskAIDialog(verse: verse),
                );
              },
              icon: const Icon(Icons.auto_awesome, size: 18),
              label: const Text('Perguntar sobre este versiculo'),
              style: OutlinedButton.styleFrom(
                foregroundColor: Colors.deepPurple,
                side: const BorderSide(color: Colors.deepPurple),
              ),
            ),
          ),
          const SizedBox(height: 8),
          // Tabs
          const TabBar(
            tabs: [
              Tab(text: 'Comentarios'),
              Tab(text: 'Refs Cruzadas'),
              Tab(text: 'Timeline'),
            ],
          ),
          // Tab content
          Expanded(
            child: contextAsync.when(
              data: (ctx) => TabBarView(
                children: [
                  _CommentariesTab(
                    commentaries: ctx.commentaries,
                    scrollController: scrollController,
                  ),
                  _CrossRefsTab(
                    crossRefs: ctx.crossReferences,
                    scrollController: scrollController,
                    onNavigate: (book, chapter, verse) {
                      Navigator.of(context).pop();
                      ref.read(selectedBookProvider.notifier).state = book;
                      ref.read(selectedChapterProvider.notifier).state = chapter;
                    },
                  ),
                  _TimelineTab(
                    events: ctx.timelineEvents,
                    scrollController: scrollController,
                  ),
                ],
              ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, _) => Center(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.cloud_off, size: 48, color: Colors.grey),
                      const SizedBox(height: 12),
                      Text(
                        'Nao foi possivel carregar o contexto.',
                        textAlign: TextAlign.center,
                        style: Theme.of(context).textTheme.bodyLarge,
                      ),
                      const SizedBox(height: 16),
                      FilledButton.icon(
                        onPressed: () => ref.invalidate(verseContextProvider),
                        icon: const Icon(Icons.refresh),
                        label: const Text('Tentar novamente'),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _CommentariesTab extends StatelessWidget {
  final List<Commentary> commentaries;
  final ScrollController? scrollController;

  const _CommentariesTab({
    required this.commentaries,
    this.scrollController,
  });

  @override
  Widget build(BuildContext context) {
    if (commentaries.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Text(
            'Nenhum comentario disponivel para este versiculo.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey),
          ),
        ),
      );
    }
    return ListView.builder(
      controller: scrollController,
      padding: const EdgeInsets.all(16),
      itemCount: commentaries.length,
      itemBuilder: (context, index) {
        final c = commentaries[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.person, size: 16, color: Colors.grey),
                    const SizedBox(width: 4),
                    Expanded(
                      child: Text(
                        c.author,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 13,
                        ),
                      ),
                    ),
                    if (c.source != null)
                      Text(
                        c.source!,
                        style: TextStyle(
                          fontSize: 11,
                          color: Colors.grey[600],
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  c.commentary,
                  style: const TextStyle(fontSize: 14, height: 1.5),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

class _CrossRefsTab extends StatelessWidget {
  final List<CrossRef> crossRefs;
  final ScrollController? scrollController;
  final void Function(int book, int chapter, int verse) onNavigate;

  const _CrossRefsTab({
    required this.crossRefs,
    this.scrollController,
    required this.onNavigate,
  });

  @override
  Widget build(BuildContext context) {
    if (crossRefs.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Text(
            'Nenhuma referencia cruzada disponivel.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey),
          ),
        ),
      );
    }
    return ListView.builder(
      controller: scrollController,
      padding: const EdgeInsets.all(16),
      itemCount: crossRefs.length,
      itemBuilder: (context, index) {
        final cr = crossRefs[index];
        final toBook = getBookByNumber(cr.toBook);
        return ListTile(
          leading: const Icon(Icons.link, size: 20),
          title: Text('${toBook.name} ${cr.toChapter}:${cr.toVerse}'),
          subtitle: cr.relationshipType != null
              ? Text(
                  cr.relationshipType!,
                  style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                )
              : null,
          trailing: const Icon(Icons.chevron_right, size: 20),
          onTap: () => onNavigate(cr.toBook, cr.toChapter, cr.toVerse),
        );
      },
    );
  }
}

class _TimelineTab extends StatelessWidget {
  final List<TimelineEventModel> events;
  final ScrollController? scrollController;

  const _TimelineTab({
    required this.events,
    this.scrollController,
  });

  @override
  Widget build(BuildContext context) {
    if (events.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Text(
            'Nenhum evento na timeline relacionado.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey),
          ),
        ),
      );
    }
    return ListView.builder(
      controller: scrollController,
      padding: const EdgeInsets.all(16),
      itemCount: events.length,
      itemBuilder: (context, index) {
        final e = events[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.schedule, size: 16, color: Colors.grey),
                    const SizedBox(width: 4),
                    Expanded(
                      child: Text(
                        e.eventName,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      ),
                    ),
                    if (e.approximateDate != null)
                      Text(
                        e.approximateDate!,
                        style: TextStyle(
                          fontSize: 11,
                          color: Colors.grey[600],
                        ),
                      ),
                  ],
                ),
                if (e.description != null) ...[
                  const SizedBox(height: 8),
                  Text(
                    e.description!,
                    style: const TextStyle(fontSize: 13, height: 1.4),
                  ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }
}
