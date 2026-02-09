# Relatório Completo — Bíblia Sagrada IO

**Data:** 08/02/2026  
**Tipo:** Visão geral técnica, executiva, de marketing e estratégica

---

# PARTE 1 — RESUMO EXECUTIVO

## O que é o projeto

**Bíblia Sagrada IO** é um aplicativo multiplataforma de estudo bíblico que combina:

- **Leitura interativa** da Bíblia (múltiplas versões, offline)
- **Ferramentas de estudo** (comentários, referências cruzadas, linha do tempo, mapas)
- **Gamificação** (quiz com XP, streaks, ranking)
- **Conteúdo do usuário** (destaques, anotações, favoritos, compartilhamento)
- **Plano futuro:** IA como facilitadora, jogos multiplayer, pregações com áudio/transcrição

**Modelo de negócio:** Freemium (básico gratuito, premium pago).  
**Plataformas:** Android (foco atual), iOS (estrutura pronta), via Flutter.  
**Infraestrutura:** Backend auto-hosted (FastAPI + PostgreSQL + MongoDB + Redis), Docker Compose.

## Estado atual em uma frase

O **MVP está ~80% implementado**: backend e app cobrem Bíblia, Quiz, Estudos, Perfil, conteúdo do usuário e offline. Faltam consolidação (dados populados, sync ativo, URL configurável), testes, deploy e as fases avançadas (IA, multiplayer, pregações, premium).

## Principais riscos e oportunidades

| Aspecto | Situação | Ação sugerida |
|--------|----------|----------------|
| Dados de Estudos/Quiz | Scripts existem, população não confirmada | Rodar e validar scripts; garantir conteúdo nas telas |
| Sync e API em device real | SyncService não chamado; URL fixa para emulador | Ativar sync pós-login; baseUrl configurável |
| Segurança em produção | CORS `*`, JWT em .env | Definir .env.production e restringir origens |
| Diferencial de mercado | Estudo + gamificação + IA controlada | Comunicar claramente no posicionamento e no lançamento |

---

# PARTE 2 — VISÃO TÉCNICA

## 2.1 Stack tecnológica

| Camada | Tecnologia | Observação |
|--------|------------|------------|
| **Mobile** | Flutter 3.x, Dart 3 | Riverpod, go_router, sqflite, Dio, Firebase Auth/Analytics/Messaging |
| **Backend** | Python 3.11, FastAPI | Uvicorn, SQLAlchemy, Pydantic |
| **Banco relacional** | PostgreSQL 15 | Bíblia, usuários, quiz, user content, estudos |
| **Banco flexível** | MongoDB 7 | Preferências, settings, futuros metadados de áudio |
| **Cache e sessão** | Redis 7 | Cache, rate limiting, leaderboards (planejado) |
| **Auth** | Firebase Auth + JWT | Login com Google (e Apple preparado) |
| **Infra** | Docker Compose, Nginx | API, Postgres, Mongo, Redis, proxy reverso |

## 2.2 Arquitetura de alto nível

```
[Flutter App] ←→ HTTPS/REST ←→ [Nginx] ←→ [FastAPI]
                                      ↓
     SQLite (offline)          PostgreSQL + MongoDB + Redis
```

- **App:** Offline-first (SQLite para Bíblia e dados locais), sync de highlights/annotations/bookmarks/settings (serviço implementado, ainda não ativado no fluxo pós-login).
- **API:** Stateless, autenticação JWT, endpoints REST por domínio (auth, bible, study, quiz, user_content, profile).

## 2.3 Estrutura do backend (`bible-app-backend`)

- **`app/api/v1/`:** auth, bible, study, user_content, quiz, profile.
- **`app/models/`:** user, bible (versões, textos, highlights, annotations, bookmarks), quiz (perguntas, histórico, stats, achievements), study (commentaries, cross_references, timeline, maps).
- **`app/services/`:** auth, bible, study, quiz, user_content, stats.
- **`app/core/`:** config, database (Postgres), security (JWT + Firebase).
- **Scripts:** população da Bíblia, comentários, referências cruzadas, timeline, quiz (JSON + script).

## 2.4 Estrutura do app Flutter (`bible-app-mobile`)

- **`lib/features/`:** auth, bible (leitor, busca, seletor de livro/capítulo, highlights, anotações, share), study (comentários, refs, timeline, mapas), quiz (home, jogo, resultado, leaderboard), profile (perfil, stats, settings, offline), sermons (placeholder “Em breve”).
- **`lib/core/`:** theme, services (api, auth, offline, sync), constants (livros, Firebase).
- **`lib/data/`:** models, repositories (bible, offline_bible, user_content).
- **State:** Riverpod; navegação com go_router e bottom nav (Bíblia, Estudos, Pregações, Quiz, Perfil).

## 2.5 O que está implementado e funcionando

- **Backend:** API no Docker; auth Google → JWT; Bíblia (4 versões, ~124k versículos); Quiz (next, submit, stats, leaderboard); user content (highlights, annotations, bookmarks CRUD); perfil (reading/quiz stats, settings, achievements); estudos (endpoints de commentaries, cross-refs, timeline, maps).
- **App:** Login Google; aba Bíblia (leitura, busca, seletor); highlights/anotações/bookmarks e compartilhamento com imagem; Quiz (fluxo completo, XP/streak); Perfil (estatísticas, configurações, download offline); Estudos (telas que consomem API); offline-first com SQLite.

## 2.6 Pontos frágeis ou pendentes (técnico)

- **Dados:** Estudos e Quiz dependem de scripts executados (populate_commentaries, cross_references, timeline, quiz); validar contagens e experiência nas telas.
- **SyncService:** Implementado mas não invocado após login; sync automático de user content e settings não ocorre.
- **Configuração:** Base URL da API fixa para emulador (`10.0.2.2:8000`); em dispositivo físico/iOS é necessário baseUrl configurável (env/flavor).
- **Produção:** CORS `*`, JWT_SECRET e credenciais Firebase devem vir de .env; sem CI/CD nem deploy documentado ainda.
- **Qualidade:** Testes E2E/unitários não implementados de forma visível; iOS não testado.

## 2.7 Roadmap técnico resumido (do CURSOR_CONTEXT)

- **Sprint 1 (consolidação):** Popular Estudos/Quiz, ativar SyncService, baseUrl configurável, validar em device real. (Parcialmente feito.)
- **Sprint 2–3:** Seleção inteligente de palavras (Strong’s), seleção de versículos com IA (cache, rate limit).
- **Sprint 4–6:** Multiplayer (salas, ranking), multiplayer local (QR), Stop Bíblico.
- **Sprint 7–8:** Áudio/transcrição (pregações), freemium e billing.
- **Sprint 9–10:** Onboarding, testes, deploy, monitoramento.

---

# PARTE 3 — MARKETING E ESTRATÉGIA

## 3.1 Posicionamento

- **Categoria:** Educação / Religião / Estudo Bíblico.
- **Diferencial:** Estudo profundo (comentários, referências, timeline, mapas) + gamificação (quiz, XP, streaks, ranking) + plano de IA como **facilitadora** (sem interpretação doutrinária).
- **Público-alvo:** Cristãos evangélicos (e ampliável) que buscam aprofundamento na Bíblia de forma engajante e organizada.

## 3.2 Proposta de valor

| Para o usuário | Como o produto entrega |
|----------------|------------------------|
| Ler a Bíblia em qualquer lugar | Múltiplas versões, modo offline, progresso e favoritos |
| Estudar com profundidade | Comentários, referências cruzadas, linha do tempo, mapas |
| Aprender de forma divertida | Quiz com dificuldade adaptativa, XP, streaks, ranking |
| Guardar e revisar | Destaques, anotações, bookmarks, compartilhamento |
| (Futuro) Perguntar sobre palavras/versículos | IA com limite free, cache e sem doutrina |

## 3.3 Diferenciação vs concorrentes

- **Apps só de leitura:** Bíblia Sagrada IO agrega estudo estruturado e gamificação.
- **Apps só de quiz/jogos:** Oferece Bíblia completa + estudo (comentários, refs, timeline).
- **Uso de IA:** Posicionamento explícito de “facilitadora”, com cache e rate limit para custo e segurança; sem gerar doutrina.

## 3.4 Modelo de negócio (freemium)

- **Gratuito:** Leitura, busca, uma versão offline, comentários/refs/timeline/mapas, quiz, highlights/annotations/bookmarks, compartilhamento, estatísticas básicas. Limite planejado de perguntas IA/dia (ex.: 3).
- **Premium (a implementar):** Mais perguntas IA, todas as versões offline, sem anúncios, acesso antecipado a jogos, upload de áudio (pregações), etc.
- **Monetização futura:** Assinatura (Stripe/RevenueCat), possível admin/CMS para conteúdo.

## 3.5 Mercado e oportunidade

- **Tamanho:** Mercado de apps religiosos e de estudo bíblico em crescimento; público evangélico no Brasil relevante e engajado.
- **Tendências:** Gamificação e microlearning aumentam retenção; IA como assistente de estudo é um diferencial comunicável.
- **Risco:** Concorrência de apps já estabelecidos; importância de clareza no posicionamento (estudo + gamificação + IA controlada) e de execução (dados populados, sync, estabilidade).

## 3.6 Estratégia de go-to-market (sugestão)

1. **Pré-lançamento:** Validar dados (Estudos/Quiz), ativar sync, configurar API para device real; landing/lista de espera e “Me avisar quando lançar” (já existe para Pregações).
2. **Lançamento beta:** Android primeiro (Google Play Beta); feedback direto de usuários e igrejas/grupos de estudo.
3. **Canais:** Igrejas, líderes de célula, redes sociais (conteúdo de versículos + dicas de estudo), parcerias com ministérios de ensino.
4. **Mensagem:** “Estude a Bíblia a fundo e de forma divertida: leitura, comentários, quiz e, em breve, perguntas inteligentes.”
5. **Métricas:** DAU/MAU, retenção D7/D30, uso de Quiz e Estudos, conversão free → premium (quando existir).

## 3.7 Roadmap estratégico (alto nível)

| Fase | Foco | Objetivo de negócio |
|------|------|----------------------|
| **Consolidação** | Dados, sync, URL, device real | App estável e completo para beta |
| **IA controlada** | Palavras + versículos, cache, limites | Diferencial e valor percebido |
| **Multiplayer** | Quiz e Stop online/local | Engajamento e viralidade |
| **Pregações** | Áudio, transcrição, player | Novo use case e retenção |
| **Premium** | Assinatura, paywall | Receita recorrente |

---

# PARTE 4 — MÉTRICAS DE SUCESSO E PRÓXIMOS PASSOS

## 4.1 Métricas sugeridas

**Técnicas:** Cache hit (IA) > 80%; latência P95 < 500 ms; uptime > 99,5%.  
**Produto:** DAU/MAU > 20%; retenção D7 > 40%; conversão free → premium > 3% (quando houver premium).

## 4.2 Próximos passos imediatos (prioridade)

1. **Backend:** Executar e validar scripts de população (commentaries, cross_references, timeline, quiz); conferir contagens nas tabelas e resposta dos endpoints.
2. **App:** Ativar SyncService após login; tornar baseUrl configurável (env/build flavor); testar em dispositivo físico Android.
3. **Produto:** Garantir que as telas de Estudos e Quiz exibam conteúdo real após população.
4. **Operação:** Documentar .env de produção (JWT, Firebase, CORS) e preparar checklist de deploy.

---

# ANEXO — REFERÊNCIAS RÁPIDAS

- **Contexto para IA:** `CURSOR_CONTEXT.md`
- **Estado atual:** `docs/ESTADO-ATUAL-DO-PROJETO.md`
- **Especificação:** `ESPECIFICACAO-TECNICA-COMPLETA.md`
- **Plano MVP/sprints:** `docs/plans/2026-02-01-biblia-sagrada-app-mvp.md`

---

*Relatório gerado para alinhamento técnico, executivo, de marketing e estratégico. Atualizar conforme o projeto evoluir.*
