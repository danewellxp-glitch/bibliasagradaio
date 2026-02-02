import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/services/api_service.dart';
import '../../auth/providers/auth_provider.dart';

class QuizQuestionModel {
  final int id;
  final String difficultyLevel;
  final String questionType;
  final String questionText;
  final List<String> options;
  final String? category;

  QuizQuestionModel({
    required this.id,
    required this.difficultyLevel,
    required this.questionType,
    required this.questionText,
    required this.options,
    this.category,
  });

  factory QuizQuestionModel.fromJson(Map<String, dynamic> json) {
    final opts = json['options'] as List<dynamic>? ?? [];
    return QuizQuestionModel(
      id: json['id'] as int,
      difficultyLevel: json['difficulty_level'] as String,
      questionType: json['question_type'] as String,
      questionText: json['question_text'] as String,
      options: opts.map((e) => e.toString()).toList(),
      category: json['category'] as String?,
    );
  }
}

class QuizStatsModel {
  final int totalXp;
  final int currentLevel;
  final int currentStreak;
  final int longestStreak;
  final int totalQuestionsAnswered;
  final int totalCorrectAnswers;

  QuizStatsModel({
    required this.totalXp,
    required this.currentLevel,
    required this.currentStreak,
    required this.longestStreak,
    required this.totalQuestionsAnswered,
    required this.totalCorrectAnswers,
  });

  factory QuizStatsModel.fromJson(Map<String, dynamic> json) =>
      QuizStatsModel(
        totalXp: json['total_xp'] as int? ?? 0,
        currentLevel: json['current_level'] as int? ?? 1,
        currentStreak: json['current_streak'] as int? ?? 0,
        longestStreak: json['longest_streak'] as int? ?? 0,
        totalQuestionsAnswered: json['total_questions_answered'] as int? ?? 0,
        totalCorrectAnswers: json['total_correct_answers'] as int? ?? 0,
      );
}

class LeaderboardEntryModel {
  final int rank;
  final String userId;
  final String? displayName;
  final int totalXp;
  final int currentLevel;

  LeaderboardEntryModel({
    required this.rank,
    required this.userId,
    this.displayName,
    required this.totalXp,
    required this.currentLevel,
  });

  factory LeaderboardEntryModel.fromJson(Map<String, dynamic> json) =>
      LeaderboardEntryModel(
        rank: json['rank'] as int,
        userId: json['user_id'] as String,
        displayName: json['display_name'] as String?,
        totalXp: json['total_xp'] as int,
        currentLevel: json['current_level'] as int,
      );
}

Future<QuizQuestionModel?> fetchNextQuestion(ApiService api) async {
  final res = await api.get('/quiz/next-question');
  return QuizQuestionModel.fromJson(res.data as Map<String, dynamic>);
}

Future<Map<String, dynamic>> submitAnswer(
  ApiService api, {
  required int questionId,
  required String answer,
  int? timeTakenSeconds,
}) async {
  final res = await api.post('/quiz/answer', data: {
    'question_id': questionId,
    'answer': answer,
    'time_taken_seconds': timeTakenSeconds,
  });
  return res.data as Map<String, dynamic>;
}

Future<QuizStatsModel> fetchStats(ApiService api) async {
  final res = await api.get('/quiz/stats');
  return QuizStatsModel.fromJson(res.data as Map<String, dynamic>);
}

Future<List<LeaderboardEntryModel>> fetchLeaderboard(ApiService api,
    {int limit = 50}) async {
  final res = await api.get('/quiz/leaderboard', params: {'limit': limit});
  final list = res.data as List;
  return list
      .map((e) => LeaderboardEntryModel.fromJson(e as Map<String, dynamic>))
      .toList();
}

final quizStatsProvider = FutureProvider<QuizStatsModel>((ref) {
  return fetchStats(ref.read(apiServiceProvider));
});

final leaderboardProvider =
    FutureProvider<List<LeaderboardEntryModel>>((ref) {
  return fetchLeaderboard(ref.read(apiServiceProvider));
});
