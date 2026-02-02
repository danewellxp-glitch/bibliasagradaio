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

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `flutter` não reconhecido | Adicione o Flutter ao PATH ou execute o script no terminal do Android Studio |
| Erro de plugin google-services | Verifique se `google-services.json` está em `android/app/` |
| applicationId não coincide | O package no Firebase Console deve ser `com.bibliasagrada.app` |
