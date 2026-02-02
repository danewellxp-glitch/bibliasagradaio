import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:bible_app/data/models/bible_models.dart';
import 'package:bible_app/features/bible/providers/bible_provider.dart';
import 'package:bible_app/features/bible/providers/user_content_provider.dart';
import 'package:bible_app/features/bible/screens/bible_reader_screen.dart';

void main() {
  final sampleVerses = [
    const Verse(
      bookNumber: 1,
      bookName: 'Gênesis',
      chapter: 1,
      verse: 1,
      text: 'No princípio criou Deus os céus e a terra.',
    ),
    const Verse(
      bookNumber: 1,
      bookName: 'Gênesis',
      chapter: 1,
      verse: 2,
      text: 'E a terra era sem forma e vazia.',
    ),
  ];

  testWidgets('BibleReaderScreen shows scaffold with app bar', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          chapterVersesProvider.overrideWith((ref) => Future.value(sampleVerses)),
          highlightsProvider.overrideWith((ref) => Future.value([])),
        ],
        child: MaterialApp(
          home: const BibleReaderScreen(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.byType(Scaffold), findsOneWidget);
    expect(find.byType(AppBar), findsOneWidget);
  });

  testWidgets('BibleReaderScreen shows verse text when data is loaded',
      (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          chapterVersesProvider.overrideWith((ref) => Future.value(sampleVerses)),
          highlightsProvider.overrideWith((ref) => Future.value([])),
        ],
        child: MaterialApp(
          home: const BibleReaderScreen(),
        ),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.textContaining('No princípio criou Deus'), findsOneWidget);
    expect(find.textContaining('E a terra era sem forma'), findsOneWidget);
  });
}
