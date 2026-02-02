import '../../core/services/api_service.dart';
import '../models/bible_models.dart';

class UserContentRepository {
  final ApiService _api;

  UserContentRepository(this._api);

  // Highlights
  Future<List<Highlight>> getHighlights() async {
    final response = await _api.get('/highlights');
    final data = response.data as List;
    return data
        .map((e) => Highlight.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<Highlight> createHighlight(Highlight highlight) async {
    final response =
        await _api.post('/highlights', data: highlight.toJson());
    return Highlight.fromJson(response.data as Map<String, dynamic>);
  }

  Future<void> deleteHighlight(String id) async {
    await _api.delete('/highlights/$id');
  }

  // Annotations
  Future<List<Annotation>> getAnnotations() async {
    final response = await _api.get('/annotations');
    final data = response.data as List;
    return data
        .map((e) => Annotation.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<Annotation> createAnnotation(Annotation annotation) async {
    final response =
        await _api.post('/annotations', data: annotation.toJson());
    return Annotation.fromJson(response.data as Map<String, dynamic>);
  }

  Future<void> deleteAnnotation(String id) async {
    await _api.delete('/annotations/$id');
  }

  // Bookmarks
  Future<List<Bookmark>> getBookmarks() async {
    final response = await _api.get('/bookmarks');
    final data = response.data as List;
    return data
        .map((e) => Bookmark.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<Bookmark> createBookmark(Bookmark bookmark) async {
    final response =
        await _api.post('/bookmarks', data: bookmark.toJson());
    return Bookmark.fromJson(response.data as Map<String, dynamic>);
  }

  Future<void> deleteBookmark(String id) async {
    await _api.delete('/bookmarks/$id');
  }
}
