# Setup Flutter Android + Firebase
# Execute este script no diretório bible-app-mobile (ou a partir da raiz do projeto)
# Requer: Flutter no PATH

$ErrorActionPreference = "Stop"
$mobileDir = $PSScriptRoot
Set-Location $mobileDir

Write-Host "=== Setup Flutter + Firebase para Biblia Sagrada ===" -ForegroundColor Cyan

# 1. Verificar Flutter
$flutterCmd = Get-Command flutter -ErrorAction SilentlyContinue
if (-not $flutterCmd) {
    Write-Host "ERRO: Flutter nao encontrado no PATH." -ForegroundColor Red
    Write-Host "Instale o Flutter e adicione ao PATH, ou execute este script no terminal do Android Studio." -ForegroundColor Yellow
    Write-Host "https://docs.flutter.dev/get-started/install" -ForegroundColor Yellow
    exit 1
}

# 2. Flutter create (gera android/ e ios/)
Write-Host "`n[1/3] Gerando estrutura Android/iOS com flutter create..." -ForegroundColor Green
flutter create . --org com.bibliasagrada

if (-not (Test-Path "android\app\build.gradle") -and -not (Test-Path "android\app\build.gradle.kts")) {
    Write-Host "ERRO: flutter create nao gerou a estrutura android corretamente." -ForegroundColor Red
    exit 1
}

# 3. Garantir google-services.json no lugar
$googleServicesSrc = Join-Path (Split-Path $mobileDir -Parent) "google-services (1).json"
if (-not (Test-Path "android\app\google-services.json") -and (Test-Path $googleServicesSrc)) {
    Copy-Item $googleServicesSrc "android\app\google-services.json"
    Write-Host "google-services.json copiado para android/app/" -ForegroundColor Green
}

# 4. Configurar Firebase: settings.gradle.kts ou build.gradle (projeto)
Write-Host "`n[2/3] Configurando Firebase no projeto Android..." -ForegroundColor Green
$settingsKts = "android\settings.gradle.kts"
$rootBuildGradle = "android\build.gradle"
$rootBuildKts = "android\build.gradle.kts"

if (Test-Path $settingsKts) {
    $content = Get-Content $settingsKts -Raw
    if ($content -notmatch "google-services") {
        $content = $content -replace '(id\("org\.jetbrains\.kotlin\.android"\) version "[^"]+" apply false)', "`$1`n    id(`"com.google.gms.google-services`") version `"4.4.2`" apply false"
        Set-Content $settingsKts $content -NoNewline
        Write-Host "Plugin google-services adicionado em settings.gradle.kts." -ForegroundColor Green
    } else { Write-Host "Plugin google-services ja configurado." -ForegroundColor Gray }
} elseif (Test-Path $rootBuildGradle) {
    $content = Get-Content $rootBuildGradle -Raw
    if ($content -notmatch "google-services") {
        $content = $content -replace "(classpath ['\`"]com\.android\.tools\.build:gradle:[^'\`"]+['\`"])", "`$1`n        classpath 'com.google.gms:google-services:4.4.2'"
        Set-Content $rootBuildGradle $content -NoNewline
        Write-Host "Plugin google-services adicionado ao build.gradle." -ForegroundColor Green
    } else { Write-Host "Plugin google-services ja configurado." -ForegroundColor Gray }
}

# 5. Configurar Firebase no app (build.gradle.kts ou build.gradle)
Write-Host "`n[3/3] Configurando Firebase no android/app/..." -ForegroundColor Green
$appBuildGradle = "android\app\build.gradle"
$appBuildKts = "android\app\build.gradle.kts"

if (Test-Path $appBuildKts) {
    $appContent = Get-Content $appBuildKts -Raw
    $appContent = $appContent -replace 'applicationId\s*=\s*"[^"]*"', 'applicationId = "com.bibliasagrada.app"'
    if ($appContent -notmatch "google-services") {
        $appContent = $appContent -replace '(id\("dev\.flutter\.flutter-gradle-plugin"\))', "`$1`n    id(`"com.google.gms.google-services`")"
    }
    Set-Content $appBuildKts $appContent -NoNewline
    Write-Host "applicationId e plugin google-services configurados em app/build.gradle.kts." -ForegroundColor Green
} elseif (Test-Path $appBuildGradle) {
    $appContent = Get-Content $appBuildGradle -Raw
    $appContent = $appContent -replace 'applicationId\s+["'']([^"'']+)["'']', 'applicationId "com.bibliasagrada.app"'
    if ($appContent -notmatch "google-services") {
        $appContent = $appContent.TrimEnd() + "`n`napply plugin: 'com.google.gms.google-services'"
        Set-Content $appBuildGradle $appContent -NoNewline
    }
    Write-Host "applicationId e plugin google-services configurados em app/build.gradle." -ForegroundColor Green
}

# 6. flutter pub get
Write-Host "`n[4/4] Executando flutter pub get..." -ForegroundColor Green
flutter pub get

# 7. Lembrete SHA-1 para Google Sign-In
Write-Host "`n=== Setup concluido! ===" -ForegroundColor Cyan
Write-Host "Para rodar o app: flutter run" -ForegroundColor Yellow
Write-Host "`nSe for usar Login com Google, adicione o SHA-1 no Firebase:" -ForegroundColor Yellow
Write-Host "  keytool -list -v -alias androiddebugkey -keystore %USERPROFILE%\.android\debug.keystore" -ForegroundColor Gray
Write-Host "  (senha: android). Copie o SHA1 e adicione em Firebase Console > Configuracoes > Seu app Android." -ForegroundColor Gray
Write-Host "  Ou: cd bible-app-mobile\android; .\gradlew signingReport (requer Java 11+). Veja SETUP-FIREBASE.md." -ForegroundColor Gray
