import 'dart:async';

import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sqflite/sqflite.dart';

import '../constants/bible_books.dart';
import '../../data/models/bible_models.dart' show Verse;

/// Service for local SQLite storage of Bible text for offline reading.
/// Tracks which versions are downloaded via SharedPreferences.
class OfflineService {
  static const String _dbName = 'bible_offline.db';
  static const int _dbVersion = 1;
  static const String _tableVerses = 'bible_texts_offline';
  static const String _prefPrefix = 'offline_version_';

  Database? _db;
  SharedPreferences? _prefs;
  final Completer<void> _initCompleter = Completer<void>();

  Future<void> init() async {
    if (_initCompleter.isCompleted) return;
    final dir = await getApplicationDocumentsDirectory();
    final path = join(dir.path, _dbName);
    _db = await openDatabase(
      path,
      version: _dbVersion,
      onCreate: _onCreate,
    );
    _prefs = await SharedPreferences.getInstance();
    _initCompleter.complete();
  }

  Future<void> _onCreate(Database db, int version) async {
    await db.execute('''
      CREATE TABLE $_tableVerses (
        version_code TEXT NOT NULL,
        book_number INTEGER NOT NULL,
        book_name TEXT NOT NULL,
        chapter INTEGER NOT NULL,
        verse INTEGER NOT NULL,
        text TEXT NOT NULL,
        PRIMARY KEY (version_code, book_number, chapter, verse)
      )
    ''');
    await db.execute(
      'CREATE INDEX idx_offline_ref ON $_tableVerses (version_code, book_number, chapter)',
    );
  }

  Future<Database> get _database async {
    if (!_initCompleter.isCompleted) await init();
    return _db!;
  }

  Future<SharedPreferences> get _preferences async {
    if (!_initCompleter.isCompleted) await init();
    return _prefs!;
  }

  /// Whether the given version code is marked as downloaded for offline.
  Future<bool> isVersionDownloaded(String versionCode) async {
    final prefs = await _preferences;
    return prefs.getBool('$_prefPrefix$versionCode') ?? false;
  }

  /// Mark a version as downloaded or not.
  Future<void> setVersionDownloaded(String versionCode, bool downloaded) async {
    final prefs = await _preferences;
    await prefs.setBool('$_prefPrefix$versionCode', downloaded);
  }

  /// List of version codes that are downloaded.
  Future<List<String>> getDownloadedVersionCodes() async {
    final prefs = await _preferences;
    final keys = prefs.getKeys();
    return keys
        .where((k) => k.startsWith(_prefPrefix))
        .map((k) => k.replaceFirst(_prefPrefix, ''))
        .where((code) => prefs.getBool('$_prefPrefix$code') == true)
        .toList();
  }

  /// Get verses for a chapter from local storage. Returns empty list if not found.
  Future<List<Verse>> getChapter(
    String versionCode,
    int bookNumber,
    int chapter,
  ) async {
    final db = await _database;
    final rows = await db.query(
      _tableVerses,
      where:
          'version_code = ? AND book_number = ? AND chapter = ?',
      whereArgs: [versionCode, bookNumber, chapter],
      orderBy: 'verse ASC',
    );
    return rows.map(_rowToVerse).toList();
  }

  static Verse _rowToVerse(Map<String, dynamic> row) {
    return Verse(
      bookNumber: row['book_number'] as int,
      bookName: row['book_name'] as String,
      chapter: row['chapter'] as int,
      verse: row['verse'] as int,
      text: row['text'] as String,
    );
  }

  /// Insert verses for a chapter. Used during download.
  Future<void> insertVerses(
    String versionCode,
    int bookNumber,
    String bookName,
    int chapter,
    List<Verse> verses,
  ) async {
    if (verses.isEmpty) return;
    final db = await _database;
    final batch = db.batch();
    for (final v in verses) {
      batch.insert(
        _tableVerses,
        {
          'version_code': versionCode,
          'book_number': bookNumber,
          'book_name': bookName,
          'chapter': chapter,
          'verse': v.verse,
          'text': v.text,
        },
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    }
    await batch.commit(noResult: true);
  }

  /// Remove all stored data for a version (e.g. to free space).
  Future<void> removeVersion(String versionCode) async {
    final db = await _database;
    await db.delete(
      _tableVerses,
      where: 'version_code = ?',
      whereArgs: [versionCode],
    );
    await setVersionDownloaded(versionCode, false);
  }

  /// Total number of chapters in the Bible (for download progress).
  static int get totalChapters {
    return bibleBooks.fold<int>(
      0,
      (sum, book) => sum + book.chapters,
    );
  }

  /// Close the database (e.g. on logout or app dispose).
  Future<void> close() async {
    if (_db != null && _db!.isOpen) {
      await _db!.close();
      _db = null;
    }
  }
}
