import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/services/api_service.dart';
import '../../auth/providers/auth_provider.dart';

class ReadingStatsModel {
  final int chaptersRead;
  final int chaptersCompleted;
  final int highlightsCount;
  final int annotationsCount;
  final int bookmarksCount;

  ReadingStatsModel({
    required this.chaptersRead,
    required this.chaptersCompleted,
    required this.highlightsCount,
    required this.annotationsCount,
    required this.bookmarksCount,
  });

  factory ReadingStatsModel.fromJson(Map<String, dynamic> json) =>
      ReadingStatsModel(
        chaptersRead: json['chapters_read'] as int? ?? 0,
        chaptersCompleted: json['chapters_completed'] as int? ?? 0,
        highlightsCount: json['highlights_count'] as int? ?? 0,
        annotationsCount: json['annotations_count'] as int? ?? 0,
        bookmarksCount: json['bookmarks_count'] as int? ?? 0,
      );
}

class SettingsModel {
  final int fontSize;
  final String fontFamily;
  final double lineHeight;
  final String theme;
  final bool showVerseNumbers;
  final bool showRedLetters;
  final String defaultVersion;
  final String language;

  SettingsModel({
    required this.fontSize,
    required this.fontFamily,
    required this.lineHeight,
    required this.theme,
    required this.showVerseNumbers,
    required this.showRedLetters,
    required this.defaultVersion,
    required this.language,
  });

  factory SettingsModel.fromJson(Map<String, dynamic> json) => SettingsModel(
        fontSize: json['fontSize'] as int? ?? 16,
        fontFamily: json['fontFamily'] as String? ?? 'Georgia',
        lineHeight: (json['lineHeight'] as num?)?.toDouble() ?? 1.5,
        theme: json['theme'] as String? ?? 'light',
        showVerseNumbers: json['showVerseNumbers'] as bool? ?? true,
        showRedLetters: json['showRedLetters'] as bool? ?? true,
        defaultVersion: json['defaultVersion'] as String? ?? 'ARA',
        language: json['language'] as String? ?? 'pt-BR',
      );

  Map<String, dynamic> toJson() => {
        'fontSize': fontSize,
        'fontFamily': fontFamily,
        'lineHeight': lineHeight,
        'theme': theme,
        'showVerseNumbers': showVerseNumbers,
        'showRedLetters': showRedLetters,
        'defaultVersion': defaultVersion,
        'language': language,
      };
}

Future<ReadingStatsModel> fetchReadingStats(ApiService api) async {
  final res = await api.get('/profile/reading-stats');
  return ReadingStatsModel.fromJson(res.data as Map<String, dynamic>);
}

Future<SettingsModel> fetchSettings(ApiService api) async {
  final res = await api.get('/profile/settings');
  return SettingsModel.fromJson(res.data as Map<String, dynamic>);
}

Future<SettingsModel> putSettings(ApiService api, Map<String, dynamic> prefs) async {
  final res = await api.put('/profile/settings', data: prefs);
  return SettingsModel.fromJson(res.data as Map<String, dynamic>);
}

final readingStatsProvider = FutureProvider<ReadingStatsModel>((ref) {
  return fetchReadingStats(ref.read(apiServiceProvider));
});

final profileSettingsProvider = FutureProvider<SettingsModel>((ref) {
  return fetchSettings(ref.read(apiServiceProvider));
});
