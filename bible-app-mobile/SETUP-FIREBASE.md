# Setup Flutter + Firebase para Biblia Sagrada

## Pré-requisitos

- **Flutter** instalado e no PATH ([instalar](https://docs.flutter.dev/get-started/install))
- **Android Studio** (opcional, mas recomendado)
- Arquivo **google-services.json** já em `android/app/` (baixado do Firebase Console)

## Passo a passo automático

### 1. Execute o script de setup

No terminal (PowerShell ou CMD), na pasta **bible-app-mobile**:

```powershell
.\setup_flutter_firebase.ps1
```

O script faz:
- `flutter create . --org com.bibliasagrada` (gera android/ e ios/)
- Copia `google-services.json` para `android/app/` (se faltar)
- Adiciona o plugin **google-services** no `build.gradle` do projeto
- Configura **applicationId** como `com.bibliasagrada.app`
- Aplica o plugin **google-services** no módulo app
- Executa `flutter pub get`

### 2. Rodar o app

```bash
flutter run
```

## Alternativa: FlutterFire CLI

Se preferir, use o FlutterFire para configurar automaticamente:

```bash
dart pub global activate flutterfire_cli
flutterfire configure
```

Isso gera `firebase_options.dart` e configura o Gradle.

## Package name Android

O app está registrado no Firebase com:
- **Package name:** `com.bibliasagrada.app`
- **google-services.json** deve estar em `android/app/google-services.json`

## SHA-1 para Google Sign-In (obrigatório)

O **Google Sign-In** no Android exige que o **SHA-1** do certificado esteja registrado no Firebase. Sem isso, o login falha com **ApiException código 10** (DEVELOPER_ERROR).

### 1. Obter o SHA-1 de debug

**Importante:** use a pasta do app Flutter (`bible-app-mobile\android`), **não** a pasta `android` na raiz do repositório.

**Opção A – keytool (recomendado, não depende do Gradle/Java do projeto):**

Se `keytool` não estiver no PATH, use o que vem com o Android Studio:
```powershell
& "C:\Program Files\Android\Android Studio\jbr\bin\keytool.exe" -list -v -alias androiddebugkey -keystore "$env:USERPROFILE\.android\debug.keystore" -storepass android
```
Ou, com keytool no PATH (JDK instalado):
```powershell
keytool -list -v -alias androiddebugkey -keystore $env:USERPROFILE\.android\debug.keystore
```
Senha padrão: `android`. Copie o valor de **SHA1** (ex.: `AA:BB:CC:...`).

**Opção B – Gradle (exige Java 11+ no PATH/JAVA_HOME):**
```powershell
cd bible-app-mobile\android
.\gradlew signingReport
```
Procure em **Variant: debug** a linha **SHA1:** e copie o valor. Se aparecer "This build uses a Java 8 JVM", use a Opção A (keytool) ou defina `JAVA_HOME` para um JDK 11+ (ex.: o que vem com o Android Studio).

### 2. Registrar no Firebase

1. Acesse [Firebase Console](https://console.firebase.google.com) → seu projeto (**bibliasagrada-e602c**).
2. **Configurações do projeto** (ícone de engrenagem) → **Geral**.
3. Em **Seus apps**, selecione o app Android (`com.bibliasagrada.app`).
4. Clique em **Adicionar impressão digital** e cole o **SHA-1** (e, se quiser, o **SHA-256** do mesmo relatório).
5. Salve. Aguarde alguns minutos e teste o login de novo.

### 3. Release / Google Play

Para build de release, use o SHA-1 do keystore de release. Se usar **Google Play App Signing**, pegue o SHA-1 em **Play Console → Release → Configuração do app → Integridade do app** e adicione também no Firebase.

---

## Web Client ID para Google Sign-In (obrigatório no Android)

Além do SHA-1, o **Firebase Auth** exige que o app use o **Web Client ID** no Google Sign-In. Sem isso, o login pode continuar falhando com **ApiException código 10**.

### 1. Obter o Web Client ID

- **Opção A – Firebase Console:** Configurações do projeto → Geral → em **Seus apps**, se existir um app **Web**, use o **ID do cliente** (formato `xxxxx.apps.googleusercontent.com`).
- **Opção B – Google Cloud Console:** [console.cloud.google.com](https://console.cloud.google.com) → selecione o projeto **bibliasagrada-e602c** (ou o do Firebase) → **APIs e serviços** → **Credenciais** → em **OAuth 2.0 – IDs de cliente**, procure **"Cliente da Web (criado automaticamente para o Google Sign-in)"** e copie o **ID do cliente**.

### 2. Configurar no app

Abra `lib/core/constants/firebase_config.dart` e substitua o valor de `kGoogleSignInWebClientId` pelo ID que você copiou (mantenha as aspas):

```dart
const String kGoogleSignInWebClientId =
    '1025159376677-xxxxxxxxxxxx.apps.googleusercontent.com';  // seu ID real
```

Salve, faça um novo build e teste o login com Google.

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| **Falha no login via Google: ApiException código 10** | 1) Adicione o **SHA-1** do certificado no Firebase (seção **SHA-1 para Google Sign-In**). 2) Configure o **Web Client ID** em `lib/core/constants/firebase_config.dart` (seção **Web Client ID** acima). |
| `flutter` não reconhecido | Adicione o Flutter ao PATH ou execute o script no terminal do Android Studio |
| Erro de plugin google-services | Verifique se `google-services.json` está em `android/app/` |
| applicationId não coincide | O package no Firebase Console deve ser `com.bibliasagrada.app` |
