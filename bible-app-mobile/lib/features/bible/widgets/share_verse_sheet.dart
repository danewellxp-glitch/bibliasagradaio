import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';

import '../../../data/models/bible_models.dart';
import '../services/verse_image_generator.dart';

class ShareVerseSheet extends StatelessWidget {
  final Verse verse;

  const ShareVerseSheet({super.key, required this.verse});

  static Future<void> show(BuildContext context, Verse verse) {
    return showModalBottomSheet(
      context: context,
      builder: (ctx) => ShareVerseSheet(verse: verse),
    );
  }

  @override
  Widget build(BuildContext context) {
    final text = '${verse.reference}\n\n"${verse.text}"\n\n— Biblia Sagrada App';

    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              verse.reference,
              style: Theme.of(context).textTheme.titleMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              verse.text,
              style: Theme.of(context).textTheme.bodyMedium,
              maxLines: 3,
              overflow: TextOverflow.ellipsis,
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () async {
                await Share.share(text);
                if (context.mounted) Navigator.of(context).pop();
              },
              icon: const Icon(Icons.text_fields),
              label: const Text('Compartilhar como texto'),
            ),
            const SizedBox(height: 12),
            ElevatedButton.icon(
              onPressed: () async {
                final file = await VerseImageGenerator.captureVerseImage(
                  context,
                  verse: verse,
                );
                if (file != null) {
                  await Share.shareXFiles(
                    [XFile(file.path)],
                    text: verse.reference,
                  );
                }
                if (context.mounted) Navigator.of(context).pop();
              },
              icon: const Icon(Icons.image),
              label: const Text('Compartilhar como imagem'),
            ),
          ],
        ),
      ),
    );
  }
}
