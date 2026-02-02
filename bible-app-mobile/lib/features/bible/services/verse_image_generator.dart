import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:path_provider/path_provider.dart';
import 'package:screenshot/screenshot.dart';

import '../../../data/models/bible_models.dart';

/// Generates an image of a verse with a configurable template for sharing.
class VerseImageGenerator {
  static Future<File?> captureVerseImage(
    BuildContext context, {
    required Verse verse,
    Color? backgroundColor,
    Color? textColor,
    Color? accentColor,
  }) async {
    final controller = ScreenshotController();
    final bg = backgroundColor ?? Colors.white;
    final text = textColor ?? Colors.black87;
    final accent = accentColor ?? Colors.brown;

    final widget = RepaintBoundary(
      child: Container(
        width: 400,
        padding: const EdgeInsets.all(32),
        decoration: BoxDecoration(
          color: bg,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              blurRadius: 8,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: 48,
              height: 4,
              decoration: BoxDecoration(
                color: accent,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: 20),
            Text(
              verse.reference,
              style: TextStyle(
                color: accent,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            Text(
              verse.text,
              style: TextStyle(
                color: text,
                fontSize: 20,
                height: 1.5,
              ),
            ),
            const SizedBox(height: 16),
            Text(
              'Biblia Sagrada App',
              style: TextStyle(
                color: text.withOpacity(0.6),
                fontSize: 12,
              ),
            ),
          ],
        ),
      ),
    );

    try {
      final bytes = await controller.captureFromWidget(
        Material(
          color: Colors.transparent,
          child: widget,
        ),
        pixelRatio: 2,
      );
      if (bytes == null) return null;
      final dir = await getTemporaryDirectory();
      final file = File('${dir.path}/verse_${verse.bookNumber}_${verse.chapter}_${verse.verse}.png');
      await file.writeAsBytes(bytes);
      return file;
    } catch (_) {
      return null;
    }
  }
}
