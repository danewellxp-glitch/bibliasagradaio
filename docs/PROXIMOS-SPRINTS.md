# Proximos Sprints - Biblia Sagrada IO

**Criado em:** 09/02/2026
**Baseado em:** Auditoria completa do codebase + CURSOR_CONTEXT.md

---

## Estado Atual - O que JA FOI implementado

### Sprint 1 - Consolidacao: CONCLUIDO
- [x] populate_commentaries.py (~200 entradas)
- [x] populate_cross_references.py (~300 entradas)
- [x] populate_timeline.py (40 eventos)
- [x] quiz_questions.json (501 perguntas)
- [x] Endpoint GET /study/verse-context/{version}/{book}/{chapter}/{verse}
- [x] Flutter baseUrl configuravel via --dart-define
- [x] SyncService ativado apos login
- [x] ensureBackendToken() para restart do app

### Sprint 2 - Lexico Strong's: CONCLUIDO
- [x] LexiconEntry + WordOccurrence models (study.py)
- [x] LexiconService (get_entry, search, occurrences)
- [x] Endpoints: GET /study/lexicon/{strong}, GET /study/lexicon/search/?q=
- [x] populate_lexicon.py (93 entradas: 47 Hebrew + 46 Greek, ~440 ocorrencias)
- [x] Flutter: botao "Estudar" no HighlightMenu -> VerseStudySheet (tabs: Comentarios/Refs/Timeline)
- [x] Flutter: Long press versiculo -> seletor de palavras -> WordDetailSheet (dados Strong's)
- [x] Flutter: lexiconProvider, lexiconSearchProvider, verseContextProvider

### Sprint 3 - IA com Ollama/Qwen: CONCLUIDO
- [x] Container Ollama no docker-compose.yml (qwen2.5:7b)
- [x] app/core/cache.py (Redis cache + rate limit diario por usuario)
- [x] app/core/ai_gateway.py (Ollama HTTP, system prompt de estudo biblico)
- [x] AIRequestLog model em study.py
- [x] VerseAskRequest/Response schemas
- [x] POST /study/verse-ask (rate limit -> cache -> Ollama -> log)
- [x] Flutter: AskAIDialog (pergunta, resposta, contador restante)
- [x] Botao "Perguntar sobre este versiculo" no VerseStudySheet

### Sprint 4 - Onboarding + Polish: CONCLUIDO
- [x] OnboardingScreen (3 paginas com SharedPreferences)
- [x] GET /bible/verse-of-the-day (365 versiculos curados, deterministico por dia)
- [x] VerseOfTheDayCard no topo da aba Biblia
- [x] .env.example atualizado
- [x] Auto-create tables (Base.metadata.create_all) no main.py

### Sprint 5 - Multiplayer Online Quiz: CONCLUIDO
- [x] GameRoom + GameParticipant + GameAnswer models
- [x] GameService (create, join, start, question, answer, advance, finish)
- [x] 7 endpoints games (create, join, status, start, question, answer, results)
- [x] Flutter: GameModeScreen, CreateRoomScreen, LobbyScreen, MultiplayerGameScreen, GameResultScreen
- [x] Flutter: GameProvider com polling 2s
- [x] Nav bar: "Quiz" -> "Jogos" com sub-rotas multiplayer
- [x] Quiz solo acessivel via /games/quiz-solo

### Sprint 8 - Premium + Billing: CONCLUIDO
- [x] Subscription model + PremiumService
- [x] GET /premium/status, POST /premium/verify-receipt
- [x] Rate limit de IA usa status premium (3/dia free, 100/dia premium)
- [x] Flutter: PremiumScreen (comparacao free/premium), PremiumProvider
- [x] Botao Premium no perfil
- [ ] TODO: Integrar in_app_purchase package (Google Play/App Store)

### Sprint 10 - CI/CD + Deploy: CONCLUIDO
- [x] .github/workflows/backend-test.yml (pytest + postgres + redis)
- [x] .github/workflows/flutter-test.yml (analyze + test)
- [x] docker-compose.prod.yml (4 workers, SSL, certbot, backup, redis tuning)
- [x] nginx/nginx.prod.conf (HTTPS, rate limiting, security headers)
- [x] test_games_api.py (testes para games, verse-of-day, premium)

### Infraestrutura atualizada
- 9 API routers: auth, bible, games, premium, profile, quiz, study, user_content
- 9 services: auth, bible, game, lexicon, premium, quiz, stats, study, user_content
- 5 core modules: ai_gateway, cache, config, database, security
- Docker: api, postgres, mongo, redis, ollama, nginx
- Flutter: 9 features (auth, bible, games, onboarding, premium, study, quiz, profile, sermons[placeholder])
- CI/CD: GitHub Actions para backend + Flutter
- Testes: test_health, test_auth, test_bible_api, test_quiz_api, test_user_content_api, test_games_api

---

## O que AINDA NAO FOI implementado

| Funcionalidade | Prioridade | Complexidade | Status |
|---|---|---|---|
| ~~Jogos Multiplayer Online~~ | ~~Alta~~ | ~~Alta~~ | **CONCLUIDO (Sprint 5)** |
| Multiplayer Local (QR Code) | Media | Media | Pendente |
| Stop Biblico | Media | Media | Pendente |
| Verdadeiro ou Falso | Media | Baixa | Pendente |
| Pregacoes (audio/transcricao) | Media | Alta | Pendente |
| ~~Premium/Billing~~ | ~~Alta~~ | ~~Media~~ | **CONCLUIDO (Sprint 8)** |
| ~~Onboarding/Tutorial~~ | ~~Alta~~ | ~~Baixa~~ | **CONCLUIDO (Sprint 4)** |
| Notificacoes Push | Media | Media | Pendente |
| ~~Testes + CI/CD~~ | ~~Alta~~ | ~~Media~~ | **CONCLUIDO (Sprint 10)** |
| ~~Deploy producao~~ | ~~Alta~~ | ~~Media~~ | **CONCLUIDO (Sprint 10)** |
| Admin/CMS | Baixa | Media | Pendente |
| iOS (testar/publicar) | Media | Baixa | Pendente |
| Elasticsearch (busca avancada) | Baixa | Media | Pendente |
| In-app Purchase (Google Play) | Alta | Media | Pendente (tela pronta) |

---

## Sprints Priorizados (ordem recomendada)

### Sprint 4: Onboarding + Polish (1-2 semanas)

**Justificativa:** Antes de adicionar features complexas, garantir que o app existente funcione bem e retenha usuarios novos.

#### 4A. Tela de Onboarding (3 telas)

**Arquivo:** `bible-app-mobile/lib/features/onboarding/screens/onboarding_screen.dart` (NOVO)

- Tela 1: "Bem-vindo ao Biblia Sagrada IO" + ilustracao
- Tela 2: "Estude com ferramentas profundas" (lexico, comentarios, IA)
- Tela 3: "Jogue e aprenda" (quiz, XP, ranking)
- Botao "Comecar" -> Login
- SharedPreferences flag `onboarding_complete` para nao mostrar novamente

#### 4B. Devocional diario (simples)

**Backend:** Endpoint GET /api/v1/bible/verse-of-the-day (versiculo aleatorio/curado)
**Flutter:** Card na tela inicial ou no topo da aba Biblia

#### 4C. Melhorias de UX

- Skeleton loading nas listas (shimmer)
- Pull-to-refresh na aba Biblia
- Mensagens de estado vazio mais bonitas
- Haptic feedback em acoes (highlight, bookmark)
- Notificacao local diaria "Leia a Biblia hoje" (flutter_local_notifications)

#### 4D. Ajustes pendentes do Sprint 1

- [ ] Executar scripts de populate no Docker (se nao feito)
- [ ] Testar em dispositivo fisico Android
- [ ] Validar que telas de Estudos mostram dados reais
- [ ] .env.example para producao

**Verificacao:**
- App abre com onboarding na primeira vez
- Versiculo do dia aparece
- Loading states sao bonitos
- Notificacao local funciona

---

### Sprint 5: Multiplayer Online - Quiz (3-4 semanas)

**Justificativa:** Feature mais pedida, maior potencial de engajamento e viralizacao.

#### 5A. Backend: Modelos de jogo

**Arquivo:** `bible-app-backend/app/models/game.py` (NOVO)

```python
class GameRoom(Base):
    __tablename__ = "game_rooms"
    id = Column(UUID, primary_key=True, default=uuid4)
    room_code = Column(String(6), unique=True)  # codigo da sala
    game_type = Column(String(50))  # quiz, true_false, stop
    difficulty = Column(String(20))  # beginner, intermediate, advanced
    max_players = Column(Integer, default=10)
    created_by = Column(UUID, ForeignKey("users.id"))
    status = Column(String(20), default="waiting")  # waiting, playing, finished
    current_question = Column(Integer, default=0)
    total_questions = Column(Integer, default=10)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

class GameParticipant(Base):
    __tablename__ = "game_participants"
    id = Column(Integer, primary_key=True)
    room_id = Column(UUID, ForeignKey("game_rooms.id", ondelete="CASCADE"))
    user_id = Column(UUID, ForeignKey("users.id"))
    display_name = Column(String(50))
    score = Column(Integer, default=0)
    answers_correct = Column(Integer, default=0)
    answers_total = Column(Integer, default=0)
    joined_at = Column(DateTime, server_default=func.now())
```

#### 5B. Backend: GameService + endpoints

**Arquivo:** `bible-app-backend/app/services/game_service.py` (NOVO)
**Arquivo:** `bible-app-backend/app/api/v1/games.py` (NOVO)

Endpoints:
- POST /games/room/create -> cria sala, retorna room_code
- POST /games/room/{code}/join -> entra na sala
- GET /games/room/{code}/status -> status atual (jogadores, pontuacao)
- POST /games/room/{code}/start -> inicia o jogo (so o criador)
- GET /games/room/{code}/question -> proxima pergunta
- POST /games/room/{code}/answer -> responde pergunta

Mecanismo de sincronizacao: **polling** (GET /status a cada 2s)
- Simples de implementar, funciona em todas plataformas
- WebSocket pode vir depois como otimizacao

#### 5C. Backend: Leaderboard Redis

```python
# Redis sorted sets para ranking em tempo real
redis_client.zadd(f"game:{room_id}:scores", {user_id: score})
redis_client.zrevrange(f"game:{room_id}:scores", 0, -1, withscores=True)

# Leaderboard global semanal
redis_client.zadd(f"leaderboard:weekly:{week_number}", {user_id: total_xp})
```

#### 5D. Flutter: Telas multiplayer

**Arquivos novos:**
- `features/games/screens/game_mode_screen.dart` - Seletor: Jogar Solo / Criar Sala / Entrar em Sala
- `features/games/screens/create_room_screen.dart` - Criar sala (tipo jogo, dificuldade, max jogadores)
- `features/games/screens/lobby_screen.dart` - Sala de espera (lista jogadores, botao iniciar)
- `features/games/screens/multiplayer_game_screen.dart` - Tela do jogo (pergunta, timer, scoreboard lateral)
- `features/games/screens/game_result_screen.dart` - Resultado final (ranking, XP ganho)
- `features/games/providers/game_provider.dart` - Estado do jogo, polling, acoes

**Modificar:**
- `app_router.dart` - Adicionar rotas /games/*
- Bottom nav: trocar "Quiz" por "Jogos" (abrange quiz solo + multiplayer)

**Verificacao:**
1. Criar sala -> compartilhar codigo -> outro usuario entra
2. Iniciar jogo -> perguntas sincronizadas -> pontuacao ao vivo
3. Finalizar -> ranking -> XP distribuido
4. curl endpoints funcionam standalone

---

### Sprint 6: Verdadeiro/Falso + Stop Biblico (2-3 semanas)

**Justificativa:** Variedade de jogos aumenta retencao. Reutiliza infraestrutura do Sprint 5.

#### 6A. Verdadeiro ou Falso

**Backend:**
- Tabela `true_false_statements` (statement, is_true, explanation, difficulty, category)
- Script `populate_true_false.py` (~200 afirmacoes)
- Endpoint GET /games/true-false/next

**Flutter:**
- `true_false_game_screen.dart` - Statement + botoes V/F + animacao + explicacao
- Funciona tanto solo quanto multiplayer

#### 6B. Stop Biblico

**Backend:**
- Tabela `stop_categories` (id, name) - ex: Nome de pessoa, Lugar, Livro da Biblia, Objeto, Animal
- Endpoint POST /games/stop/validate (letra, categoria, resposta) -> valida se existe na Biblia
- Validacao: busca no banco de versiculos por match parcial

**Flutter:**
- `stop_game_screen.dart` - Letra sorteada + categorias + timer + input
- Modo solo: jogar contra o tempo
- Modo multiplayer: usar GameRoom existente com game_type="stop"

#### 6C. Modo Misto

- Sequencia aleatoria de quiz + V/F + stop em uma mesma partida
- Reutiliza infra de GameRoom com game_type="mixed"

**Verificacao:**
1. V/F: 200+ afirmacoes, explicacao ao errar
2. Stop: validacao funciona para nomes, lugares, livros
3. Misto: alterna entre tipos de jogo

---

### Sprint 7: Multiplayer Local + QR Code (1-2 semanas)

**Justificativa:** Permite jogar presencialmente (celula, EBD, grupo jovem).

#### 7A. QR Code

**Flutter:**
- Pacote `qr_flutter` (gerar) + `mobile_scanner` (ler)
- Tela "Criar Sala" gera QR com room_code embutido
- Tela "Entrar" tem botao "Ler QR Code" que scanneia e entra automaticamente
- Alternativa: digitar codigo manualmente (ja funciona do Sprint 5)

#### 7B. Modo Apresentador

- Opcao "Projetar na TV" (tela sem controles, so pergunta + placar)
- Usa a mesma API de GameRoom, mas com layout fullscreen
- Jogadores respondem nos proprios celulares

**Verificacao:**
1. QR gerado -> outro celular le -> entra na sala
2. Modo apresentador: tela limpa projetavel

---

### Sprint 8: Premium + Billing (2-3 semanas)

**Justificativa:** Monetizacao necessaria antes de escalar. Implementar apos ter features que justifiquem o upgrade.

#### 8A. Backend

**Modelo:**
```python
class Subscription(Base):
    user_id = Column(UUID, ForeignKey("users.id"))
    plan = Column(String(20))  # free, monthly, annual
    status = Column(String(20))  # active, cancelled, expired
    provider = Column(String(20))  # google_play, app_store
    provider_subscription_id = Column(String(200))
    started_at = Column(DateTime)
    expires_at = Column(DateTime)
```

**Endpoints:**
- POST /premium/verify-receipt (valida compra Google Play/App Store)
- GET /premium/status (retorna plano atual)
- Middleware: `get_user_plan()` para verificar limites

#### 8B. Flutter

- `premium_screen.dart` - Comparacao free vs premium, botao assinar
- In-app purchase: `in_app_purchase` package (Google Play + App Store)
- Badge "Premium" no perfil
- Rate limit de IA ajustado (100/dia vs 3/dia)

**Beneficios Premium:**
- Perguntas IA ilimitadas (100/dia vs 3/dia)
- Download de todas versoes offline
- Sem anuncios (quando implementados)
- Modos de jogo exclusivos (ex: campeonatos)
- Upload de pregacoes (futuro)

**Verificacao:**
1. Tela premium mostra beneficios
2. Compra funciona (sandbox Google Play)
3. Apos compra, rate limit de IA aumenta
4. Badge premium aparece no perfil

---

### Sprint 9: Pregacoes - Audio e Transcricao (3-4 semanas)

**Justificativa:** Diferencial competitivo forte, mas complexo. Implementar apos monetizacao estar funcionando.

#### 9A. Backend

**MongoDB collection `sermons`:**
```json
{
    "user_id": "uuid",
    "title": "Pregacao sobre Joao 3:16",
    "file_url": "uploads/sermon_123.mp3",
    "duration_seconds": 2400,
    "transcription": {
        "status": "processing|completed|failed",
        "text": "...",
        "segments": [{"start": 0.0, "end": 5.2, "text": "..."}]
    },
    "bible_references": [
        {"book": 43, "chapter": 3, "verse": 16, "timestamp": 120.5}
    ]
}
```

**Endpoints:**
- POST /sermons/upload (upload MP3/WAV)
- GET /sermons/ (listar do usuario)
- GET /sermons/{id} (detalhes + transcricao)
- POST /sermons/{id}/transcribe (inicia transcricao async)

**Transcricao:**
- Opcao A: Ollama + Whisper (self-hosted, gratuito)
- Opcao B: OpenAI Whisper API (pago, mais preciso)
- Usar Celery/BackgroundTasks para processamento async

#### 9B. Flutter

- `sermon_upload_screen.dart` - Upload de audio (file_picker)
- `sermon_list_screen.dart` - Lista de pregacoes do usuario
- `sermon_player_screen.dart` - Player com transcricao sincronizada
- Substituir placeholder "Em breve" na aba Pregacoes

**Verificacao:**
1. Upload de MP3 funciona
2. Transcricao roda em background
3. Player mostra texto sincronizado
4. Busca por palavra na transcricao

---

### Sprint 10: Testes + CI/CD + Deploy (3 semanas)

**Justificativa:** Antes de publicar na Play Store, precisa de qualidade e pipeline automatizado.

#### 10A. Testes Backend

- Ampliar testes existentes (test_study_api, test_games_api)
- Testes para rate limiting de IA
- Testes para cache Redis
- Testes para GameRoom lifecycle
- Load test com Locust (100 usuarios simultaneos)

#### 10B. Testes Flutter

- Widget tests para telas principais
- Integration tests (patrol ou integration_test)
- Golden tests para UI critica

#### 10C. CI/CD

**GitHub Actions:**
- `.github/workflows/backend-test.yml` - pytest on push
- `.github/workflows/flutter-test.yml` - flutter test + analyze on push
- `.github/workflows/deploy.yml` - deploy automatizado

#### 10D. Deploy

- Docker Compose producao (docker-compose.prod.yml)
- VPS ou Cloud Run
- SSL com Let's Encrypt
- Backup automatico PostgreSQL
- Monitoramento: Sentry (erros) + UptimeRobot (disponibilidade)
- Dominio: api.bibliasagrada.io

#### 10E. Publicacao

- Google Play Console: configurar listing, screenshots, descricao
- APK/AAB assinado
- Beta testing (internal track)
- Revisao de politicas (conteudo religioso permitido)

**Verificacao:**
1. Todos os testes passam
2. CI roda em cada push
3. Deploy automatico funciona
4. App acessivel via URL publica
5. Beta testers conseguem instalar

---

## Resumo Visual

```
Sprint 4: Onboarding + Polish        [1-2 sem] -> Retencao de usuarios novos
Sprint 5: Multiplayer Online Quiz     [3-4 sem] -> Feature principal de engajamento
Sprint 6: V/F + Stop Biblico         [2-3 sem] -> Variedade de jogos
Sprint 7: Multiplayer Local + QR     [1-2 sem] -> Jogos presenciais
Sprint 8: Premium + Billing          [2-3 sem] -> Monetizacao
Sprint 9: Pregacoes (Audio)          [3-4 sem] -> Conteudo diferenciado
Sprint 10: Testes + CI/CD + Deploy   [3 sem]   -> Qualidade e lancamento
                                     -----------
                                     ~18-23 semanas total
```

## Dependencias entre sprints

```
Sprint 4 (Onboarding)  -> independente, pode comecar ja
Sprint 5 (Multiplayer) -> independente, pode comecar ja
Sprint 6 (V/F + Stop)  -> depende do Sprint 5 (infra de GameRoom)
Sprint 7 (Local + QR)  -> depende do Sprint 5 (infra de GameRoom)
Sprint 8 (Premium)     -> melhor apos Sprint 5 e 6 (features para justificar)
Sprint 9 (Pregacoes)   -> independente, mas melhor apos Sprint 8 (premium limita uploads)
Sprint 10 (Deploy)     -> melhor por ultimo (testa tudo que foi feito)
```

## Recomendacao de execucao paralela

Se houver dois desenvolvedores:
- **Dev A:** Sprint 4 -> Sprint 8 -> Sprint 9
- **Dev B:** Sprint 5 -> Sprint 6 -> Sprint 7

Sprint 10 como esforco conjunto no final.
