import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../auth/providers/auth_provider.dart';
import '../providers/profile_provider.dart';
import '../widgets/stat_card.dart';

class ReadingStatsScreen extends ConsumerWidget {
  const ReadingStatsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final async = ref.watch(readingStatsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Estatisticas de leitura'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.pop(),
        ),
      ),
      body: async.when(
        data: (stats) => SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 2,
                mainAxisSpacing: 12,
                crossAxisSpacing: 12,
                childAspectRatio: 1.2,
                children: [
                  StatCard(
                    icon: Icons.menu_book,
                    label: 'Capitulos lidos',
                    value: '${stats.chaptersRead}',
                  ),
                  StatCard(
                    icon: Icons.check_circle,
                    label: 'Capitulos completos',
                    value: '${stats.chaptersCompleted}',
                  ),
                  StatCard(
                    icon: Icons.highlight,
                    label: 'Destaques',
                    value: '${stats.highlightsCount}',
                  ),
                  StatCard(
                    icon: Icons.note,
                    label: 'Anotacoes',
                    value: '${stats.annotationsCount}',
                  ),
                  StatCard(
                    icon: Icons.bookmark,
                    label: 'Favoritos',
                    value: '${stats.bookmarksCount}',
                  ),
                ],
              ),
            ],
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Erro: $e'),
              ElevatedButton(
                onPressed: () => ref.invalidate(readingStatsProvider),
                child: const Text('Tentar novamente'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
