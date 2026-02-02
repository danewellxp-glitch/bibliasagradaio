import 'package:flutter/material.dart';

class XpProgressWidget extends StatelessWidget {
  final int totalXp;
  final int level;
  final int streak;
  final int longestStreak;
  final int questionsAnswered;
  final int correctAnswers;

  const XpProgressWidget({
    super.key,
    required this.totalXp,
    required this.level,
    required this.streak,
    required this.longestStreak,
    required this.questionsAnswered,
    required this.correctAnswers,
  });

  @override
  Widget build(BuildContext context) {
    final xpInLevel = totalXp % 100;
    final progress = xpInLevel / 100.0;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Nivel $level',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                Row(
                  children: [
                    const Icon(Icons.local_fire_department, color: Colors.orange),
                    const SizedBox(width: 4),
                    Text('$streak dias', style: const TextStyle(fontSize: 16)),
                  ],
                ),
              ],
            ),
            const SizedBox(height: 12),
            LinearProgressIndicator(
              value: progress,
              minHeight: 8,
              borderRadius: BorderRadius.circular(4),
            ),
            const SizedBox(height: 4),
            Text(
              '$xpInLevel / 100 XP para o proximo nivel',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _Stat(label: 'Total XP', value: '$totalXp'),
                _Stat(label: 'Perguntas', value: '$questionsAnswered'),
                _Stat(label: 'Acertos', value: '$correctAnswers'),
                _Stat(label: 'Maior streak', value: '$longestStreak'),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _Stat extends StatelessWidget {
  final String label;
  final String value;

  const _Stat({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(value, style: Theme.of(context).textTheme.titleMedium),
        Text(label, style: Theme.of(context).textTheme.bodySmall),
      ],
    );
  }
}
