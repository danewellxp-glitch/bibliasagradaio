class BibleVersion {
  final int id;
  final String code;
  final String name;
  final String language;
  final bool isPremium;

  const BibleVersion({
    required this.id,
    required this.code,
    required this.name,
    required this.language,
    required this.isPremium,
  });

  factory BibleVersion.fromJson(Map<String, dynamic> json) => BibleVersion(
        id: json['id'] as int,
        code: json['code'] as String,
        name: json['name'] as String,
        language: json['language'] as String,
        isPremium: json['is_premium'] as bool,
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'code': code,
        'name': name,
        'language': language,
        'is_premium': isPremium,
      };
}

class Verse {
  final int bookNumber;
  final String bookName;
  final int chapter;
  final int verse;
  final String text;

  const Verse({
    required this.bookNumber,
    required this.bookName,
    required this.chapter,
    required this.verse,
    required this.text,
  });

  factory Verse.fromJson(Map<String, dynamic> json) => Verse(
        bookNumber: json['book_number'] as int,
        bookName: json['book_name'] as String,
        chapter: json['chapter'] as int,
        verse: json['verse'] as int,
        text: json['text'] as String,
      );

  Map<String, dynamic> toJson() => {
        'book_number': bookNumber,
        'book_name': bookName,
        'chapter': chapter,
        'verse': verse,
        'text': text,
      };

  String get reference => '$bookName $chapter:$verse';
}

class Highlight {
  final String? id;
  final int versionId;
  final int bookNumber;
  final int chapter;
  final int verse;
  final String color;
  final DateTime? createdAt;

  const Highlight({
    this.id,
    required this.versionId,
    required this.bookNumber,
    required this.chapter,
    required this.verse,
    required this.color,
    this.createdAt,
  });

  factory Highlight.fromJson(Map<String, dynamic> json) => Highlight(
        id: json['id'] as String?,
        versionId: json['version_id'] as int,
        bookNumber: json['book_number'] as int,
        chapter: json['chapter'] as int,
        verse: json['verse'] as int,
        color: json['color'] as String,
        createdAt: json['created_at'] != null
            ? DateTime.parse(json['created_at'] as String)
            : null,
      );

  Map<String, dynamic> toJson() => {
        'version_id': versionId,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
        'color': color,
      };
}

class Annotation {
  final String? id;
  final int versionId;
  final int bookNumber;
  final int chapter;
  final int verse;
  final String note;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  const Annotation({
    this.id,
    required this.versionId,
    required this.bookNumber,
    required this.chapter,
    required this.verse,
    required this.note,
    this.createdAt,
    this.updatedAt,
  });

  factory Annotation.fromJson(Map<String, dynamic> json) => Annotation(
        id: json['id'] as String?,
        versionId: json['version_id'] as int,
        bookNumber: json['book_number'] as int,
        chapter: json['chapter'] as int,
        verse: json['verse'] as int,
        note: json['note'] as String,
        createdAt: json['created_at'] != null
            ? DateTime.parse(json['created_at'] as String)
            : null,
        updatedAt: json['updated_at'] != null
            ? DateTime.parse(json['updated_at'] as String)
            : null,
      );

  Map<String, dynamic> toJson() => {
        'version_id': versionId,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
        'note': note,
      };
}

class Bookmark {
  final String? id;
  final int versionId;
  final int bookNumber;
  final int chapter;
  final int verse;
  final String? title;
  final DateTime? createdAt;

  const Bookmark({
    this.id,
    required this.versionId,
    required this.bookNumber,
    required this.chapter,
    required this.verse,
    this.title,
    this.createdAt,
  });

  factory Bookmark.fromJson(Map<String, dynamic> json) => Bookmark(
        id: json['id'] as String?,
        versionId: json['version_id'] as int,
        bookNumber: json['book_number'] as int,
        chapter: json['chapter'] as int,
        verse: json['verse'] as int,
        title: json['title'] as String?,
        createdAt: json['created_at'] != null
            ? DateTime.parse(json['created_at'] as String)
            : null,
      );

  Map<String, dynamic> toJson() => {
        'version_id': versionId,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
        'title': title,
      };
}
