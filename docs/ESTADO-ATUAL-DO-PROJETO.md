# Estado atual do projeto — Bíblia Sagrada IO

Resumo do que **funciona**, do que está **parcial** e do que **ainda não existe**, para alinhar com IA/equipe e priorizar próximos passos.

---

## O que FUNCIONA

### Backend (FastAPI + PostgreSQL + Docker)
- **API no ar:** Docker Compose sobe API, Postgres (porta 5433), Mongo, Redis, Nginx.
- **Auth:** Login com Google (Firebase) → token JWT. Endpoint `POST /api/v1/login`. Firebase Admin init condicional.
- **Bíblia:** 
  - `GET /api/v1/bible/versions` — retorna NVI, ARC, ACF, KJV.
  - `GET /api/v1/bible/{version}/{book}/{chapter}` — capítulo completo.
  - `GET /api/v1/bible/{version}/{book}/{chapter}/{verse}` — versículo único.
  - `GET /api/v1/bible/{version}/search?q=...` — busca.
  - **Dados:** ~124k versículos, 66 livros, 4 versões (script `download_and_populate_bible.py`).
- **Quiz:** next-question, submit answer, stats, leaderboard. Resposta duplicada bloqueada.
- **User content:** highlights, annotations, bookmarks (CRUD com auth).
- **Perfil:** reading-stats, quiz-stats, settings (GET/PUT), achievements. Settings em MongoDB.
- **Estudos:** endpoints de commentaries, cross-references, timeline, maps (retornam dados se populados).

### App Flutter (Android em foco)
- **Login:** tela de login, Google Sign-In, envio do token para backend, navegação pós-login.
- **Aba Bíblia:** lista de versões (API), seletor de livro/capítulo, leitor de capítulo (versos), versão padrão NVI.
- **Busca:** busca por texto na Bíblia (API).
- **Highlights/Anotações/Bookmarks:** UI (menus, diálogos) e integração com API quando logado.
- **Compartilhar versículo:** sheet de compartilhamento e geração de imagem do versículo.
- **Quiz:** tela inicial, jogar pergunta, resultado, leaderboard, XP/streak (se backend tiver perguntas).
- **Perfil:** tela de perfil, estatísticas de leitura/quiz, configurações (fonte, tema, versão padrão), gerenciamento offline (download de versão para SQLite).
- **Estudos:** abas/telas para comentários, referências cruzadas, linha do tempo, mapas (chamam API; conteúdo depende de dados no backend).
- **Offline:** fluxo offline-first: tenta SQLite primeiro, depois API. Download de versão inteira para uso offline (sem rede).
- **Pregações:** aba existe com tela “Em breve” e switch “Me avisar quando lançar” (sem backend).

### Infra / DevEx
- Git (Documents = fonte, pull no Android Studio a partir daqui).
- Scripts de população: Bíblia completa (download + insert), seed de Gênesis, scripts para commentaries, cross-refs, quiz, timeline (existência dos scripts; dados podem não estar todos rodados).

---

## O que está PARCIAL ou FRÁGIL

- **Dados de Estudos:** Endpoints existem; tabelas (commentaries, cross_references, timeline, maps) existem; scripts `populate_commentaries.py`, `populate_cross_references.py`, `populate_timeline.py` existem — **não está claro se já foram executados e se há volume de dados** para uma boa experiência.
- **Quiz:** Lógica e API ok; **depende de perguntas no banco** (`populate_quiz.py` / `quiz_questions.json`). Sem dados, a experiência fica vazia.
- **SyncService:** Implementado mas **nunca chamado** (ex.: após login). Highlights/annotations/bookmarks não sincronizam automaticamente ao abrir o app.
- **Base URL da API:** Hardcoded `10.0.2.2:8000` (emulador Android). Em **dispositivo físico** ou **iOS** é preciso configurar IP/host (env ou flavor).
- **Segurança/Produção:** CORS `*`, JWT_SECRET e Firebase credenciais precisam de .env em produção; documentado como “aceitável para MVP, restringir depois”.

---

## O que NÃO existe / está “seco”

- **Pregações (Fase 2):** Apenas placeholder “Em breve”. Sem upload de áudio, transcrição, análise com IA, listagem, player.
- **IA em geral:** Nada de chat bíblico, sugestões com IA, análise de pregações (previsto para Fase 2/3 na especificação).
- **Conteúdo rico de Estudos:** Comentários, referências cruzadas, timeline e mapas podem estar vazios ou com poucos dados; experiência “seca” se não houver população consistente.
- **Onboarding / Tutorial:** Nenhum fluxo de primeira utilização.
- **Notificações push:** Firebase Messaging referenciado na stack; integração no app não verificada.
- **Testes automatizados:** Checklist de testes manuais no REFINAMENTO; cobertura de testes E2E/unitários não implementada de forma visível.
- **iOS:** Estrutura Flutter existe; configuração e testes em iOS não foram foco (Android em evidência).
- **Deploy/produção:** Sem pipeline (CI/CD) nem doc de deploy em servidor (apenas previsão de auto-hosted na especificação).
- **Admin / CMS:** Opcional na spec; não implementado.
- **Pagamento / Premium:** Modelo freemium definido na spec; nenhuma implementação de assinatura ou paywall no app.

---

## Resumo em uma frase

**Funciona:** Backend com auth, Bíblia completa (4 versões, 124k versículos), Quiz (lógica + API), user content (highlights/annotations/bookmarks), perfil e configurações, fluxo offline básico, e a maior parte das telas do app (Bíblia, Quiz, Perfil, Estudos, Pregações placeholder).  
**Pendente/parcial:** Dados de Estudos e Quiz populados, SyncService ativado, config de API para dispositivo real/iOS, pregações e IA (Fase 2), testes, deploy e freemium.

---

## Sugestão de próximos passos (para jogar na IA)

1. **Popular Estudos e Quiz:** Rodar e validar `populate_commentaries`, `populate_cross_references`, `populate_timeline`, `populate_quiz` e garantir que as telas de Estudos e Quiz tenham conteúdo.
2. **Ativar SyncService:** Chamar sincronização (highlights/annotations/bookmarks/settings) após login ou no primeiro build com usuário logado.
3. **Configurar baseUrl:** Tornar a URL da API configurável (env ou build flavor) para dispositivo físico e iOS.
4. **Definir prioridade das “novas ideias”:** Listar as ideias (ex.: novas features, melhorias de UX, IA, pregações) e ordenar por impacto vs esforço para a próxima sprint.

---

*Documento gerado para alinhamento de estado do projeto. Atualizar conforme o produto evoluir.*
