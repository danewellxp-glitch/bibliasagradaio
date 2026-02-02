import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/services/offline_service.dart';
import '../../../data/models/bible_models.dart';
import '../../../data/repositories/bible_repository.dart';
import '../../../data/repositories/offline_bible_repository.dart';
import '../../auth/providers/auth_provider.dart';

final offlineServiceProvider = Provider<OfflineService>((ref) => OfflineService());

final bibleRepositoryProvider = Provider<BibleRepository>((ref) {
  return BibleRepository(ref.read(apiServiceProvider));
});

/// Offline-first Bible repository: local SQLite first, then API.
final offlineBibleRepositoryProvider = Provider<OfflineBibleRepository>((ref) {
  return OfflineBibleRepository(
    ref.read(bibleRepositoryProvider),
    ref.read(offlineServiceProvider),
  );
});

final versionsProvider = FutureProvider<List<BibleVersion>>((ref) {
  return ref.read(offlineBibleRepositoryProvider).getVersions();
});

final selectedVersionProvider = StateProvider<String>((ref) => 'ARA');
final selectedBookProvider = StateProvider<int>((ref) => 1);
final selectedChapterProvider = StateProvider<int>((ref) => 1);

final chapterVersesProvider = FutureProvider<List<Verse>>((ref) {
  final version = ref.watch(selectedVersionProvider);
  final book = ref.watch(selectedBookProvider);
  final chapter = ref.watch(selectedChapterProvider);
  return ref.read(offlineBibleRepositoryProvider).getChapter(version, book, chapter);
});

final searchQueryProvider = StateProvider<String>((ref) => '');

final searchResultsProvider = FutureProvider<List<Verse>>((ref) {
  final query = ref.watch(searchQueryProvider);
  if (query.isEmpty) return Future.value([]);
  final version = ref.watch(selectedVersionProvider);
  return ref.read(offlineBibleRepositoryProvider).search(version, query);
});

/// List of version codes available offline (for settings/UI).
final downloadedVersionsProvider = FutureProvider<List<String>>((ref) {
  return ref.read(offlineServiceProvider).getDownloadedVersionCodes();
});
