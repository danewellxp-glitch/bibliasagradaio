import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'core/theme/app_theme.dart';
import 'features/auth/providers/auth_provider.dart';
import 'features/onboarding/screens/onboarding_screen.dart';
import 'routing/app_router.dart';

final onboardingCompleteProvider = StateProvider<bool>((ref) => true);

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  final prefs = await SharedPreferences.getInstance();
  final onboardingComplete = prefs.getBool('onboarding_complete') ?? false;

  runApp(ProviderScope(
    overrides: [
      onboardingCompleteProvider.overrideWith((ref) => onboardingComplete),
    ],
    child: const BibleApp(),
  ));
}

class BibleApp extends ConsumerStatefulWidget {
  const BibleApp({super.key});

  @override
  ConsumerState<BibleApp> createState() => _BibleAppState();
}

class _BibleAppState extends ConsumerState<BibleApp> {
  @override
  Widget build(BuildContext context) {
    // Sync user content when auth state changes to logged-in
    ref.listen(authStateProvider, (previous, next) {
      final wasLoggedOut = previous?.value == null;
      final isLoggedIn = next.value != null;
      if (wasLoggedOut && isLoggedIn) {
        ref.read(syncServiceProvider).syncOnAppStart();
      }
    });
    final onboardingDone = ref.watch(onboardingCompleteProvider);

    if (!onboardingDone) {
      return MaterialApp(
        title: 'Biblia Sagrada',
        theme: AppTheme.light,
        darkTheme: AppTheme.dark,
        debugShowCheckedModeBanner: false,
        home: OnboardingScreen(
          onComplete: () {
            ref.read(onboardingCompleteProvider.notifier).state = true;
          },
        ),
      );
    }

    final router = ref.watch(appRouterProvider);
    return MaterialApp.router(
      title: 'Biblia Sagrada',
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      routerConfig: router,
      debugShowCheckedModeBanner: false,
    );
  }
}
