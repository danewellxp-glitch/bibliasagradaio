# Análise de Código - Pré Sprint 6

## Objetivo
Verificar se o código não é mock/falso e se botões e funções estão realmente implementados e funcionais.

---

## Problemas críticos (quebram o app)

### 1. **Autenticação: Firebase token não enviado ao backend**

**Local:** `bible-app-mobile/lib/core/services/auth_service.dart`

**Problema:** O Flutter chama `_api.post('/auth/login')` **sem enviar o token do Firebase**. O backend espera `Authorization: Bearer <firebase_id_token>` no header.

**Impacto:** Login falha sempre - backend retorna 401 (não recebe token) ou erro.

**Correção:** Enviar o idToken no header:
```dart
final response = await _api.post(
  '/auth/login',
  headers: {'Authorization': 'Bearer $idToken'},
);
```

---

### 2. **Firebase não inicializado no app**

**Local:** `bible-app-mobile/lib/main.dart`

**Problema:** `Firebase.initializeApp()` nunca é chamado. Firebase Auth, Analytics etc. dependem disso.

**Impacto:** App pode crashar ao usar Firebase Auth (login com Google).

**Correção:** Chamar `await Firebase.initializeApp()` antes de `runApp()`. Requer `firebase_options.dart` (gerado por `flutterfire configure`).

---

### 3. **SyncService usa paths incorretos**

**Local:** `bible-app-mobile/lib/core/services/sync_service.dart`

**Problema:** Chama `/user-content/highlights`, `/user-content/annotations` etc. O backend expõe `/highlights`, `/annotations` (sem prefixo user-content).

**Impacto:** Sync falha - endpoints 404.

**Correção:** Trocar para `/highlights`, `/annotations`, `/bookmarks`.

---

### 4. **get_current_user: comparação UUID com string**

**Local:** `bible-app-backend/app/core/security.py`

**Problema:** `User.id == payload["sub"]` - User.id é UUID, payload["sub"] é string. Em alguns drivers pode falhar.

**Correção:** Usar `User.id == uuid.UUID(payload["sub"])` ou garantir coerção.

---

## Problemas médios

### 5. **SyncService nunca é chamado**

**Local:** `bible-app-mobile/lib/main.dart`, `app_router.dart`

**Problema:** `syncOnAppStart()` existe mas não é invocado em lugar nenhum.

**Impacto:** Sincronização não roda ao abrir o app.

**Correção:** Chamar sync após login ou no primeiro build do app (quando usuário logado).

---

### 6. **ApiService baseUrl fixa para emulador Android**

**Local:** `bible-app-mobile/lib/core/services/api_service.dart`

**Problema:** baseUrl é `http://10.0.2.2:8000/api/v1` - funciona só no emulador Android. iOS e dispositivo real precisam de IP/host diferente.

**Recomendação:** Usar variável de ambiente ou config para diferentes ambientes.

---

### 7. **Sermons "Me avisar" não persiste**

**Local:** `bible-app-mobile/lib/features/sermons/screens/sermons_screen.dart`

**Problema:** O switch "Me avisar quando lancar" só mostra SnackBar - não salva em lugar nenhum (nem local, nem API).

**Impacto:** Funcionalidade é placebo - não faz nada real.

---

## Código verificado como correto

| Componente | Status |
|------------|--------|
| Bible API (get chapter, verses, search) | OK - usa PostgreSQL real |
| User Content API (highlights, annotations, bookmarks) | OK - CRUD real |
| Quiz API (next question, answer, stats, leaderboard) | OK - usa PostgreSQL |
| Study API (commentaries, cross-refs, timeline, maps) | OK - usa PostgreSQL |
| Profile API (reading-stats, quiz-stats, settings) | OK - PostgreSQL + MongoDB |
| Offline service (SQLite) | OK - implementação real |
| Share verse (texto + imagem) | OK - share_plus + screenshot |
| Botões no leitor (highlight, anotar, favoritar, compartilhar) | OK - chamam APIs |
| Download offline | OK - baixa da API e salva SQLite |
| Quiz play flow | OK - fetch question, submit answer, mostra resultado |

---

## Resumo de correções

### Corrigido
1. **auth_service.dart** – Firebase token agora é enviado no header `Authorization: Bearer <idToken>` no POST /auth/login
2. **main.dart** – `Firebase.initializeApp()` adicionado (requer google-services.json / GoogleService-Info.plist)
3. **SyncService** – Paths corrigidos: `/highlights`, `/annotations`, `/bookmarks` (removido prefixo user-content)
4. **security.py** – `get_current_user` passa a converter `payload["sub"]` para UUID antes da comparação

### Pendente (opcional)
5. Integrar `syncOnAppStart` no fluxo do app (após login ou no primeiro build)
6. Sermons: persistir preferência "me avisar" em SharedPreferences ou API
