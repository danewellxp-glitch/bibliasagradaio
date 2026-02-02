/// Configuração Firebase / Google Sign-In.
///
/// Para Login com Google funcionar no Android, você precisa:
/// 1. SHA-1 do keystore no Firebase (Configurações > Seu app Android).
/// 2. Web Client ID abaixo (obtido no Google Cloud Console).
///
/// Como obter o Web Client ID:
/// - Firebase Console > Configurações do projeto > Geral > Seus apps.
/// - Se existir um app "Web", use o "ID do cliente" dele.
/// - Se não existir: Google Cloud Console (link do projeto) > APIs e serviços >
///   Credenciais > procure "Cliente da Web (criado automaticamente para o Google Sign-in)"
///   e copie o "ID do cliente" (formato: xxxxx-xxx.apps.googleusercontent.com).
const String kGoogleSignInWebClientId =
    '1025159376677-6uv7n52t7f1blf79bbta04lr20aclr2u.apps.googleusercontent.com';
