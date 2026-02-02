import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

class QuizResultScreen extends ConsumerWidget {
  final bool correct;
  final String correctAnswer;
  final String? explanation;
  final int xpEarned;
  final int streak;

  const QuizResultScreen({
    super.key,
    required this.correct,
    required this.correctAnswer,
    this.explanation,
    required this.xpEarned,
    required this.streak,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Resultado')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Icon(
              correct ? Icons.check_circle : Icons.cancel,
              size: 80,
              color: correct ? Colors.green : Colors.red,
            ),
            const SizedBox(height: 24),
            Text(
              correct ? 'Correto!' : 'Incorreto',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            Text('Resposta correta: $correctAnswer'),
            if (explanation != null) ...[
              const SizedBox(height: 16),
              Text(explanation!),
            ],
            if (xpEarned > 0) ...[
              const SizedBox(height: 16),
              Text('+$xpEarned XP${streak > 0 ? ' | Streak: $streak dias' : ''}'),
            ],
            const SizedBox(height: 32),
            FilledButton(
              onPressed: () => context.go('/quiz'),
              child: const Text('Voltar ao Quiz'),
            ),
          ],
        ),
      ),
    );
  }
}
