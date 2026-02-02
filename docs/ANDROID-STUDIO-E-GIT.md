# Testar no Android Studio e fazer Commit/Push

## 1. Abrir o projeto no Android Studio

1. **Android Studio** → File → Open.
2. Selecione a pasta **`bible-app-mobile`** (não a raiz do repositório).
3. Aguarde o Gradle sync e o `flutter pub get` (se o Android Studio pedir).
4. Conecte um dispositivo ou inicie um emulador (AVD) e rode com **Run** (▶) ou `Shift+F10`.

**Importante:** O app Flutter fica em `bible-app-mobile/`. A raiz do repo contém também o backend e outros arquivos.

### Erro: "flutter.sdk not set in local.properties"

Se o projeto foi clonado (ex.: em `StudioProjects`) ou aberto sem rodar Flutter antes, o arquivo `android/local.properties` não existe (ele é gerado pelo Flutter e está no `.gitignore`).

**Solução 1 (recomendada):** No terminal, na pasta **bible-app-mobile**:

```powershell
cd C:\Users\danew\StudioProjects\bibliasagradaio\bible-app-mobile
flutter pub get
```

Isso gera `android/local.properties` com `flutter.sdk` e `sdk.dir`. Depois, sincronize o Gradle no Android Studio (File → Sync Project with Gradle Files).

**Solução 2:** Crie manualmente o arquivo `bible-app-mobile/android/local.properties` com (ajuste os caminhos para o seu PC):

```properties
sdk.dir=C:\\Users\\danew\\AppData\\Local\\Android\\sdk
flutter.sdk=C:\\Users\\danew\\src\\flutter
```

No Windows use **barras duplas** (`\\`). Você pode copiar de `android/local.properties.example` e trocar `YOUR_USER` pelo seu usuário.

---

## 2. Firebase (só na sua máquina)

O arquivo **`google-services.json`** não é commitado (está no `.gitignore`).

- Se ainda não tiver: copie o arquivo que você baixou do Firebase Console para **`bible-app-mobile/android/app/google-services.json`**.
- Quem clonar o projeto precisa baixar o próprio `google-services.json` do Firebase e colocar no mesmo caminho.

---

## 3. Antes do commit

- **Não commitar:** `google-services.json`, `serviceAccountKey.json`, arquivos `*firebase*adminsdk*.json`, `.env`, `.env.production`.
- O `.gitignore` já evita isso; mesmo assim, confira com `git status` antes de dar commit.

---

## 4. Commit e push (na raiz do repositório)

Na pasta **raiz do projeto** (onde está `bible-app-backend`, `bible-app-mobile`, `docker-compose.yml`):

```powershell
cd C:\Users\danew\Documents\bibliasagradaio

# Ver o que será commitado (não deve listar .env, google-services.json, serviceAccountKey.json, nul)
git status

# Adicionar tudo exceto o que está no .gitignore
git add .

# Commit (primeiro commit = Initial commit)
git commit -m "chore: prepare project for Android Studio testing and push"

# Enviar (primeira vez: -u define upstream)
git push -u origin main
```

**Se der erro "src refspec main does not match any":** significa que ainda não há nenhum commit (por exemplo, porque `git add` falhou antes). Confirme que `git add .` terminou sem erro e que `git commit` foi executado com sucesso.

**Se o branch padrão do GitHub for `master`:**
```powershell
git push -u origin master
```

**Nota:** O arquivo `nul` (nome reservado no Windows) foi removido e está no `.gitignore` para não ser criado de novo por engano.

---

## 5. Resumo

| Ação              | Onde                         |
|-------------------|------------------------------|
| Abrir no Android Studio | Pasta **bible-app-mobile**   |
| Rodar o app       | Run no Android Studio ou `flutter run` em `bible-app-mobile` |
| Commit / push     | Na **raiz** do repo (`bibliasagradaio`) |

Após o primeiro push, quem clonar deve colocar o próprio `google-services.json` em `bible-app-mobile/android/app/` e abrir a pasta `bible-app-mobile` no Android Studio.
