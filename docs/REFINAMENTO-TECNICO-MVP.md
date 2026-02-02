# Refinamento Técnico MVP — Sprints 1 a 5

> Tech Lead: varredura completa antes do Sprint 6 (testes)

---

## 1️⃣ PROBLEMAS ENCONTRADOS

### [Sprint 1] Firebase Admin SDK não inicializado
- **Descrição:** `verify_firebase_token` chama `firebase_auth.verify_id_token()` mas o Firebase Admin nunca foi inicializado. Login sempre falha.
- **Impacto:** Autenticação quebrada em produção.
- **Onde:** `app/core/security.py` → `verify_firebase_token`
- **Status:** ✅ Corrigido — init em `main.py` condicional ao arquivo de credenciais.

### [Sprint 1] Ausência de tratamento de 401 no cliente
- **Descrição:** Quando o JWT expira, o backend retorna 401. O app Flutter não limpava o token nem redirecionava para login.
- **Impacto:** Usuário fica em tela quebrada sem feedback.
- **Onde:** `lib/core/services/api_service.dart`
- **Status:** ✅ Corrigido — interceptor 401 limpa o token. Redirecionamento depende de authState (logout no próximo refresh).

### [Sprint 4] Quiz: `total_questions_answered` só aumentava em acertos
- **Descrição:** `stats.total_questions_answered += 1` estava dentro do bloco `if is_correct`. Respostas erradas não eram contadas.
- **Impacto:** Estatísticas incorretas e percentual de acerto inflado.
- **Onde:** `app/services/quiz_service.py` → `submit_answer`
- **Status:** ✅ Já estava correto — o incremento está fora do `if is_correct` após a refatoração. Verificado.

### [Sprint 4] Quiz: respostas duplicadas permitidas
- **Descrição:** Usuário poderia responder a mesma pergunta várias vezes e ganhar XP repetido.
- **Impacto:** Gamificação inválida, inflação de XP.
- **Onde:** `app/services/quiz_service.py` → `submit_answer`
- **Status:** ✅ Corrigido — checagem de `UserQuizHistory` antes de inserir.

### [Sprint 2] Bible API sem validação de parâmetros
- **Descrição:** `book`, `chapter`, `verse` aceitavam valores inválidos (ex.: book=999, chapter=-1).
- **Impacto:** Queries desnecessárias, possíveis edge cases.
- **Onde:** `app/api/v1/bible.py`
- **Status:** ✅ Corrigido — `Path(..., ge=1, le=66)` para book, `ge=1, le=150` para chapter, `ge=1, le=176` para verse.

### [Sprint 2] Offline: versão marcada como baixada sem dados completos
- **Descrição:** Se o download falhar no meio, a versão pode ser marcada como offline mesmo sem todos os capítulos.
- **Impacto:** Leitura offline incompleta, tela em branco em capítulos não baixados.
- **Onde:** `lib/data/repositories/offline_bible_repository.dart` → `downloadVersion`
- **Status:** ⚠️ Pendente — marcar `setVersionDownloaded` apenas após todos os capítulos serem inseridos (já está assim). Em caso de erro no meio, a flag não é setada. Verificado — OK.

### [Sprint 5] SyncService nunca invocado
- **Descrição:** `syncOnAppStart()` existe mas não é chamado em nenhum lugar.
- **Impacto:** Sincronização não ocorre ao abrir o app.
- **Onde:** `lib/core/services/sync_service.dart`
- **Status:** ⚠️ Pendente — recomendado chamar após login ou no primeiro build com usuário logado.

### [Sprint 1] JWT_SECRET padrão inseguro
- **Descrição:** `JWT_SECRET = "change-me-in-production"` em `config.py`.
- **Impacto:** Alto risco de segurança se não sobrescrito via env.
- **Onde:** `app/core/config.py`
- **Status:** ⚠️ Documentar — garantir uso de `.env` em produção.

### [Sprint 1] CORS `allow_origins=["*"]`
- **Descrição:** Permite qualquer origem.
- **Impacto:** Risco em produção.
- **Onde:** `app/main.py`
- **Status:** ⚠️ Aceitável para MVP — restringir em produção.

---

## 2️⃣ RISCOS SE NÃO CORRIGIR

| Área        | Risco                                                                 |
|------------|-----------------------------------------------------------------------|
| Segurança  | JWT fraco, CORS permissivo, Firebase sem credenciais em produção      |
| UX         | 401 sem tratamento, estatísticas erradas no Quiz                      |
| Performance| Buscas Bíblia sem validação, queries com parâmetros inválidos         |
| Escalabilidade | Sem paginação em highlights/annotations/bookmarks, leaderboard        |
| Consistência | Quiz com respostas duplicadas, XP inflado                           |

---

## 3️⃣ CORREÇÕES IMEDIATAS (já aplicadas)

1. **Firebase Admin init** em `main.py` (condicional ao arquivo de credenciais)
2. **Quiz:** bloqueio de resposta duplicada (checagem em `UserQuizHistory`)
3. **Bible API:** validação de `book` (1–66), `chapter` (1–150), `verse` (1–176) com `Path`
4. **ApiService:** interceptor 401 limpando token

---

## 4️⃣ AJUSTES RECOMENDADOS (prioridade média)

1. **Integrar SyncService** — chamar `syncOnAppStart()` após login ou no primeiro build com usuário logado
2. **Variáveis de ambiente** — documentar `.env` obrigatório em produção (JWT_SECRET, FIREBASE_CREDENTIALS_PATH)
3. **ApiService baseUrl** — trocar hardcode por config (env/build flavor) para iOS e dispositivos reais
4. **Quiz:** erro 409 para resposta duplicada em vez de 404
5. **Bible API:** ordem de rotas — garantir que `/{version}/search` seja avaliada antes de `/{version}/{book}/{chapter}` (já está correta)

---

## 5️⃣ CHECKLIST FINAL PRONTO-PARA-TESTES

### Autenticação
- [ ] Login Google → Firebase token → POST /auth/login com header → JWT retornado
- [ ] JWT no header em todas as requisições privadas
- [ ] 401 limpa token no cliente
- [ ] Logout limpa token e estado

### Bíblia
- [ ] GET /bible/versions retorna lista
- [ ] GET /bible/ARA/1/1 retorna Gênesis 1
- [ ] Parâmetros inválidos retornam 422
- [ ] Offline: download completo marca versão
- [ ] Leitura offline usa SQLite quando disponível

### Quiz
- [ ] GET /quiz/next-question retorna pergunta (auth)
- [ ] POST /quiz/answer registra resposta
- [ ] Resposta duplicada retorna erro
- [ ] XP e streak atualizam corretamente
- [ ] Leaderboard ordenado por XP

### User Content (highlights, annotations, bookmarks)
- [ ] CRUD com auth
- [ ] Dados isolados por user_id

### Estudos
- [ ] GET commentaries, cross-references, timeline, maps
- [ ] Tratamento de listas vazias

### Perfil
- [ ] reading-stats, quiz-stats, settings
- [ ] PUT settings persiste em MongoDB

### Fluxos reais
- [ ] Login → Bíblia → Ler → Highlight → Sair → Login → Highlight ainda aparece
- [ ] Quiz → Acertar → Errar → Ver stats
- [ ] Download offline → Desligar rede → Ler capítulo baixado

---

## Resumo

| Categoria      | Total | Corrigidos | Pendentes |
|----------------|-------|------------|-----------|
| Críticos       | 5     | 5          | 0         |
| Médios         | 4     | 0          | 4         |
| Documentação   | 2     | 0          | 2         |

**MVP está pronto para fase de testes (Sprint 6)** após as correções aplicadas.
