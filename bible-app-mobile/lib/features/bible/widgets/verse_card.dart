import 'package:flutter/material.dart';

import '../../../data/models/bible_models.dart';
import 'word_detail_sheet.dart';

class VerseCard extends StatelessWidget {
  final Verse verse;
  final VoidCallback? onTap;
  final VoidCallback? onLongPress;
  final Color? highlightColor;

  const VerseCard({
    super.key,
    required this.verse,
    this.onTap,
    this.onLongPress,
    this.highlightColor,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      onLongPress: () => _showWordSelector(context),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(vertical: 6, horizontal: 4),
        decoration: highlightColor != null
            ? BoxDecoration(
                color: highlightColor!.withOpacity(0.25),
                borderRadius: BorderRadius.circular(4),
              )
            : null,
        child: RichText(
          text: TextSpan(
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  fontFamily: 'Georgia',
                  height: 1.7,
                  fontSize: 16,
                ),
            children: [
              TextSpan(
                text: ' ${verse.verse} ',
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).colorScheme.primary,
                  fontFamily: 'Roboto',
                ),
              ),
              TextSpan(text: verse.text),
            ],
          ),
        ),
      ),
    );
  }

  void _showWordSelector(BuildContext context) {
    final words = verse.text
        .split(RegExp(r'\s+'))
        .where((w) => w.isNotEmpty)
        .toList();

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(
          verse.reference,
          style: const TextStyle(fontSize: 16),
        ),
        content: SingleChildScrollView(
          child: Wrap(
            spacing: 6,
            runSpacing: 6,
            children: words.map((word) {
              // Strip punctuation for lookup
              final clean = word.replaceAll(RegExp(r'[^\w\sáéíóúãõâêôçÁÉÍÓÚÃÕÂÊÔÇ]'), '');
              return ActionChip(
                label: Text(word),
                onPressed: () {
                  Navigator.of(ctx).pop();
                  WordDetailSheet.show(context, clean);
                },
              );
            }).toList(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Fechar'),
          ),
        ],
      ),
    );
  }
}
