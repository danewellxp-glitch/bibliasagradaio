# Bíblia Sagrada IO

Repositório do app Bíblia Sagrada (mobile + backend).

## Estrutura do repositório

- **`bible-app-mobile/`** — App Flutter (Bíblia, Estudos, Quiz, Perfil). **Este é o app que você deve rodar.**
- **`bible-app-backend/`** — API FastAPI (PostgreSQL, MongoDB, Redis)
- **`lib/`**, **`android/`**, **`pubspec.yaml` na raiz** — Projeto Flutter padrão (demo). **Não use para desenvolvimento do app.**

## Como rodar o app no Android Studio

Se ao rodar "medium phone api" (ou qualquer dispositivo) aparecer a **Flutter Demo Home Page** (contador), é porque o Android Studio está usando o projeto da **raiz** em vez do app Bíblia.

**Solução:** abrir a pasta do app como projeto:

1. No Android Studio: **File → Open**
2. Navegue até a pasta **`bible-app-mobile`** (dentro do repositório) e selecione essa pasta
3. Clique em **Open**
4. Aguarde o Flutter pub get e a indexação
5. Selecione o device (ex.: Medium Phone API) e rode o app (Run ▶️)

O app que sobe será o **Bíblia Sagrada** (login, Bíblia, Estudos, Quiz, Perfil).

### Alternativa pela linha de comando

```bash
cd bible-app-mobile
flutter pub get
flutter run
```

## Backend

```bash
docker-compose up -d
# API em http://localhost:8000
```

---

Para visão geral do projeto, ver `docs/RELATORIO-OVERALL-PROJETO.md` e `CURSOR_CONTEXT.md`.
