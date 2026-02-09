import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/app_colors.dart';
import '../../auth/providers/auth_provider.dart';
import '../providers/game_provider.dart';

class MultiplayerGameScreen extends ConsumerStatefulWidget {
  final String roomCode;

  const MultiplayerGameScreen({super.key, required this.roomCode});

  @override
  ConsumerState<MultiplayerGameScreen> createState() =>
      _MultiplayerGameScreenState();
}

class _MultiplayerGameScreenState
    extends ConsumerState<MultiplayerGameScreen> {
  GameQuestion? _question;
  GameAnswerResult? _lastResult;
  bool _loading = true;
  bool _submitting = false;
  String? _selectedAnswer;
  int _timeLeft = 30;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _loadQuestion();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  void _startTimer() {
    _timer?.cancel();
    _timeLeft = 30;
    _timer = Timer.periodic(const Duration(seconds: 1), (t) {
      if (_timeLeft <= 0) {
        t.cancel();
        // Auto-submit empty if time runs out
        if (_selectedAnswer == null && _question != null) {
          _submit(_question!.options.first);
        }
      } else {
        setState(() => _timeLeft--);
      }
    });
  }

  Future<void> _loadQuestion() async {
    setState(() {
      _loading = true;
      _lastResult = null;
      _selectedAnswer = null;
    });

    try {
      final api = ref.read(apiServiceProvider);
      final q = await getQuestion(api, widget.roomCode);
      if (mounted) {
        setState(() {
          _question = q;
          _loading = false;
        });
        _startTimer();
      }
    } catch (e) {
      // Game might be finished
      if (mounted) {
        final api = ref.read(apiServiceProvider);
        try {
          final room = await getRoomStatus(api, widget.roomCode);
          if (room.status == 'finished') {
            context.go('/games/results/${widget.roomCode}');
            return;
          }
        } catch (_) {}
        setState(() => _loading = false);
      }
    }
  }

  Future<void> _submit(String answer) async {
    if (_submitting || _question == null) return;
    setState(() {
      _submitting = true;
      _selectedAnswer = answer;
    });
    _timer?.cancel();

    try {
      final api = ref.read(apiServiceProvider);
      final result = await submitAnswer(
        api,
        widget.roomCode,
        questionId: _question!.questionId,
        answer: answer,
        timeTakenSeconds: 30 - _timeLeft,
      );
      if (mounted) {
        setState(() {
          _lastResult = result;
          _submitting = false;
        });

        // Wait 2 seconds then load next question
        await Future.delayed(const Duration(seconds: 2));
        if (mounted) _loadQuestion();
      }
    } catch (e) {
      if (mounted) {
        setState(() => _submitting = false);
        // Check if game is finished
        try {
          final api = ref.read(apiServiceProvider);
          final room = await getRoomStatus(api, widget.roomCode);
          if (room.status == 'finished') {
            context.go('/games/results/${widget.roomCode}');
          }
        } catch (_) {}
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final roomAsync = ref.watch(roomPollingProvider(widget.roomCode));

    return Scaffold(
      appBar: AppBar(
        title: Text('Sala ${widget.roomCode}'),
        automaticallyImplyLeading: false,
        actions: [
          // Timer
          Container(
            margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            decoration: BoxDecoration(
              color: _timeLeft <= 10 ? Colors.red : AppColors.primary,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Row(
              children: [
                const Icon(Icons.timer, size: 16, color: Colors.white),
                const SizedBox(width: 4),
                Text(
                  '${_timeLeft}s',
                  style: const TextStyle(
                      color: Colors.white, fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _question == null
              ? const Center(child: Text('Aguardando proxima pergunta...'))
              : Column(
                  children: [
                    // Scoreboard strip
                    roomAsync.when(
                      data: (room) {
                        // Redirect if finished
                        if (room.status == 'finished') {
                          WidgetsBinding.instance.addPostFrameCallback((_) {
                            context.go('/games/results/${widget.roomCode}');
                          });
                        }
                        return Container(
                          height: 48,
                          color: Colors.grey[100],
                          child: ListView(
                            scrollDirection: Axis.horizontal,
                            padding: const EdgeInsets.symmetric(horizontal: 8),
                            children: room.participants.map((p) {
                              return Padding(
                                padding:
                                    const EdgeInsets.symmetric(horizontal: 6),
                                child: Chip(
                                  avatar: CircleAvatar(
                                    radius: 12,
                                    child: Text(
                                      (p.displayName ?? 'J')[0].toUpperCase(),
                                      style: const TextStyle(fontSize: 10),
                                    ),
                                  ),
                                  label: Text(
                                    '${p.displayName ?? 'Jogador'}: ${p.score}',
                                    style: const TextStyle(fontSize: 12),
                                  ),
                                ),
                              );
                            }).toList(),
                          ),
                        );
                      },
                      loading: () => const SizedBox(height: 48),
                      error: (_, __) => const SizedBox(height: 48),
                    ),

                    // Question info
                    Padding(
                      padding: const EdgeInsets.all(16),
                      child: Text(
                        'Pergunta ${_question!.questionIndex}',
                        style: TextStyle(
                            fontSize: 13, color: Colors.grey[600]),
                      ),
                    ),

                    // Question text
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 24),
                      child: Text(
                        _question!.questionText,
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                    const SizedBox(height: 24),

                    // Options
                    Expanded(
                      child: ListView.builder(
                        padding: const EdgeInsets.symmetric(horizontal: 24),
                        itemCount: _question!.options.length,
                        itemBuilder: (context, index) {
                          final option = _question!.options[index];
                          final isSelected = _selectedAnswer == option;
                          final showResult = _lastResult != null;
                          final isCorrect = showResult &&
                              option == _lastResult!.correctAnswer;
                          final isWrong =
                              showResult && isSelected && !isCorrect;

                          Color? bgColor;
                          if (showResult && isCorrect) {
                            bgColor = Colors.green[50];
                          } else if (isWrong) {
                            bgColor = Colors.red[50];
                          } else if (isSelected) {
                            bgColor = AppColors.primary.withOpacity(0.1);
                          }

                          return Padding(
                            padding: const EdgeInsets.only(bottom: 12),
                            child: Material(
                              color: bgColor ?? Colors.white,
                              borderRadius: BorderRadius.circular(12),
                              elevation: 1,
                              child: InkWell(
                                borderRadius: BorderRadius.circular(12),
                                onTap: _selectedAnswer != null
                                    ? null
                                    : () => _submit(option),
                                child: Padding(
                                  padding: const EdgeInsets.all(16),
                                  child: Row(
                                    children: [
                                      Expanded(
                                        child: Text(
                                          option,
                                          style: TextStyle(
                                            fontSize: 15,
                                            fontWeight: isSelected
                                                ? FontWeight.bold
                                                : FontWeight.normal,
                                          ),
                                        ),
                                      ),
                                      if (showResult && isCorrect)
                                        const Icon(Icons.check_circle,
                                            color: Colors.green),
                                      if (isWrong)
                                        const Icon(Icons.cancel,
                                            color: Colors.red),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          );
                        },
                      ),
                    ),

                    // Result feedback
                    if (_lastResult != null)
                      Container(
                        padding: const EdgeInsets.all(16),
                        color: _lastResult!.isCorrect
                            ? Colors.green[50]
                            : Colors.red[50],
                        child: Row(
                          children: [
                            Icon(
                              _lastResult!.isCorrect
                                  ? Icons.check_circle
                                  : Icons.cancel,
                              color: _lastResult!.isCorrect
                                  ? Colors.green
                                  : Colors.red,
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                _lastResult!.isCorrect
                                    ? '+${_lastResult!.pointsEarned} pontos!'
                                    : 'Resposta: ${_lastResult!.correctAnswer}',
                                style: const TextStyle(
                                    fontWeight: FontWeight.bold),
                              ),
                            ),
                            Text(
                              'Total: ${_lastResult!.totalScore}',
                              style: const TextStyle(
                                  fontWeight: FontWeight.w600),
                            ),
                          ],
                        ),
                      ),
                  ],
                ),
    );
  }
}
