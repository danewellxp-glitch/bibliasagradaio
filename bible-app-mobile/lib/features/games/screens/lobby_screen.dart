import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/app_colors.dart';
import '../../auth/providers/auth_provider.dart';
import '../providers/game_provider.dart';

class LobbyScreen extends ConsumerStatefulWidget {
  final String roomCode;

  const LobbyScreen({super.key, required this.roomCode});

  @override
  ConsumerState<LobbyScreen> createState() => _LobbyScreenState();
}

class _LobbyScreenState extends ConsumerState<LobbyScreen> {
  bool _joining = true;
  bool _starting = false;

  @override
  void initState() {
    super.initState();
    _join();
  }

  Future<void> _join() async {
    try {
      final api = ref.read(apiServiceProvider);
      await joinRoom(api, widget.roomCode);
    } catch (_) {
      // Already joined or error - polling will show status
    }
    if (mounted) setState(() => _joining = false);
  }

  Future<void> _startGame() async {
    setState(() => _starting = true);
    try {
      final api = ref.read(apiServiceProvider);
      await startGame(api, widget.roomCode);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro ao iniciar: $e')),
        );
      }
    }
    if (mounted) setState(() => _starting = false);
  }

  @override
  Widget build(BuildContext context) {
    final roomAsync = ref.watch(roomPollingProvider(widget.roomCode));

    return Scaffold(
      appBar: AppBar(
        title: Text('Sala ${widget.roomCode}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.copy),
            tooltip: 'Copiar codigo',
            onPressed: () {
              Clipboard.setData(ClipboardData(text: widget.roomCode));
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Codigo copiado!')),
              );
            },
          ),
        ],
      ),
      body: roomAsync.when(
        data: (room) {
          // If game started, navigate to game screen
          if (room.status == 'playing') {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              context.go('/games/play/${widget.roomCode}');
            });
            return const Center(child: CircularProgressIndicator());
          }
          if (room.status == 'finished') {
            WidgetsBinding.instance.addPostFrameCallback((_) {
              context.go('/games/results/${widget.roomCode}');
            });
            return const Center(child: CircularProgressIndicator());
          }

          final authState = ref.watch(authStateProvider);
          final currentUserId = authState.valueOrNull?.uid ?? '';
          final isCreator = room.createdBy.contains(currentUserId) ||
              room.participants.isNotEmpty &&
                  room.participants.first.userId == currentUserId;

          return Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Room info card
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              widget.roomCode,
                              style: const TextStyle(
                                fontSize: 32,
                                fontWeight: FontWeight.bold,
                                letterSpacing: 4,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Compartilhe este codigo com seus amigos',
                          style: TextStyle(
                              fontSize: 13, color: Colors.grey[600]),
                        ),
                        const SizedBox(height: 12),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                            _InfoChip(
                                label: room.difficulty, icon: Icons.speed),
                            _InfoChip(
                                label: '${room.totalQuestions} perguntas',
                                icon: Icons.quiz),
                            _InfoChip(
                                label: 'Max ${room.maxPlayers}',
                                icon: Icons.people),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 24),

                // Participants
                Text(
                  'Jogadores (${room.participants.length}/${room.maxPlayers})',
                  style: const TextStyle(
                      fontSize: 16, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 12),
                Expanded(
                  child: ListView.builder(
                    itemCount: room.participants.length,
                    itemBuilder: (context, index) {
                      final p = room.participants[index];
                      final isHost = index == 0;
                      return ListTile(
                        leading: CircleAvatar(
                          backgroundColor: isHost
                              ? AppColors.secondary
                              : AppColors.primary.withOpacity(0.2),
                          child: Text(
                            (p.displayName ?? 'J')[0].toUpperCase(),
                            style: TextStyle(
                              color: isHost ? Colors.white : AppColors.primary,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                        title: Text(p.displayName ?? 'Jogador'),
                        trailing: isHost
                            ? Container(
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 8, vertical: 2),
                                decoration: BoxDecoration(
                                  color: AppColors.secondary,
                                  borderRadius: BorderRadius.circular(4),
                                ),
                                child: const Text(
                                  'HOST',
                                  style: TextStyle(
                                    fontSize: 10,
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              )
                            : null,
                      );
                    },
                  ),
                ),

                // Start button (only for creator)
                if (isCreator)
                  FilledButton.icon(
                    onPressed: _starting || room.participants.length < 2
                        ? null
                        : _startGame,
                    icon: _starting
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                                strokeWidth: 2, color: Colors.white),
                          )
                        : const Icon(Icons.play_arrow),
                    label: Text(room.participants.length < 2
                        ? 'Aguardando jogadores...'
                        : _starting
                            ? 'Iniciando...'
                            : 'Iniciar Jogo'),
                    style: FilledButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                  )
                else
                  const Card(
                    child: Padding(
                      padding: EdgeInsets.all(16),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(strokeWidth: 2)),
                          SizedBox(width: 12),
                          Text('Aguardando o host iniciar o jogo...'),
                        ],
                      ),
                    ),
                  ),
              ],
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.error_outline, size: 48, color: Colors.grey),
              const SizedBox(height: 12),
              Text('Sala nao encontrada: $e'),
              const SizedBox(height: 16),
              FilledButton(
                onPressed: () => context.go('/games'),
                child: const Text('Voltar'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _InfoChip extends StatelessWidget {
  final String label;
  final IconData icon;

  const _InfoChip({required this.label, required this.icon});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 14, color: Colors.grey),
        const SizedBox(width: 4),
        Text(label, style: const TextStyle(fontSize: 12)),
      ],
    );
  }
}
