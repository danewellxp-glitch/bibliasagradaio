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

final selectedVersionProvider = StateProvider<String>((ref) => 'NVI');
/// Version ID for the currently selected version (for API calls that need version_id).
final selectedVersionIdProvider = Provider<int>((ref) {
  final code = ref.watch(selectedVersionProvider);
  final versions = ref.watch(versionsProvider).valueOrNull ?? [];
  for (final v in versions) {
    if (v.code == code) return v.id;
  }
  return versions.isNotEmpty ? versions.first.id : 1;
});
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

/// Verse of the day from the backend API.
final verseOfTheDayProvider = FutureProvider<Verse?>((ref) async {
  try {
    final api = ref.read(apiServiceProvider);
    final version = ref.watch(selectedVersionProvider);
    final res = await api.get('/bible/verse-of-the-day', params: {'version': version});
    return Verse.fromJson(res.data as Map<String, dynamic>);
  } catch (_) {
    return null;
  }
});
