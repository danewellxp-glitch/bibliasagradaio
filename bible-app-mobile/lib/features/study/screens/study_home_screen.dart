import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class StudyHomeScreen extends StatelessWidget {
  const StudyHomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Estudos')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _Tile(
            icon: Icons.menu_book,
            title: 'Comentarios biblicos',
            subtitle: 'Leia comentarios sobre livros e versiculos',
            onTap: () => context.push('/studies/commentaries'),
          ),
          _Tile(
            icon: Icons.link,
            title: 'Referencias cruzadas',
            subtitle: 'Explore passagens relacionadas',
            onTap: () => context.push('/studies/cross-references'),
          ),
          _Tile(
            icon: Icons.timeline,
            title: 'Linha do tempo',
            subtitle: 'Eventos biblicos em ordem cronologica',
            onTap: () => context.push('/studies/timeline'),
          ),
          _Tile(
            icon: Icons.map,
            title: 'Mapas',
            subtitle: 'Mapas e geografia biblica',
            onTap: () => context.push('/studies/maps'),
          ),
        ],
      ),
    );
  }
}

class _Tile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const _Tile({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: Icon(icon, color: Theme.of(context).colorScheme.primary),
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.chevron_right),
        onTap: onTap,
      ),
    );
  }
}
