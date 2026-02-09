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

// Lexicon models
class LexiconEntry {
  final int id;
  final String strongNumber;
  final String language;
  final String? originalWord;
  final String? transliteration;
  final String? pronunciation;
  final String? basicMeaning;
  final String? extendedDefinition;
  final int? usageCount;
  final String? firstOccurrence;

  LexiconEntry({
    required this.id,
    required this.strongNumber,
    required this.language,
    this.originalWord,
    this.transliteration,
    this.pronunciation,
    this.basicMeaning,
    this.extendedDefinition,
    this.usageCount,
    this.firstOccurrence,
  });

  factory LexiconEntry.fromJson(Map<String, dynamic> json) => LexiconEntry(
        id: json['id'] as int,
        strongNumber: json['strong_number'] as String,
        language: json['language'] as String,
        originalWord: json['original_word'] as String?,
        transliteration: json['transliteration'] as String?,
        pronunciation: json['pronunciation'] as String?,
        basicMeaning: json['basic_meaning'] as String?,
        extendedDefinition: json['extended_definition'] as String?,
        usageCount: json['usage_count'] as int?,
        firstOccurrence: json['first_occurrence'] as String?,
      );
}

class WordOccurrence {
  final int id;
  final int lexiconEntryId;
  final int bookNumber;
  final int chapter;
  final int verse;
  final int? wordPosition;
  final String? wordInVerse;

  WordOccurrence({
    required this.id,
    required this.lexiconEntryId,
    required this.bookNumber,
    required this.chapter,
    required this.verse,
    this.wordPosition,
    this.wordInVerse,
  });

  factory WordOccurrence.fromJson(Map<String, dynamic> json) => WordOccurrence(
        id: json['id'] as int,
        lexiconEntryId: json['lexicon_entry_id'] as int,
        bookNumber: json['book_number'] as int,
        chapter: json['chapter'] as int,
        verse: json['verse'] as int,
        wordPosition: json['word_position'] as int?,
        wordInVerse: json['word_in_verse'] as String?,
      );
}

class LexiconDetail {
  final LexiconEntry entry;
  final List<WordOccurrence> occurrences;

  LexiconDetail({required this.entry, required this.occurrences});

  factory LexiconDetail.fromJson(Map<String, dynamic> json) => LexiconDetail(
        entry: LexiconEntry.fromJson(json['entry'] as Map<String, dynamic>),
        occurrences: (json['occurrences'] as List)
            .map((e) => WordOccurrence.fromJson(e as Map<String, dynamic>))
            .toList(),
      );
}

class VerseContext {
  final String version;
  final int book;
  final int chapter;
  final int verse;
  final List<Commentary> commentaries;
  final List<CrossRef> crossReferences;
  final List<TimelineEventModel> timelineEvents;

  VerseContext({
    required this.version,
    required this.book,
    required this.chapter,
    required this.verse,
    required this.commentaries,
    required this.crossReferences,
    required this.timelineEvents,
  });

  factory VerseContext.fromJson(Map<String, dynamic> json) => VerseContext(
        version: json['version'] as String,
        book: json['book'] as int,
        chapter: json['chapter'] as int,
        verse: json['verse'] as int,
        commentaries: (json['commentaries'] as List)
            .map((e) => Commentary.fromJson(e as Map<String, dynamic>))
            .toList(),
        crossReferences: (json['cross_references'] as List)
            .map((e) => CrossRef.fromJson(e as Map<String, dynamic>))
            .toList(),
        timelineEvents: (json['timeline_events'] as List)
            .map((e) => TimelineEventModel.fromJson(e as Map<String, dynamic>))
            .toList(),
      );
}

// Lexicon API calls
Future<LexiconDetail> fetchLexiconEntry(
  ApiService api,
  String strongNumber,
) async {
  final res = await api.get('/study/lexicon/$strongNumber');
  return LexiconDetail.fromJson(res.data as Map<String, dynamic>);
}

Future<List<LexiconEntry>> searchLexicon(
  ApiService api,
  String query,
) async {
  final res = await api.get('/study/lexicon/search/', params: {'q': query});
  final list = res.data as List;
  return list.map((e) => LexiconEntry.fromJson(e as Map<String, dynamic>)).toList();
}

Future<VerseContext> fetchVerseContext(
  ApiService api, {
  required String version,
  required int book,
  required int chapter,
  required int verse,
}) async {
  final res = await api.get('/study/verse-context/$version/$book/$chapter/$verse');
  return VerseContext.fromJson(res.data as Map<String, dynamic>);
}

// Providers
final lexiconProvider = FutureProvider.family<LexiconDetail, String>((ref, strongNumber) {
  return fetchLexiconEntry(ref.read(apiServiceProvider), strongNumber);
});

final lexiconSearchProvider = FutureProvider.family<List<LexiconEntry>, String>((ref, query) {
  return searchLexicon(ref.read(apiServiceProvider), query);
});

final verseContextProvider = FutureProvider.family<VerseContext, ({String version, int book, int chapter, int verse})>((ref, params) {
  return fetchVerseContext(
    ref.read(apiServiceProvider),
    version: params.version,
    book: params.book,
    chapter: params.chapter,
    verse: params.verse,
  );
});

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

// AI verse-ask
class VerseAskResponse {
  final String answer;
  final bool fromCache;
  final int remainingQuestions;

  VerseAskResponse({
    required this.answer,
    required this.fromCache,
    required this.remainingQuestions,
  });

  factory VerseAskResponse.fromJson(Map<String, dynamic> json) =>
      VerseAskResponse(
        answer: json['answer'] as String,
        fromCache: json['from_cache'] as bool,
        remainingQuestions: json['remaining_questions'] as int,
      );
}

Future<VerseAskResponse> askAboutVerse(
  ApiService api, {
  required String version,
  required int book,
  required int chapter,
  required int verse,
  required String question,
}) async {
  final res = await api.post('/study/verse-ask', data: {
    'version': version,
    'book': book,
    'chapter': chapter,
    'verse': verse,
    'question': question,
  });
  return VerseAskResponse.fromJson(res.data as Map<String, dynamic>);
}
