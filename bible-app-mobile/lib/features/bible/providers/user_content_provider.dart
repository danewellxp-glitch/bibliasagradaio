import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../data/models/bible_models.dart';
import '../../../data/repositories/user_content_repository.dart';
import '../../auth/providers/auth_provider.dart';

final userContentRepositoryProvider =
    Provider<UserContentRepository>((ref) {
  return UserContentRepository(ref.read(apiServiceProvider));
});

final highlightsProvider =
    FutureProvider<List<Highlight>>((ref) {
  return ref.read(userContentRepositoryProvider).getHighlights();
});

final annotationsProvider =
    FutureProvider<List<Annotation>>((ref) {
  return ref.read(userContentRepositoryProvider).getAnnotations();
});

final bookmarksProvider =
    FutureProvider<List<Bookmark>>((ref) {
  return ref.read(userContentRepositoryProvider).getBookmarks();
});

/// Get highlight color for a specific verse (if exists)
String? getHighlightForVerse(
  List<Highlight> highlights,
  int versionId,
  int book,
  int chapter,
  int verse,
) {
  try {
    final h = highlights.firstWhere(
      (h) =>
          h.versionId == versionId &&
          h.bookNumber == book &&
          h.chapter == chapter &&
          h.verse == verse,
    );
    return h.color;
  } catch (_) {
    return null;
  }
}
