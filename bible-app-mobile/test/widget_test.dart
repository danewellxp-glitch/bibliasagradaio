// Basic Flutter widget smoke test (no Firebase/main app).

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('MaterialApp smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Center(child: Text('Biblia Sagrada')),
        ),
      ),
    );
    expect(find.text('Biblia Sagrada'), findsOneWidget);
  });
}
