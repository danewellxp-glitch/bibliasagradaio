import 'package:firebase_auth/firebase_auth.dart' as fb;
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/services/api_service.dart';
import '../../../core/services/auth_service.dart';
import '../../../core/services/sync_service.dart';

final apiServiceProvider = Provider<ApiService>((ref) => ApiService());

final authServiceProvider = Provider<AuthService>((ref) {
  return AuthService(ref.read(apiServiceProvider));
});

final syncServiceProvider = Provider<SyncService>((ref) {
  return SyncService(ref.read(apiServiceProvider));
});

final authStateProvider = StreamProvider<fb.User?>((ref) {
  return ref.read(authServiceProvider).authStateChanges;
});
