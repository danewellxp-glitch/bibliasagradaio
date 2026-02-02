import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../data/models/bible_models.dart';

class HighlightMenu extends StatelessWidget {
  final Verse verse;
  final VoidCallback onAnnotate;
  final VoidCallback onBookmark;
  final VoidCallback onShare;
  final void Function(String color) onHighlight;
  final VoidCallback? onRemoveHighlight;

  const HighlightMenu({
    super.key,
    required this.verse,
    required this.onAnnotate,
    required this.onBookmark,
    required this.onShare,
    required this.onHighlight,
    this.onRemoveHighlight,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Verse reference
          Text(
            verse.reference,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 16),

          // Highlight colors row
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _ColorButton(
                color: AppColors.highlightYellow,
                label: 'Amarelo',
                onTap: () => onHighlight('yellow'),
              ),
              const SizedBox(width: 12),
              _ColorButton(
                color: AppColors.highlightGreen,
                label: 'Verde',
                onTap: () => onHighlight('green'),
              ),
              const SizedBox(width: 12),
              _ColorButton(
                color: AppColors.highlightBlue,
                label: 'Azul',
                onTap: () => onHighlight('blue'),
              ),
              const SizedBox(width: 12),
              _ColorButton(
                color: AppColors.highlightRed,
                label: 'Vermelho',
                onTap: () => onHighlight('red'),
              ),
              const SizedBox(width: 12),
              _ColorButton(
                color: AppColors.highlightPurple,
                label: 'Roxo',
                onTap: () => onHighlight('purple'),
              ),
            ],
          ),

          if (onRemoveHighlight != null) ...[
            const SizedBox(height: 8),
            TextButton(
              onPressed: onRemoveHighlight,
              child: const Text(
                'Remover destaque',
                style: TextStyle(color: Colors.grey),
              ),
            ),
          ],

          const Divider(height: 24),

          // Actions row
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _ActionButton(
                icon: Icons.edit_note,
                label: 'Anotar',
                onTap: onAnnotate,
              ),
              _ActionButton(
                icon: Icons.bookmark_border,
                label: 'Favoritar',
                onTap: onBookmark,
              ),
              _ActionButton(
                icon: Icons.share,
                label: 'Compartilhar',
                onTap: onShare,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _ColorButton extends StatelessWidget {
  final Color color;
  final String label;
  final VoidCallback onTap;

  const _ColorButton({
    required this.color,
    required this.label,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Tooltip(
        message: label,
        child: Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
            border: Border.all(color: Colors.black12),
          ),
        ),
      ),
    );
  }
}

class _ActionButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  const _ActionButton({
    required this.icon,
    required this.label,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(8),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 28),
            const SizedBox(height: 4),
            Text(label, style: const TextStyle(fontSize: 12)),
          ],
        ),
      ),
    );
  }
}
