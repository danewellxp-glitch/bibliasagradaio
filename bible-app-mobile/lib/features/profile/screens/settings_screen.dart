import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../auth/providers/auth_provider.dart';
import '../../bible/providers/bible_provider.dart';
import '../providers/profile_provider.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  bool _loading = false;

  @override
  Widget build(BuildContext context) {
    final async = ref.watch(profileSettingsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Configuracoes'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.pop(),
        ),
      ),
      body: async.when(
        data: (settings) => SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              DropdownButtonFormField<String>(
                value: settings.theme,
                decoration: const InputDecoration(labelText: 'Tema'),
                items: const [
                  DropdownMenuItem(value: 'light', child: Text('Claro')),
                  DropdownMenuItem(value: 'dark', child: Text('Escuro')),
                  DropdownMenuItem(value: 'sepia', child: Text('Sepia')),
                ],
                onChanged: _loading
                    ? null
                    : (v) => _updateSettings(context, ref, {'theme': v}),
              ),
              const SizedBox(height: 16),
              Slider(
                value: settings.fontSize.toDouble(),
                min: 12,
                max: 24,
                divisions: 12,
                label: 'Tamanho: ${settings.fontSize}',
                onChanged: _loading
                    ? null
                    : (v) => _updateSettings(context, ref, {'fontSize': v.toInt()}),
              ),
              const SizedBox(height: 16),
              SwitchListTile(
                title: const Text('Mostrar numeros dos versiculos'),
                value: settings.showVerseNumbers,
                onChanged: _loading
                    ? null
                    : (v) =>
                        _updateSettings(context, ref, {'showVerseNumbers': v}),
              ),
              SwitchListTile(
                title: const Text('Palavras de Jesus em vermelho'),
                value: settings.showRedLetters,
                onChanged: _loading
                    ? null
                    : (v) =>
                        _updateSettings(context, ref, {'showRedLetters': v}),
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                value: settings.defaultVersion,
                decoration: const InputDecoration(labelText: 'Versao padrao'),
                items: const [
                  DropdownMenuItem(value: 'NVI', child: Text('NVI')),
                  DropdownMenuItem(value: 'ARC', child: Text('ARC')),
                  DropdownMenuItem(value: 'ACF', child: Text('ACF')),
                  DropdownMenuItem(value: 'KJV', child: Text('KJV')),
                ],
                onChanged: _loading
                    ? null
                    : (v) => _updateSettings(context, ref, {'defaultVersion': v}),
              ),
            ],
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Erro: $e'),
              ElevatedButton(
                onPressed: () => ref.invalidate(profileSettingsProvider),
                child: const Text('Tentar novamente'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Future<void> _updateSettings(
    BuildContext context,
    WidgetRef ref,
    Map<String, dynamic> updates,
  ) async {
    setState(() => _loading = true);
    try {
      final api = ref.read(apiServiceProvider);
      final current = ref.read(profileSettingsProvider).valueOrNull;
      if (current == null) return;
      final prefs = current.toJson()..addAll(updates);
      await putSettings(api, prefs);
      ref.invalidate(profileSettingsProvider);
      if ('defaultVersion' == updates.keys.first || updates.containsKey('defaultVersion')) {
        ref.read(selectedVersionProvider.notifier).state =
            updates['defaultVersion'] as String;
      }
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Configuracoes salvas')),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro: $e')),
        );
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }
}
