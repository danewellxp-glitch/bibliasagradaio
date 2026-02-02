import '../../core/services/api_service.dart';
import '../models/bible_models.dart';

class BibleRepository {
  final ApiService _api;

  BibleRepository(this._api);

  Future<List<BibleVersion>> getVersions() async {
    final response = await _api.get('/bible/versions');
    final data = response.data as List;
    return data
        .map((e) => BibleVersion.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<List<Verse>> getChapter(
      String version, int book, int chapter) async {
    final response = await _api.get('/bible/$version/$book/$chapter');
    final data = response.data['verses'] as List;
    return data
        .map((e) => Verse.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<Verse?> getVerse(
      String version, int book, int chapter, int verse) async {
    final response =
        await _api.get('/bible/$version/$book/$chapter/$verse');
    return Verse.fromJson(response.data as Map<String, dynamic>);
  }

  Future<List<Verse>> search(String version, String query,
      {int limit = 50}) async {
    final response = await _api
        .get('/bible/$version/search', params: {'q': query, 'limit': limit});
    final data = response.data['results'] as List;
    return data
        .map((e) => Verse.fromJson(e as Map<String, dynamic>))
        .toList();
  }
}
