import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../data/models/bible_models.dart';

class AnnotationDialog extends StatefulWidget {
  final Verse verse;
  final String? existingNote;

  const AnnotationDialog({
    super.key,
    required this.verse,
    this.existingNote,
  });

  @override
  State<AnnotationDialog> createState() => _AnnotationDialogState();
}

class _AnnotationDialogState extends State<AnnotationDialog> {
  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: widget.existingNote ?? '');
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(
        'Anotacao - ${widget.verse.reference}',
        style: const TextStyle(fontSize: 16),
      ),
      content: TextField(
        controller: _controller,
        maxLines: 6,
        decoration: const InputDecoration(
          hintText: 'Escreva sua anotacao...',
          border: OutlineInputBorder(),
        ),
        autofocus: true,
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Cancelar'),
        ),
        ElevatedButton(
          onPressed: () {
            final text = _controller.text.trim();
            if (text.isNotEmpty) {
              Navigator.of(context).pop(text);
            }
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.primary,
            foregroundColor: Colors.white,
          ),
          child: const Text('Salvar'),
        ),
      ],
    );
  }
}
