# Bíblia Sagrada — App Mobile

App Flutter do projeto Bíblia Sagrada IO (leitura, estudos, quiz, perfil).

## Rodar o app

```bash
flutter pub get
flutter run
```

## Conectar na API (backend)

O app precisa da API rodando para carregar a Bíblia (até você baixar uma versão para uso offline).

### 1. Subir o backend

Na **raiz do repositório** (pasta `bibliasagradaio`):

```bash
docker-compose up -d
```

A API fica em `http://localhost:8000`.

### 2. Endereço da API no app

- **Emulador Android:** o padrão `http://10.0.2.2:8000` já aponta para o localhost da sua máquina. Nada a configurar.
- **Dispositivo físico ou iOS:** o emulador não está na mesma máquina, então use o **IP do seu PC** na rede (ex.: `192.168.1.10`):

```bash
# Descubra o IP (Windows: ipconfig, Mac/Linux: ifconfig ou ip addr)
flutter run --dart-define=API_BASE_URL=http://SEU_IP:8000
```

Exemplo: `flutter run --dart-define=API_BASE_URL=http://192.168.1.10:8000`

No Android Studio: **Run → Edit Configurations** e em **Additional run args** coloque:

`--dart-define=API_BASE_URL=http://SEU_IP:8000`

### Se aparecer "connection timeout"

- Confirme que o backend está no ar: `docker-compose ps` e acesse `http://localhost:8000/health` no navegador.
- Em **dispositivo físico**, use o IP do PC com `--dart-define=API_BASE_URL=...` como acima.
- Como alternativa, use **Baixar Bíblia para uso offline** no menu (⋯) do leitor; depois o capítulo carrega do SQLite sem depender da API.

## Estrutura

- `lib/features/` — auth, bible, study, quiz, profile, sermons
- `lib/core/` — theme, services (api, auth, offline, sync)
- `lib/data/` — models, repositories
