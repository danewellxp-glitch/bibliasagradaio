import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/theme/app_colors.dart';
import '../providers/premium_provider.dart';

class PremiumScreen extends ConsumerWidget {
  const PremiumScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final statusAsync = ref.watch(premiumStatusProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Premium')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Header
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [AppColors.secondary, AppColors.secondaryDark],
                ),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                children: [
                  const Icon(Icons.workspace_premium,
                      size: 48, color: Colors.white),
                  const SizedBox(height: 12),
                  const Text(
                    'Biblia Sagrada Premium',
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 8),
                  statusAsync.when(
                    data: (status) => status.isPremium
                        ? Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 12, vertical: 4),
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.2),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              'Plano ${status.plan} ativo',
                              style: const TextStyle(color: Colors.white),
                            ),
                          )
                        : const Text(
                            'Desbloqueie todas as ferramentas',
                            style: TextStyle(
                                color: Colors.white70, fontSize: 14),
                          ),
                    loading: () => const SizedBox.shrink(),
                    error: (_, __) => const SizedBox.shrink(),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Comparison table
            const Text(
              'Compare os planos',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),

            _ComparisonRow(
              feature: 'Leitura da Biblia',
              free: true,
              premium: true,
            ),
            _ComparisonRow(
              feature: 'Quiz Solo',
              free: true,
              premium: true,
            ),
            _ComparisonRow(
              feature: 'Multiplayer',
              free: true,
              premium: true,
            ),
            _ComparisonRow(
              feature: 'Comentarios e Refs',
              free: true,
              premium: true,
            ),
            _ComparisonRow(
              feature: 'Lexico Strong\'s',
              free: true,
              premium: true,
            ),
            _ComparisonRow(
              feature: 'Perguntas IA',
              freeText: '3/dia',
              premiumText: '100/dia',
            ),
            _ComparisonRow(
              feature: 'Download offline',
              freeText: '1 versao',
              premiumText: 'Todas',
            ),
            _ComparisonRow(
              feature: 'Sem anuncios',
              free: false,
              premium: true,
            ),
            _ComparisonRow(
              feature: 'Modos exclusivos',
              free: false,
              premium: true,
            ),
            const SizedBox(height: 32),

            // Pricing
            _PlanCard(
              title: 'Mensal',
              price: 'R\$ 9,90/mes',
              productId: 'monthly_premium',
              onSubscribe: () => _subscribe(context, ref, 'monthly_premium'),
            ),
            const SizedBox(height: 12),
            _PlanCard(
              title: 'Anual',
              price: 'R\$ 79,90/ano',
              productId: 'annual_premium',
              badge: 'Economia de 33%',
              onSubscribe: () => _subscribe(context, ref, 'annual_premium'),
            ),
          ],
        ),
      ),
    );
  }

  void _subscribe(BuildContext context, WidgetRef ref, String productId) {
    // TODO: Integrate with in_app_purchase package
    // For now, show a placeholder dialog
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Em breve'),
        content: const Text(
          'A compra via Google Play/App Store sera integrada em breve. '
          'Fique atento as atualizacoes!',
        ),
        actions: [
          FilledButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}

class _ComparisonRow extends StatelessWidget {
  final String feature;
  final bool? free;
  final bool? premium;
  final String? freeText;
  final String? premiumText;

  const _ComparisonRow({
    required this.feature,
    this.free,
    this.premium,
    this.freeText,
    this.premiumText,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Expanded(
            flex: 3,
            child: Text(feature, style: const TextStyle(fontSize: 14)),
          ),
          Expanded(
            flex: 2,
            child: Center(
              child: freeText != null
                  ? Text(freeText!,
                      style: TextStyle(fontSize: 12, color: Colors.grey[600]))
                  : Icon(
                      free == true ? Icons.check_circle : Icons.cancel,
                      color: free == true ? Colors.green : Colors.red[300],
                      size: 20,
                    ),
            ),
          ),
          Expanded(
            flex: 2,
            child: Center(
              child: premiumText != null
                  ? Text(premiumText!,
                      style: const TextStyle(
                          fontSize: 12,
                          color: AppColors.secondary,
                          fontWeight: FontWeight.bold))
                  : Icon(
                      premium == true ? Icons.check_circle : Icons.cancel,
                      color: premium == true
                          ? AppColors.secondary
                          : Colors.red[300],
                      size: 20,
                    ),
            ),
          ),
        ],
      ),
    );
  }
}

class _PlanCard extends StatelessWidget {
  final String title;
  final String price;
  final String productId;
  final String? badge;
  final VoidCallback onSubscribe;

  const _PlanCard({
    required this.title,
    required this.price,
    required this.productId,
    this.badge,
    required this.onSubscribe,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: badge != null ? 4 : 1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: badge != null
            ? const BorderSide(color: AppColors.secondary, width: 2)
            : BorderSide.none,
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Text(
                        title,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (badge != null) ...[
                        const SizedBox(width: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 8, vertical: 2),
                          decoration: BoxDecoration(
                            color: AppColors.secondary,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            badge!,
                            style: const TextStyle(
                              fontSize: 10,
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text(
                    price,
                    style: TextStyle(fontSize: 14, color: Colors.grey[600]),
                  ),
                ],
              ),
            ),
            FilledButton(
              onPressed: onSubscribe,
              style: FilledButton.styleFrom(
                backgroundColor: AppColors.secondary,
              ),
              child: const Text('Assinar'),
            ),
          ],
        ),
      ),
    );
  }
}
