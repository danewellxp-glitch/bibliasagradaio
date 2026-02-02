import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../features/auth/providers/auth_provider.dart';
import '../features/auth/screens/login_screen.dart';
import '../features/bible/screens/bible_reader_screen.dart';
import '../features/study/screens/commentary_screen.dart';
import '../features/study/screens/cross_references_screen.dart';
import '../features/study/screens/maps_screen.dart';
import '../features/profile/screens/offline_management_screen.dart';
import '../features/sermons/screens/sermons_screen.dart';
import '../features/profile/screens/profile_screen.dart';
import '../features/profile/screens/reading_stats_screen.dart';
import '../features/profile/screens/settings_screen.dart';
import '../features/quiz/screens/leaderboard_screen.dart';
import '../features/quiz/screens/quiz_home_screen.dart';
import '../features/quiz/screens/quiz_play_screen.dart';
import '../features/study/screens/study_home_screen.dart';
import '../features/study/screens/timeline_screen.dart';

final appRouterProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authStateProvider);

  return GoRouter(
    initialLocation: '/bible',
    redirect: (context, state) {
      final isLoggedIn = authState.valueOrNull != null;
      final isLoginRoute = state.matchedLocation == '/login';

      if (!isLoggedIn && !isLoginRoute) return '/login';
      if (isLoggedIn && isLoginRoute) return '/bible';
      return null;
    },
    routes: [
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) {
          return ScaffoldWithNavBar(navigationShell: navigationShell);
        },
        branches: [
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/bible',
              builder: (context, state) =>
                  const BibleReaderScreen(),
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/studies',
              builder: (context, state) => const StudyHomeScreen(),
              routes: [
                GoRoute(
                  path: 'commentaries',
                  builder: (context, state) => const CommentaryScreen(),
                ),
                GoRoute(
                  path: 'cross-references',
                  builder: (context, state) => const CrossReferencesScreen(),
                ),
                GoRoute(
                  path: 'timeline',
                  builder: (context, state) => const TimelineScreen(),
                ),
                GoRoute(
                  path: 'maps',
                  builder: (context, state) => const MapsScreen(),
                ),
              ],
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/sermons',
              builder: (context, state) => const SermonsScreen(),
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/quiz',
              builder: (context, state) => const QuizHomeScreen(),
              routes: [
                GoRoute(
                  path: 'play',
                  builder: (context, state) => const QuizPlayScreen(),
                ),
                GoRoute(
                  path: 'leaderboard',
                  builder: (context, state) => const LeaderboardScreen(),
                ),
              ],
            ),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(
              path: '/profile',
              builder: (context, state) => const ProfileScreen(),
              routes: [
                GoRoute(
                  path: 'reading-stats',
                  builder: (context, state) => const ReadingStatsScreen(),
                ),
                GoRoute(
                  path: 'settings',
                  builder: (context, state) => const SettingsScreen(),
                ),
                GoRoute(
                  path: 'offline',
                  builder: (context, state) => const OfflineManagementScreen(),
                ),
              ],
            ),
          ]),
        ],
      ),
    ],
  );
});

class ScaffoldWithNavBar extends StatelessWidget {
  final StatefulNavigationShell navigationShell;

  const ScaffoldWithNavBar({super.key, required this.navigationShell});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: NavigationBar(
        selectedIndex: navigationShell.currentIndex,
        onDestinationSelected: (index) => navigationShell.goBranch(index),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.book), label: 'Biblia'),
          NavigationDestination(icon: Icon(Icons.school), label: 'Estudos'),
          NavigationDestination(icon: Icon(Icons.mic), label: 'Pregacoes'),
          NavigationDestination(icon: Icon(Icons.quiz), label: 'Quiz'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Perfil'),
        ],
      ),
    );
  }
}

class PlaceholderScreen extends StatelessWidget {
  final String title;

  const PlaceholderScreen({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(
        child: Text(
          title,
          style: const TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}
