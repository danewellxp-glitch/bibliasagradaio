import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/services/api_service.dart';
import '../../auth/providers/auth_provider.dart';

class PremiumStatus {
  final bool isPremium;
  final String plan;
  final String status;
  final DateTime? expiresAt;
  final int aiDailyLimit;

  PremiumStatus({
    required this.isPremium,
    required this.plan,
    required this.status,
    this.expiresAt,
    required this.aiDailyLimit,
  });

  factory PremiumStatus.fromJson(Map<String, dynamic> json) => PremiumStatus(
        isPremium: json['is_premium'] as bool,
        plan: json['plan'] as String,
        status: json['status'] as String,
        expiresAt: json['expires_at'] != null
            ? DateTime.parse(json['expires_at'] as String)
            : null,
        aiDailyLimit: json['ai_daily_limit'] as int,
      );
}

Future<PremiumStatus> fetchPremiumStatus(ApiService api) async {
  final res = await api.get('/premium/status');
  return PremiumStatus.fromJson(res.data as Map<String, dynamic>);
}

Future<Map<String, dynamic>> verifyReceipt(
  ApiService api, {
  required String provider,
  required String purchaseToken,
  required String productId,
}) async {
  final res = await api.post('/premium/verify-receipt', data: {
    'provider': provider,
    'purchase_token': purchaseToken,
    'product_id': productId,
  });
  return res.data as Map<String, dynamic>;
}

final premiumStatusProvider = FutureProvider<PremiumStatus>((ref) {
  return fetchPremiumStatus(ref.read(apiServiceProvider));
});
