# Deploy e Publicação Beta – Sprint 6

## Deploy do backend (Task 6.3)

### Desenvolvimento (com nginx)
```bash
docker-compose up -d
# API: http://localhost:80 (nginx) ou http://localhost:8000 (direto)
```

### Produção
1. Copiar `bible-app-backend/.env.production.example` para `bible-app-backend/.env.production`.
2. Preencher em `.env.production`: `JWT_SECRET`, `POSTGRES_PASSWORD`, e garantir que `serviceAccountKey.json` esteja em `bible-app-backend/`.
3. Subir com override de produção:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```
4. **SSL (Let's Encrypt):** editar `nginx/nginx.conf`, descomentar o bloco `server` com `listen 443 ssl`, configurar caminhos dos certificados e montar volumes em `docker-compose.prod.yml` para `/etc/letsencrypt`. Usar certbot para obter os certificados.

---

## Build e publicação beta (Task 6.4)

### Android
```bash
cd bible-app-mobile
flutter pub get
flutter build apk --release
# APK: build/app/outputs/flutter-apk/app-release.apk
```
- Google Play Beta: criar app em [Play Console](https://play.google.com/console), fazer upload do AAB (`flutter build appbundle --release`) e enviar para teste interno/fechado.

### iOS
```bash
cd bible-app-mobile
flutter build ios --release
```
- Abrir `ios/Runner.xcworkspace` no Xcode, configurar signing e enviar para TestFlight (Archive → Distribute App → App Store Connect).

### Checklist pré-beta
1. Testes em dispositivos reais (Android e iOS).
2. Login com Google/Apple e chamadas à API em produção.
3. Ajustar `ApiService` baseUrl no app para a URL da API em produção (ex.: `https://api.seudominio.com`).
4. Corrigir bugs encontrados nos testes.

---

## Commits sugeridos (Sprint 6)

```bash
git add bible-app-backend/tests/ conftest.py
git commit -m "test(backend): add integration tests for Bible, Quiz, User Content API"

git add bible-app-mobile/test/
git commit -m "test(mobile): add widget tests for Bible reader and Quiz"

git add nginx/ docker-compose.yml docker-compose.prod.yml bible-app-backend/.env.production.example bible-app-backend/.gitignore
git commit -m "infra: add production deployment with nginx, SSL placeholder, and docker-compose"

git add docs/DEPLOY-E-BETA.md
git commit -m "docs: add deploy and beta release instructions"
```
