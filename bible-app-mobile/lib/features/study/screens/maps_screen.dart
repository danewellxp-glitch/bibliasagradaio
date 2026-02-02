import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/study_provider.dart';

class MapsScreen extends ConsumerWidget {
  const MapsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final async = ref.watch(mapsProvider(null));

    return Scaffold(
      appBar: AppBar(title: const Text('Mapas')),
      body: async.when(
        data: (list) {
          if (list.isEmpty) {
            return const Center(
              child: Text('Nenhum mapa disponivel.'),
            );
          }
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: list.length,
            itemBuilder: (_, i) {
              final m = list[i];
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (m.imageUrl.isNotEmpty)
                      Image.network(
                        m.imageUrl,
                        height: 160,
                        width: double.infinity,
                        fit: BoxFit.cover,
                        errorBuilder: (_, __, ___) => Container(
                          height: 160,
                          color: Colors.grey[300],
                          child: const Icon(Icons.map, size: 48),
                        ),
                      ),
                    Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            m.title,
                            style: Theme.of(context).textTheme.titleMedium,
                          ),
                          if (m.period != null)
                            Text(
                              m.period!,
                              style: Theme.of(context).textTheme.bodySmall,
                            ),
                          if (m.description != null) ...[
                            const SizedBox(height: 8),
                            Text(m.description!),
                          ],
                        ],
                      ),
                    ),
                  ],
                ),
              );
            },
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Erro: $e'),
              ElevatedButton(
                onPressed: () => ref.invalidate(mapsProvider(null)),
                child: const Text('Tentar novamente'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
