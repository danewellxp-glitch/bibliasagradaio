import 'package:dio/dio.dart';
import 'package:firebase_auth/firebase_auth.dart' as fb;
import 'package:google_sign_in/google_sign_in.dart';

import 'api_service.dart';

class AuthService {
  final fb.FirebaseAuth _firebaseAuth = fb.FirebaseAuth.instance;
  final GoogleSignIn _googleSignIn = GoogleSignIn();
  final ApiService _api;

  AuthService(this._api);

  fb.User? get currentUser => _firebaseAuth.currentUser;

  Stream<fb.User?> get authStateChanges => _firebaseAuth.authStateChanges();

  Future<String?> signInWithGoogle() async {
    final googleUser = await _googleSignIn.signIn();
    if (googleUser == null) return null;

    final googleAuth = await googleUser.authentication;
    final credential = fb.GoogleAuthProvider.credential(
      accessToken: googleAuth.accessToken,
      idToken: googleAuth.idToken,
    );

    final userCredential =
        await _firebaseAuth.signInWithCredential(credential);
    final idToken = await userCredential.user?.getIdToken();
    if (idToken == null) return null;

    // Login on backend to get JWT (backend expects Firebase token in Authorization header)
    final response = await _api.post(
      '/auth/login',
      options: Options(
        headers: {'Authorization': 'Bearer $idToken'},
      ),
    );
    final jwt = response.data['access_token'] as String;
    _api.setToken(jwt);
    return jwt;
  }

  Future<void> signOut() async {
    _api.clearToken();
    await _googleSignIn.signOut();
    await _firebaseAuth.signOut();
  }
}
