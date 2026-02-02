import '../../core/constants/bible_books.dart';
import '../../core/services/offline_service.dart';
import '../models/bible_models.dart';
import 'bible_repository.dart';

/// Repository that provides offline-first Bible reading: tries local SQLite
/// first, then falls back to API. Supports downloading a full version for offline.
class OfflineBibleRepository {
  final BibleRepository _apiRepository;
  final OfflineService _offlineService;

  OfflineBibleRepository(this._apiRepository, this._offlineService);

  /// Versions list always from API.
  Future<List<BibleVersion>> getVersions() => _apiRepository.getVersions();

  /// Get chapter: offline first, then API. If version is downloaded and we have
  /// no data for this chapter, returns empty list.
  Future<List<Verse>> getChapter(
    String version,
    int book,
    int chapter,
  ) async {
    await _offlineService.init();
    final downloaded = await _offlineService.isVersionDownloaded(version);
    final local = await _offlineService.getChapter(version, book, chapter);
    if (local.isNotEmpty) return local;
    if (downloaded) return []; // downloaded but no data for this chapter
    return _apiRepository.getChapter(version, book, chapter);
  }

  /// Single verse: try offline first, then API.
  Future<Verse?> getVerse(
    String version,
    int book,
    int chapter,
    int verse,
  ) async {
    final verses = await getChapter(version, book, chapter);
    try {
      return verses.firstWhere((v) => v.verse == verse);
    } catch (_) {
      return null;
    }
  }

  /// Search: use API (optional: add local search later for downloaded versions).
  Future<List<Verse>> search(
    String version,
    String query, {
    int limit = 50,
  }) =>
      _apiRepository.search(version, query, limit: limit);

  /// Whether the given version is available offline.
  Future<bool> isVersionDownloaded(String versionCode) =>
      _offlineService.isVersionDownloaded(versionCode);

  /// List of version codes that are downloaded.
  Future<List<String>> getDownloadedVersionCodes() =>
      _offlineService.getDownloadedVersionCodes();

  /// Download full Bible for a version and store in SQLite.
  /// [onProgress] is called with (chaptersDone, totalChapters).
  Future<void> downloadVersion(
    String versionCode, {
    void Function(int chaptersDone, int totalChapters)? onProgress,
  }) async {
    await _offlineService.init();
    final total = OfflineService.totalChapters;
    int done = 0;
    for (final book in bibleBooks) {
      for (var c = 1; c <= book.chapters; c++) {
        final verses = await _apiRepository.getChapter(
          versionCode,
          book.number,
          c,
        );
        await _offlineService.insertVerses(
          versionCode,
          book.number,
          book.name,
          c,
          verses,
        );
        done++;
        onProgress?.call(done, total);
      }
    }
    await _offlineService.setVersionDownloaded(versionCode, true);
  }

  /// Remove downloaded version to free space.
  Future<void> removeDownloadedVersion(String versionCode) =>
      _offlineService.removeVersion(versionCode);
}
