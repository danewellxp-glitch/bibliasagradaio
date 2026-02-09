import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../auth/providers/auth_provider.dart';
import '../providers/game_provider.dart';

class CreateRoomScreen extends ConsumerStatefulWidget {
  const CreateRoomScreen({super.key});

  @override
  ConsumerState<CreateRoomScreen> createState() => _CreateRoomScreenState();
}

class _CreateRoomScreenState extends ConsumerState<CreateRoomScreen> {
  String _difficulty = 'beginner';
  int _totalQuestions = 10;
  int _maxPlayers = 10;
  bool _loading = false;

  Future<void> _create() async {
    setState(() => _loading = true);
    try {
      final api = ref.read(apiServiceProvider);
      final room = await createRoom(
        api,
        gameType: 'quiz',
        difficulty: _difficulty,
        maxPlayers: _maxPlayers,
        totalQuestions: _totalQuestions,
      );
      if (mounted) {
        context.go('/games/lobby/${room.roomCode}');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro ao criar sala: $e')),
        );
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Criar Sala')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Configurar Partida',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 24),

            // Difficulty
            const Text('Dificuldade',
                style: TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            SegmentedButton<String>(
              segments: const [
                ButtonSegment(value: 'beginner', label: Text('Facil')),
                ButtonSegment(
                    value: 'intermediate', label: Text('Medio')),
                ButtonSegment(value: 'advanced', label: Text('Dificil')),
              ],
              selected: {_difficulty},
              onSelectionChanged: (v) =>
                  setState(() => _difficulty = v.first),
            ),
            const SizedBox(height: 24),

            // Total questions
            const Text('Numero de Perguntas',
                style: TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            Slider(
              value: _totalQuestions.toDouble(),
              min: 5,
              max: 30,
              divisions: 5,
              label: '$_totalQuestions',
              onChanged: (v) =>
                  setState(() => _totalQuestions = v.round()),
            ),
            Text('$_totalQuestions perguntas',
                textAlign: TextAlign.center),
            const SizedBox(height: 24),

            // Max players
            const Text('Maximo de Jogadores',
                style: TextStyle(fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            Slider(
              value: _maxPlayers.toDouble(),
              min: 2,
              max: 20,
              divisions: 18,
              label: '$_maxPlayers',
              onChanged: (v) =>
                  setState(() => _maxPlayers = v.round()),
            ),
            Text('$_maxPlayers jogadores', textAlign: TextAlign.center),
            const SizedBox(height: 32),

            // Create button
            FilledButton.icon(
              onPressed: _loading ? null : _create,
              icon: _loading
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                          strokeWidth: 2, color: Colors.white),
                    )
                  : const Icon(Icons.add),
              label: Text(_loading ? 'Criando...' : 'Criar Sala'),
              style: FilledButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
