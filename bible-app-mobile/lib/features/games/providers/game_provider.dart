import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/services/api_service.dart';
import '../../auth/providers/auth_provider.dart';

// Models
class GameRoom {
  final String roomCode;
  final String roomId;
  final String gameType;
  final String difficulty;
  final String status;
  final int currentQuestion;
  final int totalQuestions;
  final int maxPlayers;
  final String createdBy;
  final List<GameParticipant> participants;

  GameRoom({
    required this.roomCode,
    required this.roomId,
    required this.gameType,
    required this.difficulty,
    required this.status,
    required this.currentQuestion,
    required this.totalQuestions,
    required this.maxPlayers,
    required this.createdBy,
    required this.participants,
  });

  factory GameRoom.fromJson(Map<String, dynamic> json) => GameRoom(
        roomCode: json['room_code'] as String,
        roomId: json['room_id'] as String,
        gameType: json['game_type'] as String,
        difficulty: json['difficulty'] as String,
        status: json['status'] as String? ?? 'waiting',
        currentQuestion: json['current_question'] as int? ?? 0,
        totalQuestions: json['total_questions'] as int? ?? 10,
        maxPlayers: json['max_players'] as int? ?? 10,
        createdBy: json['created_by'] as String? ?? '',
        participants: (json['participants'] as List<dynamic>?)
                ?.map(
                    (e) => GameParticipant.fromJson(e as Map<String, dynamic>))
                .toList() ??
            [],
      );
}

class GameParticipant {
  final String userId;
  final String? displayName;
  final int score;
  final int answersCorrect;
  final int answersTotal;

  GameParticipant({
    required this.userId,
    this.displayName,
    required this.score,
    required this.answersCorrect,
    required this.answersTotal,
  });

  factory GameParticipant.fromJson(Map<String, dynamic> json) =>
      GameParticipant(
        userId: json['user_id'] as String,
        displayName: json['display_name'] as String?,
        score: json['score'] as int? ?? 0,
        answersCorrect: json['answers_correct'] as int? ?? 0,
        answersTotal: json['answers_total'] as int? ?? 0,
      );
}

class GameQuestion {
  final int questionIndex;
  final int questionId;
  final String questionText;
  final List<String> options;
  final String? category;
  final int timeLimitSeconds;

  GameQuestion({
    required this.questionIndex,
    required this.questionId,
    required this.questionText,
    required this.options,
    this.category,
    this.timeLimitSeconds = 30,
  });

  factory GameQuestion.fromJson(Map<String, dynamic> json) => GameQuestion(
        questionIndex: json['question_index'] as int,
        questionId: json['question_id'] as int,
        questionText: json['question_text'] as String,
        options: (json['options'] as List<dynamic>)
            .map((e) => e.toString())
            .toList(),
        category: json['category'] as String?,
        timeLimitSeconds: json['time_limit_seconds'] as int? ?? 30,
      );
}

class GameAnswerResult {
  final bool isCorrect;
  final String correctAnswer;
  final String? explanation;
  final int pointsEarned;
  final int totalScore;

  GameAnswerResult({
    required this.isCorrect,
    required this.correctAnswer,
    this.explanation,
    required this.pointsEarned,
    required this.totalScore,
  });

  factory GameAnswerResult.fromJson(Map<String, dynamic> json) =>
      GameAnswerResult(
        isCorrect: json['is_correct'] as bool,
        correctAnswer: json['correct_answer'] as String,
        explanation: json['explanation'] as String?,
        pointsEarned: json['points_earned'] as int,
        totalScore: json['total_score'] as int,
      );
}

class GameResultEntry {
  final int rank;
  final String userId;
  final String? displayName;
  final int score;
  final int answersCorrect;
  final int answersTotal;
  final int xpEarned;

  GameResultEntry({
    required this.rank,
    required this.userId,
    this.displayName,
    required this.score,
    required this.answersCorrect,
    required this.answersTotal,
    required this.xpEarned,
  });

  factory GameResultEntry.fromJson(Map<String, dynamic> json) =>
      GameResultEntry(
        rank: json['rank'] as int,
        userId: json['user_id'] as String,
        displayName: json['display_name'] as String?,
        score: json['score'] as int,
        answersCorrect: json['answers_correct'] as int,
        answersTotal: json['answers_total'] as int,
        xpEarned: json['xp_earned'] as int,
      );
}

// API calls
Future<GameRoom> createRoom(
  ApiService api, {
  required String gameType,
  required String difficulty,
  int maxPlayers = 10,
  int totalQuestions = 10,
}) async {
  final res = await api.post('/games/room/create', data: {
    'game_type': gameType,
    'difficulty': difficulty,
    'max_players': maxPlayers,
    'total_questions': totalQuestions,
  });
  return GameRoom.fromJson(res.data as Map<String, dynamic>);
}

Future<void> joinRoom(ApiService api, String code,
    {String? displayName}) async {
  await api.post('/games/room/$code/join', data: {
    if (displayName != null) 'display_name': displayName,
  });
}

Future<GameRoom> getRoomStatus(ApiService api, String code) async {
  final res = await api.get('/games/room/$code/status');
  return GameRoom.fromJson(res.data as Map<String, dynamic>);
}

Future<void> startGame(ApiService api, String code) async {
  await api.post('/games/room/$code/start');
}

Future<GameQuestion> getQuestion(ApiService api, String code) async {
  final res = await api.get('/games/room/$code/question');
  return GameQuestion.fromJson(res.data as Map<String, dynamic>);
}

Future<GameAnswerResult> submitAnswer(
  ApiService api,
  String code, {
  required int questionId,
  required String answer,
  int? timeTakenSeconds,
}) async {
  final res = await api.post('/games/room/$code/answer', data: {
    'question_id': questionId,
    'answer': answer,
    'time_taken_seconds': timeTakenSeconds,
  });
  return GameAnswerResult.fromJson(res.data as Map<String, dynamic>);
}

Future<List<GameResultEntry>> getResults(ApiService api, String code) async {
  final res = await api.get('/games/room/$code/results');
  final list = res.data as List;
  return list
      .map((e) => GameResultEntry.fromJson(e as Map<String, dynamic>))
      .toList();
}

// Providers
final currentRoomCodeProvider = StateProvider<String?>((ref) => null);

final roomStatusProvider =
    FutureProvider.family<GameRoom, String>((ref, code) {
  return getRoomStatus(ref.read(apiServiceProvider), code);
});

/// Auto-polling room status every 2 seconds
class RoomPollingNotifier extends StateNotifier<AsyncValue<GameRoom>> {
  final ApiService _api;
  final String _code;
  Timer? _timer;

  RoomPollingNotifier(this._api, this._code)
      : super(const AsyncValue.loading()) {
    _poll();
    _timer = Timer.periodic(const Duration(seconds: 2), (_) => _poll());
  }

  Future<void> _poll() async {
    try {
      final room = await getRoomStatus(_api, _code);
      if (mounted) state = AsyncValue.data(room);
    } catch (e, st) {
      if (mounted) state = AsyncValue.error(e, st);
    }
  }

  void refresh() => _poll();

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}

final roomPollingProvider = StateNotifierProvider.family<RoomPollingNotifier,
    AsyncValue<GameRoom>, String>(
  (ref, code) => RoomPollingNotifier(ref.read(apiServiceProvider), code),
);
