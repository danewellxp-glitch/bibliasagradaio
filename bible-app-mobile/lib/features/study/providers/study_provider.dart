import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/services/api_service.dart';
import '../../auth/providers/auth_provider.dart';

// Models from API
class Commentary {
  final int id;
  final String author;
  final int bookNumber;
  final int? chapter;
  final int? verseStart;
  final int? verseEnd;
  final String commentary;
  final String? source;
  final String language;

  Commentary({
    required this.id,
    required this.author,
    required this.bookNumber,
    this.chapter,
    this.verseStart,
    this.verseEnd,
    required this.commentary,
    this.source,
    required this.language,
  });

  factory Commentary.fromJson(Map<String, dynamic> json) => Commentary(
        id: json['id'] as int,
        author: json['author'] as String,
        bookNumber: json['book_number'] as int,
        chapter: json['chapter'] as int?,
        verseStart: json['verse_start'] as int?,
        verseEnd: json['verse_end'] as int?,
        commentary: json['commentary'] as String,
        source: json['source'] as String?,
        language: json['language'] as String,
      );
}

class CrossRef {
  final int id;
  final int fromBook;
  final int fromChapter;
  final int fromVerse;
  final int toBook;
  final int toChapter;
  final int toVerse;
  final String? relationshipType;

  CrossRef({
    required this.id,
    required this.fromBook,
    required this.fromChapter,
    required this.fromVerse,
    required this.toBook,
    required this.toChapter,
    required this.toVerse,
    this.relationshipType,
  });

  factory CrossRef.fromJson(Map<String, dynamic> json) => CrossRef(
        id: json['id'] as int,
        fromBook: json['from_book'] as int,
        fromChapter: json['from_chapter'] as int,
        fromVerse: json['from_verse'] as int,
        toBook: json['to_book'] as int,
        toChapter: json['to_chapter'] as int,
        toVerse: json['to_verse'] as int,
        relationshipType: json['relationship_type'] as String?,
      );

  String get toReference => '$toBook:$toChapter:$toVerse';
}

class TimelineEventModel {
  final int id;
  final String eventName;
  final String? description;
  final String? approximateDate;
  final int? dateStart;
  final int? dateEnd;
  final String? eventType;
  final List<int>? relatedBooks;
  final dynamic relatedVerses;

  TimelineEventModel({
    required this.id,
    required this.eventName,
    this.description,
    this.approximateDate,
    this.dateStart,
    this.dateEnd,
    this.eventType,
    this.relatedBooks,
    this.relatedVerses,
  });

  factory TimelineEventModel.fromJson(Map<String, dynamic> json) =>
      TimelineEventModel(
        id: json['id'] as int,
        eventName: json['event_name'] as String,
        description: json['description'] as String?,
        approximateDate: json['approximate_date'] as String?,
        dateStart: json['date_start'] as int?,
        dateEnd: json['date_end'] as int?,
        eventType: json['event_type'] as String?,
        relatedBooks: (json['related_books'] as List<dynamic>?)
            ?.map((e) => e as int)
            .toList(),
        relatedVerses: json['related_verses'],
      );
}

class BibleMapModel {
  final int id;
  final String title;
  final String? description;
  final String? period;
  final String imageUrl;
  final List<int>? relatedBooks;

  BibleMapModel({
    required this.id,
    required this.title,
    this.description,
    this.period,
    required this.imageUrl,
    this.relatedBooks,
  });

  factory BibleMapModel.fromJson(Map<String, dynamic> json) => BibleMapModel(
        id: json['id'] as int,
        title: json['title'] as String,
        description: json['description'] as String?,
        period: json['period'] as String?,
        imageUrl: json['image_url'] as String,
        relatedBooks: (json['related_books'] as List<dynamic>?)
            ?.map((e) => e as int)
            .toList(),
      );
}

// API calls
Future<List<Commentary>> fetchCommentaries(
  ApiService api, {
  required int book,
  int? chapter,
  int? verse,
}) async {
  final params = <String, dynamic>{'book': book};
  if (chapter != null) params['chapter'] = chapter;
  if (verse != null) params['verse'] = verse;
  final res = await api.get('/study/commentaries', params: params);
  final list = res.data as List;
  return list.map((e) => Commentary.fromJson(e as Map<String, dynamic>)).toList();
}

Future<List<CrossRef>> fetchCrossReferences(
  ApiService api, {
  required int book,
  required int chapter,
  required int verse,
}) async {
  final res = await api.get('/study/cross-references', params: {
    'book': book,
    'chapter': chapter,
    'verse': verse,
  });
  final list = res.data as List;
  return list.map((e) => CrossRef.fromJson(e as Map<String, dynamic>)).toList();
}

Future<List<TimelineEventModel>> fetchTimeline(ApiService api) async {
  final res = await api.get('/study/timeline');
  final list = res.data as List;
  return list
      .map((e) => TimelineEventModel.fromJson(e as Map<String, dynamic>))
      .toList();
}

Future<List<BibleMapModel>> fetchMaps(ApiService api, {String? period}) async {
  final params = period != null ? {'period': period} : null;
  final res = await api.get('/study/maps', params: params);
  final list = res.data as List;
  return list
      .map((e) => BibleMapModel.fromJson(e as Map<String, dynamic>))
      .toList();
}

// Providers
final commentariesProvider = FutureProvider.family<List<Commentary>, ({int book, int? chapter, int? verse})>((ref, params) {
  return fetchCommentaries(
    ref.read(apiServiceProvider),
    book: params.book,
    chapter: params.chapter,
    verse: params.verse,
  );
});

final crossRefsProvider = FutureProvider.family<List<CrossRef>, ({int book, int chapter, int verse})>((ref, params) {
  return fetchCrossReferences(
    ref.read(apiServiceProvider),
    book: params.book,
    chapter: params.chapter,
    verse: params.verse,
  );
});

final timelineProvider = FutureProvider<List<TimelineEventModel>>((ref) {
  return fetchTimeline(ref.read(apiServiceProvider));
});

final mapsProvider = FutureProvider.family<List<BibleMapModel>, String?>((ref, period) {
  return fetchMaps(ref.read(apiServiceProvider), period: period);
});
