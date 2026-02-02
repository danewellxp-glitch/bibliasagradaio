import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:bible_app/features/quiz/providers/quiz_provider.dart';
import 'package:bible_app/features/quiz/screens/quiz_home_screen.dart';

void main() {
  final sampleStats = QuizStatsModel(
    totalXp: 100,
    currentLevel: 2,
    currentStreak: 3,
    longestStreak: 5,
    totalQuestionsAnswered: 10,
    totalCorrectAnswers: 8,
  );

  testWidgets('QuizHomeScreen shows scaffold and Quiz title', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          quizStatsProvider.overrideWith(
            (ref) => Future.value(sampleStats),
          ),
        ],
        child: MaterialApp(
          home: const QuizHomeScreen(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.byType(Scaffold), findsOneWidget);
    expect(find.text('Quiz'), findsOneWidget);
  });

  testWidgets('QuizHomeScreen shows Iniciar Quiz button', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          quizStatsProvider.overrideWith(
            (ref) => Future.value(sampleStats),
          ),
        ],
        child: MaterialApp(
          home: const QuizHomeScreen(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Iniciar Quiz'), findsOneWidget);
  });

  testWidgets('QuizHomeScreen has leaderboard action', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          quizStatsProvider.overrideWith(
            (ref) => Future.value(sampleStats),
          ),
        ],
        child: MaterialApp(
          home: const QuizHomeScreen(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.byIcon(Icons.leaderboard), findsOneWidget);
  });
}
