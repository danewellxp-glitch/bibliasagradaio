import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/app_colors.dart';
import '../../auth/providers/auth_provider.dart';
import '../providers/game_provider.dart';

class GameResultScreen extends ConsumerWidget {
  final String roomCode;

  const GameResultScreen({super.key, required this.roomCode});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Resultado'),
        automaticallyImplyLeading: false,
      ),
      body: FutureBuilder<List<GameResultEntry>>(
        future: getResults(ref.read(apiServiceProvider), roomCode),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline, size: 48),
                  const SizedBox(height: 12),
                  Text('Erro: ${snapshot.error}'),
                ],
              ),
            );
          }
          final results = snapshot.data ?? [];
          if (results.isEmpty) {
            return const Center(child: Text('Nenhum resultado disponivel'));
          }

          return Column(
            children: [
              const SizedBox(height: 16),
              // Podium
              if (results.isNotEmpty) _buildPodium(results),
              const SizedBox(height: 16),
              // Full list
              Expanded(
                child: ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  itemCount: results.length,
                  itemBuilder: (context, index) {
                    final r = results[index];
                    return Card(
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: _rankColor(r.rank),
                          child: Text(
                            '#${r.rank}',
                            style: const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                            ),
                          ),
                        ),
                        title: Text(
                          r.displayName ?? 'Jogador',
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        subtitle: Text(
                          '${r.answersCorrect}/${r.answersTotal} corretas',
                        ),
                        trailing: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.end,
                          children: [
                            Text(
                              '${r.score} pts',
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                              ),
                            ),
                            Text(
                              '+${r.xpEarned} XP',
                              style: TextStyle(
                                fontSize: 12,
                                color: AppColors.success,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),
              // Back button
              Padding(
                padding: const EdgeInsets.all(24),
                child: FilledButton.icon(
                  onPressed: () => context.go('/games'),
                  icon: const Icon(Icons.home),
                  label: const Text('Voltar ao Menu'),
                  style: FilledButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    minimumSize: const Size(double.infinity, 0),
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildPodium(List<GameResultEntry> results) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          if (results.length > 1)
            _PodiumPlace(
              rank: 2,
              name: results[1].displayName ?? 'Jogador',
              score: results[1].score,
              height: 80,
            ),
          _PodiumPlace(
            rank: 1,
            name: results[0].displayName ?? 'Jogador',
            score: results[0].score,
            height: 110,
          ),
          if (results.length > 2)
            _PodiumPlace(
              rank: 3,
              name: results[2].displayName ?? 'Jogador',
              score: results[2].score,
              height: 60,
            ),
        ],
      ),
    );
  }

  Color _rankColor(int rank) {
    switch (rank) {
      case 1:
        return AppColors.secondary;
      case 2:
        return Colors.grey;
      case 3:
        return Colors.brown;
      default:
        return AppColors.primary;
    }
  }
}

class _PodiumPlace extends StatelessWidget {
  final int rank;
  final String name;
  final int score;
  final double height;

  const _PodiumPlace({
    required this.rank,
    required this.name,
    required this.score,
    required this.height,
  });

  @override
  Widget build(BuildContext context) {
    final color = rank == 1
        ? AppColors.secondary
        : rank == 2
            ? Colors.grey
            : Colors.brown;

    return Expanded(
      child: Column(
        children: [
          Text(
            rank == 1 ? '👑' : '',
            style: const TextStyle(fontSize: 24),
          ),
          const SizedBox(height: 4),
          Text(
            name,
            style: const TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 12,
            ),
            textAlign: TextAlign.center,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 4),
          Container(
            height: height,
            margin: const EdgeInsets.symmetric(horizontal: 4),
            decoration: BoxDecoration(
              color: color.withOpacity(0.2),
              borderRadius:
                  const BorderRadius.vertical(top: Radius.circular(8)),
              border: Border.all(color: color.withOpacity(0.5)),
            ),
            child: Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    '#$rank',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: color,
                    ),
                  ),
                  Text(
                    '$score pts',
                    style: TextStyle(fontSize: 11, color: color),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
