import 'package:flutter/material.dart';

import '../providers/quiz_provider.dart';

class QuestionCard extends StatelessWidget {
  final QuizQuestionModel question;
  final void Function(String answer) onAnswer;

  const QuestionCard({
    super.key,
    required this.question,
    required this.onAnswer,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(16),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              question.questionText,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            if (question.category != null)
              Chip(
                label: Text(question.category!),
                padding: EdgeInsets.zero,
              ),
            const SizedBox(height: 16),
            ...question.options.map(
              (opt) => Padding(
                padding: const EdgeInsets.only(bottom: 8),
                child: SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () => onAnswer(opt),
                    child: Text(opt),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

}
