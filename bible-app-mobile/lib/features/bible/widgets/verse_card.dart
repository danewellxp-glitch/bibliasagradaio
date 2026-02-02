import 'package:flutter/material.dart';

import '../../../data/models/bible_models.dart';

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
      onLongPress: onLongPress,
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
}
