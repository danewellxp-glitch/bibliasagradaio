import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../auth/providers/auth_provider.dart';
import '../../quiz/providers/quiz_provider.dart';
import '../providers/profile_provider.dart';
import '../widgets/stat_card.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authStateProvider).valueOrNull;
    final readingAsync = ref.watch(readingStatsProvider);
    final quizAsync = ref.watch(quizStatsProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Perfil')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (user != null)
              Card(
                child: ListTile(
                  leading: CircleAvatar(
                    backgroundImage: user.photoURL != null
                        ? NetworkImage(user.photoURL!)
                        : null,
                    child: user.photoURL == null
                        ? Text(
                            (user.displayName ?? user.email ?? '?')
                                .substring(0, 1)
                                .toUpperCase(),
                          )
                        : null,
                  ),
                  title: Text(user.displayName ?? 'Usuario'),
                  subtitle: Text(user.email ?? ''),
                ),
              ),
            const SizedBox(height: 24),
            Text(
              'Resumo',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: readingAsync.when(
                    data: (s) => StatCard(
                      icon: Icons.menu_book,
                      label: 'Capitulos lidos',
                      value: '${s.chaptersRead}',
                    ),
                    loading: () => const StatCard(
                      icon: Icons.menu_book,
                      label: 'Capitulos',
                      value: '-',
                    ),
                    error: (_, __) => const StatCard(
                      icon: Icons.menu_book,
                      label: 'Capitulos',
                      value: '-',
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: quizAsync.when(
                    data: (s) => StatCard(
                      icon: Icons.quiz,
                      label: 'XP',
                      value: '${s.totalXp}',
                      color: Colors.amber,
                    ),
                    loading: () => const StatCard(
                      icon: Icons.quiz,
                      label: 'XP',
                      value: '-',
                    ),
                    error: (_, __) => const StatCard(
                      icon: Icons.quiz,
                      label: 'XP',
                      value: '-',
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            ListTile(
              leading: const Icon(Icons.bar_chart),
              title: const Text('Estatisticas de leitura'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => context.push('/profile/reading-stats'),
            ),
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text('Configuracoes'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => context.push('/profile/settings'),
            ),
            ListTile(
              leading: const Icon(Icons.download),
              title: const Text('Versoes offline'),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => context.push('/profile/offline'),
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.logout),
              title: const Text('Sair'),
              onTap: () async {
                await ref.read(authServiceProvider).signOut();
                if (context.mounted) context.go('/login');
              },
            ),
          ],
        ),
      ),
    );
  }
}
