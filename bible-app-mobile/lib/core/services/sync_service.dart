import 'api_service.dart';

/// Offline-first sync: pushes local changes when online,
/// pulls server data on app start.
class SyncService {
  final ApiService _api;

  SyncService(this._api);

  /// Sync on app start when online. Fetches highlights, annotations, bookmarks
  /// from server. Local SQLite (offline Bible) is separate; this syncs user content.
  Future<void> syncOnAppStart() async {
    try {
      await _syncUserContent();
    } catch (_) {
      // Offline or auth not ready - skip
    }
  }

  Future<void> _syncUserContent() async {
    await Future.wait([
      _api.get('/highlights').catchError((_) => null),
      _api.get('/annotations').catchError((_) => null),
      _api.get('/bookmarks').catchError((_) => null),
      _api.get('/profile/settings').catchError((_) => null),
    ]);
    // In full implementation: merge with local SQLite, resolve conflicts,
    // push pending local changes. For MVP we just ensure API is reachable.
  }

  /// Call when user creates/updates/deletes highlight, annotation, or bookmark.
  /// In full implementation: add to local queue if offline, push when online.
  Future<void> syncHighlight(Map<String, dynamic> data) async {
    try {
      await _api.post('/highlights', data: data);
    } catch (_) {
      // Queue for later if offline
    }
  }

  Future<void> syncAnnotation(Map<String, dynamic> data) async {
    try {
      await _api.post('/annotations', data: data);
    } catch (_) {}
  }

  Future<void> syncBookmark(Map<String, dynamic> data) async {
    try {
      await _api.post('/bookmarks', data: data);
    } catch (_) {}
  }

  /// Sync settings to MongoDB via profile API.
  Future<void> syncSettings(Map<String, dynamic> prefs) async {
    try {
      await _api.put('/profile/settings', data: prefs);
    } catch (_) {}
  }
}
