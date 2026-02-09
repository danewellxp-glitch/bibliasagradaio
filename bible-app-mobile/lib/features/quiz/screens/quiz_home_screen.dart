import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../providers/quiz_provider.dart';
import '../widgets/xp_progress.dart';

class QuizHomeScreen extends ConsumerWidget {
  const QuizHomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final statsAsync = ref.watch(quizStatsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Quiz'),
        actions: [
          IconButton(
            icon: const Icon(Icons.leaderboard),
            onPressed: () => context.push('/games/leaderboard'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            statsAsync.when(
              data: (stats) => XpProgressWidget(
                totalXp: stats.totalXp,
                level: stats.currentLevel,
                streak: stats.currentStreak,
                longestStreak: stats.longestStreak,
                questionsAnswered: stats.totalQuestionsAnswered,
                correctAnswers: stats.totalCorrectAnswers,
              ),
              loading: () => const Card(
                child: Padding(
                  padding: EdgeInsets.all(24),
                  child: Center(child: CircularProgressIndicator()),
                ),
              ),
              error: (e, _) => Card(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Text('Erro ao carregar stats: $e'),
                ),
              ),
            ),
            const SizedBox(height: 32),
            ElevatedButton.icon(
              onPressed: () => context.push('/games/quiz-solo/play'),
              icon: const Icon(Icons.play_arrow, size: 32),
              label: const Text('Iniciar Quiz', style: TextStyle(fontSize: 20)),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 32),
                minimumSize: const Size(double.infinity, 0),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
