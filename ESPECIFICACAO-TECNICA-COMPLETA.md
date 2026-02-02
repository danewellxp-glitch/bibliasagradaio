# App Bíblico Inteligente - Especificação Técnica Completa

## 📋 RESUMO EXECUTIVO

**Projeto:** App Bíblico Multiplataforma com IA  
**Equipe:** 3 desenvolvedores  
**Timeline MVP:** 2 meses  
**Plataformas:** Android + iOS (Flutter)  
**Modelo:** Freemium (básico gratuito, recursos premium pagos)  
**Infraestrutura:** Auto-hosted (servidor próprio)

---

## 🎯 OBJETIVOS DO MVP (2 MESES)

Criar aplicativo bíblico completo focando em:
1. Leitura bíblica rica e personalizável
2. Sistema de estudos com recursos educacionais
3. Quiz gamificado para aprendizado
4. Sincronização entre dispositivos
5. Base sólida para expansão futura com IA

**Funcionalidades de IA ficam para FASE 2/3:**
- Análise de pregações com IA
- Chat bíblico inteligente
- Sugestões personalizadas avançadas

---

## 🏗️ ARQUITETURA TÉCNICA DEFINIDA

### Stack Tecnológica

```
┌─────────────────────────────────────────────────────┐
│                   MOBILE APP                        │
│                    Flutter                          │
│              (Android + iOS)                        │
└─────────────────┬───────────────────────────────────┘
                  │
                  │ HTTP/REST
                  │
┌─────────────────▼───────────────────────────────────┐
│                 BACKEND API                         │
│            Python (FastAPI/Django)                  │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐              │
│  │ PostgreSQL   │  │  MongoDB     │              │
│  │ (Estruturado)│  │ (Flexível)   │              │
│  └──────────────┘  └──────────────┘              │
│                                                     │
│  ┌──────────────────────────────────┐             │
│  │    Firebase Services             │             │
│  │  - Authentication                │             │
│  │  - Analytics                     │             │
│  │  - Cloud Messaging (push)        │             │
│  └──────────────────────────────────┘             │
└─────────────────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│          SERVIDOR AUTO-HOSTED                       │
│                                                     │
│  Hardware: i3, 8GB RAM, 500GB, 500Mbps             │
│                                                     │
│  Futuro (Fase 2):                                  │
│  - Llama 3.1 (IA local)                            │
│  - Whisper (transcrição)                           │
│  - Vector DB para embeddings                       │
└─────────────────────────────────────────────────────┘
```

### Repositórios Git (Separados)

```
GitHub Organization: seu-usuario/bible-app

├── bible-app-mobile/          (Flutter - Mobile)
├── bible-app-backend/         (Python - API)
├── bible-app-admin/           (Opcional - Painel admin)
└── bible-app-docs/            (Documentação)
```

---

## 📱 ESTRUTURA DO APP FLUTTER

### Navegação Principal

```dart
Bottom Navigation Bar (5 tabs):
1. 📖 Bíblia
2. 📚 Estudos
3. 🎙️ Pregações (FASE 2 - mostrar "Em breve")
4. 🎯 Quiz
5. 👤 Perfil
```

### Arquitetura Flutter Recomendada

```
lib/
├── core/
│   ├── constants/
│   ├── theme/
│   ├── utils/
│   └── services/
│       ├── api_service.dart
│       ├── auth_service.dart
│       ├── storage_service.dart
│       └── sync_service.dart
├── data/
│   ├── models/
│   ├── repositories/
│   └── providers/
├── features/
│   ├── auth/
│   │   ├── screens/
│   │   ├── widgets/
│   │   └── providers/
│   ├── bible/
│   │   ├── screens/
│   │   │   ├── bible_reader_screen.dart
│   │   │   ├── bible_search_screen.dart
│   │   │   └── verse_detail_screen.dart
│   │   ├── widgets/
│   │   │   ├── verse_card.dart
│   │   │   ├── highlight_menu.dart
│   │   │   └── annotation_dialog.dart
│   │   └── providers/
│   ├── study/
│   │   ├── screens/
│   │   ├── widgets/
│   │   └── providers/
│   ├── quiz/
│   │   ├── screens/
│   │   ├── widgets/
│   │   └── providers/
│   └── profile/
│       ├── screens/
│       ├── widgets/
│       └── providers/
└── main.dart
```

**State Management:** Provider ou Riverpod (recomendado)

---

## 🗄️ MODELAGEM DE DADOS

### PostgreSQL - Dados Estruturados

```sql
-- USUÁRIOS E AUTENTICAÇÃO
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    firebase_uid VARCHAR(128) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    photo_url TEXT,
    preferred_version VARCHAR(10) DEFAULT 'ARA',
    preferred_language VARCHAR(5) DEFAULT 'pt-BR',
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- VERSÕES DA BÍBLIA
CREATE TABLE bible_versions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL, -- ARA, ARC, KJV, etc.
    name VARCHAR(100) NOT NULL,
    language VARCHAR(5) NOT NULL, -- pt-BR, en-US
    description TEXT,
    is_premium BOOLEAN DEFAULT FALSE,
    file_size_mb DECIMAL(10,2),
    is_available_offline BOOLEAN DEFAULT TRUE
);

-- TEXTO BÍBLICO
CREATE TABLE bible_texts (
    id SERIAL PRIMARY KEY,
    version_id INTEGER REFERENCES bible_versions(id),
    book_number INTEGER NOT NULL, -- 1-66
    book_name VARCHAR(50) NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    text TEXT NOT NULL,
    -- Índices para busca rápida
    UNIQUE(version_id, book_number, chapter, verse)
);

CREATE INDEX idx_bible_texts_search ON bible_texts USING GIN(to_tsvector('portuguese', text));
CREATE INDEX idx_bible_texts_reference ON bible_texts(version_id, book_number, chapter, verse);

-- PALAVRAS INTERATIVAS (Strong's) - FASE 2
CREATE TABLE strong_concordance (
    id SERIAL PRIMARY KEY,
    strong_number VARCHAR(10) UNIQUE NOT NULL, -- H1234 ou G5678
    language VARCHAR(2) NOT NULL, -- H=Hebrew, G=Greek
    transliteration VARCHAR(100),
    pronunciation VARCHAR(100),
    definition TEXT NOT NULL,
    etymology TEXT
);

-- DESTAQUES DO USUÁRIO
CREATE TABLE user_highlights (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    version_id INTEGER REFERENCES bible_versions(id),
    book_number INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    color VARCHAR(20) NOT NULL, -- yellow, green, blue, red, purple
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, version_id, book_number, chapter, verse)
);

CREATE INDEX idx_highlights_user ON user_highlights(user_id);

-- ANOTAÇÕES DO USUÁRIO
CREATE TABLE user_annotations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    version_id INTEGER REFERENCES bible_versions(id),
    book_number INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    note TEXT NOT NULL, -- Criptografado end-to-end no app
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_annotations_user ON user_annotations(user_id);

-- FAVORITOS/MARCADORES
CREATE TABLE user_bookmarks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    version_id INTEGER REFERENCES bible_versions(id),
    book_number INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    title VARCHAR(100), -- Título do marcador (opcional)
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, version_id, book_number, chapter, verse)
);

-- PROGRESSO DE LEITURA
CREATE TABLE reading_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    book_number INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    last_verse_read INTEGER,
    completed BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, book_number, chapter)
);

-- QUESTÕES DO QUIZ
CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,
    difficulty_level VARCHAR(20) NOT NULL, -- beginner, intermediate, advanced
    question_type VARCHAR(30) NOT NULL, -- multiple_choice, complete_verse, association
    question_text TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    wrong_answers JSONB, -- Array de respostas erradas para múltipla escolha
    explanation TEXT,
    related_verses JSONB, -- Array de referências bíblicas
    category VARCHAR(50), -- history, theology, geography, etc.
    created_at TIMESTAMP DEFAULT NOW()
);

-- HISTÓRICO DE QUIZ DO USUÁRIO
CREATE TABLE user_quiz_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES quiz_questions(id),
    is_correct BOOLEAN NOT NULL,
    time_taken_seconds INTEGER,
    answered_at TIMESTAMP DEFAULT NOW()
);

-- ESTATÍSTICAS DE QUIZ
CREATE TABLE user_quiz_stats (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    total_xp INTEGER DEFAULT 0,
    current_level INTEGER DEFAULT 1,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_quiz_date DATE,
    total_questions_answered INTEGER DEFAULT 0,
    total_correct_answers INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- CONQUISTAS/BADGES
CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon_url TEXT,
    xp_reward INTEGER DEFAULT 0,
    requirement_type VARCHAR(50), -- streak, questions, reading, etc.
    requirement_value INTEGER
);

CREATE TABLE user_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_id INTEGER REFERENCES achievements(id),
    unlocked_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
);

-- COMENTÁRIOS BÍBLICOS (domínio público)
CREATE TABLE bible_commentaries (
    id SERIAL PRIMARY KEY,
    author VARCHAR(100) NOT NULL,
    book_number INTEGER NOT NULL,
    chapter INTEGER,
    verse_start INTEGER,
    verse_end INTEGER,
    commentary TEXT NOT NULL,
    source VARCHAR(100), -- Matthew Henry, etc.
    language VARCHAR(5) DEFAULT 'pt-BR'
);

CREATE INDEX idx_commentaries_reference ON bible_commentaries(book_number, chapter, verse_start);

-- REFERÊNCIAS CRUZADAS
CREATE TABLE cross_references (
    id SERIAL PRIMARY KEY,
    from_book INTEGER NOT NULL,
    from_chapter INTEGER NOT NULL,
    from_verse INTEGER NOT NULL,
    to_book INTEGER NOT NULL,
    to_chapter INTEGER NOT NULL,
    to_verse INTEGER NOT NULL,
    relationship_type VARCHAR(50) -- parallel, prophecy_fulfillment, quote, theme
);

-- MAPAS BÍBLICOS
CREATE TABLE bible_maps (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    period VARCHAR(100), -- Exodus, Kings, New Testament, etc.
    image_url TEXT NOT NULL,
    related_books JSONB -- Array de números de livros
);

-- LINHA DO TEMPO
CREATE TABLE timeline_events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(200) NOT NULL,
    description TEXT,
    approximate_date VARCHAR(50), -- "1440 BC", "30 AD", etc.
    date_start INTEGER, -- Ano (negativo para AC)
    date_end INTEGER,
    event_type VARCHAR(50), -- exodus, kingdom, exile, etc.
    related_books JSONB,
    related_verses JSONB
);

-- PREGAÇÕES (FASE 2)
CREATE TABLE sermons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    audio_url TEXT,
    audio_duration_seconds INTEGER,
    transcription TEXT, -- Gerado por Whisper
    analyzed_data JSONB, -- Resultado da análise de IA
    related_verses JSONB,
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### MongoDB - Dados Flexíveis

```javascript
// Configurações do usuário (preferências)
{
  _id: ObjectId,
  userId: "firebase_uid",
  preferences: {
    fontSize: 16,
    fontFamily: "Georgia",
    lineHeight: 1.5,
    theme: "dark", // dark, light, sepia
    showVerseNumbers: true,
    showRedLetters: true, // Palavras de Jesus em vermelho
    defaultVersion: "ARA",
    language: "pt-BR"
  },
  notifications: {
    dailyReminder: true,
    reminderTime: "08:00",
    streakReminder: true,
    newFeatures: true
  },
  updatedAt: ISODate
}

// Cache de versículos baixados para offline
{
  _id: ObjectId,
  userId: "firebase_uid",
  versionCode: "ARA",
  books: [
    {
      bookNumber: 1,
      bookName: "Genesis",
      downloaded: true,
      chapters: [...]
    }
  ],
  lastSync: ISODate
}

// Dados de analytics locais (antes de enviar ao Firebase)
{
  _id: ObjectId,
  userId: "firebase_uid",
  sessionId: "unique_session",
  events: [
    {
      eventName: "verse_read",
      timestamp: ISODate,
      properties: {
        book: 1,
        chapter: 1,
        verse: 1
      }
    }
  ],
  synced: false
}
```

---

## 🔐 AUTENTICAÇÃO E SEGURANÇA

### Firebase Authentication

**Métodos de Login no MVP:**
1. ✅ Google Sign-In
2. ✅ Apple Sign-In (obrigatório para iOS)
3. 📧 Email/Password (fallback)

**Fluxo de Autenticação:**

```dart
// 1. Usuário faz login via Firebase
final UserCredential credential = await FirebaseAuth.instance.signInWithGoogle();

// 2. Pegar token do Firebase
final String? idToken = await credential.user?.getIdToken();

// 3. Enviar para backend próprio
final response = await http.post(
  'https://api.seuapp.com/auth/login',
  headers: {'Authorization': 'Bearer $idToken'},
);

// 4. Backend valida token e retorna JWT próprio
final String jwtToken = response.data['token'];

// 5. Usar JWT para todas as requisições subsequentes
```

**Backend (Python FastAPI):**

```python
from fastapi import Depends, HTTPException
from firebase_admin import auth, credentials, initialize_app

# Inicializar Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)

async def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/auth/login")
async def login(firebase_token: str = Depends(verify_firebase_token)):
    # Criar ou buscar usuário no PostgreSQL
    # Retornar JWT próprio para APIs
    pass
```

### Criptografia End-to-End para Anotações

**Estratégia:**
- Anotações são criptografadas no dispositivo ANTES de enviar ao servidor
- Chave de criptografia derivada do UID do usuário + senha mestra
- Servidor armazena dados criptografados (não consegue ler)

```dart
import 'package:encrypt/encrypt.dart';

class EncryptionService {
  final String userKey; // Derivado do Firebase UID
  
  String encrypt(String text) {
    final key = Key.fromUtf8(userKey.padRight(32).substring(0, 32));
    final iv = IV.fromLength(16);
    final encrypter = Encrypter(AES(key));
    return encrypter.encrypt(text, iv: iv).base64;
  }
  
  String decrypt(String encrypted) {
    final key = Key.fromUtf8(userKey.padRight(32).substring(0, 32));
    final iv = IV.fromLength(16);
    final encrypter = Encrypter(AES(key));
    return encrypter.decrypt64(encrypted, iv: iv);
  }
}
```

---

## 📖 FUNCIONALIDADES DETALHADAS - MVP

### 1. ABA BÍBLIA

#### 1.1 Leitura de Versões

**Versões Incluídas:**
- ✅ ARA (Almeida Revista e Atualizada) - Português
- ✅ ARC (Almeida Revista e Corrigida) - Português
- ✅ ACF (Almeida Corrigida Fiel) - Português
- ✅ KJV (King James Version) - Inglês

**Features:**
```dart
// Tela de leitura
- Navegação por livro/capítulo
- Scroll infinito entre capítulos
- Tap no versículo para opções
- Modo leitura contínua ou versículo por versículo
- Ajuste de fonte (12-24px)
- Escolha de fonte (Serif/Sans-serif)
- Ajuste de espaçamento de linha
- Modo escuro/claro/sépia
```

#### 1.2 Sistema de Busca

**Busca Simples:**
- Por livro + capítulo + versículo
- Autocomplete de livros

**Busca Avançada:**
```sql
-- Full-text search no PostgreSQL
SELECT book_name, chapter, verse, text
FROM bible_texts
WHERE version_id = ? 
  AND to_tsvector('portuguese', text) @@ plainto_tsquery('portuguese', ?)
ORDER BY book_number, chapter, verse
LIMIT 50;
```

**Filtros:**
- Testamento (AT/NT)
- Livro específico
- Resultados por relevância

#### 1.3 Destaques e Anotações

**Destaques (5 cores):**
```dart
enum HighlightColor {
  yellow,
  green,
  blue,
  red,
  purple
}

// Widget de menu ao selecionar texto
Widget buildHighlightMenu() {
  return Row(
    children: [
      HighlightButton(color: HighlightColor.yellow),
      HighlightButton(color: HighlightColor.green),
      // ...
      AnnotationButton(),
      BookmarkButton(),
      ShareButton(),
    ],
  );
}
```

**Anotações:**
- Dialog para escrever nota
- Markdown support (opcional)
- Timestamp automático
- Sincronização criptografada

#### 1.4 Download Offline

**Estratégia:**
- Cada versão da Bíblia = ~5MB
- Download via API em chunks
- Armazenamento em SQLite local (sqflite)
- Sincronização de preferências via MongoDB

```dart
class OfflineBibleService {
  Future<void> downloadVersion(String versionCode) async {
    // 1. Baixar JSON da API
    final response = await api.get('/bible/$versionCode/download');
    
    // 2. Salvar no SQLite local
    final db = await database;
    await db.transaction((txn) async {
      for (var verse in response.data) {
        await txn.insert('bible_texts_offline', verse);
      }
    });
    
    // 3. Marcar versão como disponível offline
    await prefs.setBool('offline_$versionCode', true);
  }
}
```

#### 1.5 Compartilhar Versículos

**Opções de compartilhamento:**

1. **Texto simples**
```
"No princípio, Deus criou os céus e a terra."
Gênesis 1:1 (ARA)
```

2. **Imagem com versículo** (INSPIRAÇÃO YOUVERSION)
```dart
class VerseImageGenerator {
  Future<File> generateImage({
    required String verseText,
    required String reference,
    required String template, // background template
  }) async {
    // Usar pacote: image / flutter_custom_canvas
    // Templates pré-definidos (10-15 opções)
    // Permite customizar: cor, fonte, background
    
    return imageFile;
  }
}
```

Templates de imagem:
- Fundo sólido com gradiente
- Fundo com imagens (natureza, abstratos)
- Minimalista preto e branco
- Colorido moderno

Compartilhar via:
- WhatsApp
- Instagram Stories
- Facebook
- Twitter
- Copiar para clipboard

---

### 2. ABA ESTUDOS

#### 2.1 Comentários Bíblicos

**Fontes (domínio público):**
- Matthew Henry Commentary (traduzido)
- Adam Clarke Commentary
- John Gill's Exposition
- Barnes' Notes

**Implementação:**
```dart
class CommentaryScreen extends StatelessWidget {
  final int book, chapter, verse;
  
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Commentary>>(
      future: api.getCommentaries(book, chapter, verse),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return LoadingIndicator();
        
        return ListView.builder(
          itemCount: snapshot.data!.length,
          itemBuilder: (context, index) {
            final commentary = snapshot.data![index];
            return CommentaryCard(
              author: commentary.author,
              text: commentary.text,
              source: commentary.source,
            );
          },
        );
      },
    );
  }
}
```

#### 2.2 Referências Cruzadas

**Base de dados:**
- Treasury of Scripture Knowledge (TSK)
- Cross-references da Bíblia de Estudo

**UI:**
```dart
// Na tela de versículo
Widget buildCrossReferences() {
  return ExpansionTile(
    title: Text('Referências Cruzadas (12)'),
    children: [
      CrossRefCard(
        reference: 'João 3:16',
        relationship: 'Tema relacionado',
        onTap: () => navigateToVerse(43, 3, 16),
      ),
      // ...
    ],
  );
}
```

#### 2.3 Linha do Tempo Histórica

**Visualização:**
- Linha do tempo interativa (ScrollView horizontal)
- Eventos principais (Criação, Êxodo, Reis, Exílio, Jesus, Apóstolos)
- Tap no evento mostra detalhes + versículos relacionados

```dart
class TimelineEvent {
  final String name;
  final String description;
  final int year; // Negativo para AC
  final List<VerseReference> relatedVerses;
  final String period; // "Patriarcas", "Reino Unido", etc.
}
```

#### 2.4 Mapas Bíblicos

**Mapas incluídos (imagens estáticas):**
- Mundo antigo (época de Abraão)
- Êxodo do Egito
- Reino de Israel (Davi/Salomão)
- Divisão do reino
- Impérios (Assírio, Babilônico, Persa, Grego, Romano)
- Viagens de Paulo
- Jerusalém (diferentes épocas)

**Implementação:**
```dart
class MapViewer extends StatelessWidget {
  final BibleMap map;
  
  @override
  Widget build(BuildContext context) {
    return InteractiveViewer( // Zoom e pan
      child: Image.network(map.imageUrl),
    );
  }
}
```

#### 2.5 Palavras Interativas (Strong's)

**IMPLEMENTAÇÃO NO MVP - SIMPLIFICADA:**

Ao invés de TODAS as palavras, começar com:
- Apenas palavras-chave importantes (Deus, amor, salvação, fé, graça, etc.)
- ~500 palavras mais frequentes/importantes
- Destacadas com sublinhado pontilhado

```dart
Widget buildVerseWithStrongWords(String verseText) {
  // Parse do texto identificando palavras no dicionário
  // Exemplo: "Porque Deus [STRONG_G2316] amou [STRONG_G25] o mundo..."
  
  return RichText(
    text: TextSpan(
      children: [
        TextSpan(text: 'Porque '),
        WidgetSpan(
          child: StrongWordWidget(
            word: 'Deus',
            strongNumber: 'G2316',
            onTap: () => showStrongDialog('G2316'),
          ),
        ),
        // ...
      ],
    ),
  );
}
```

**Dialog de palavra:**
```dart
class StrongWordDialog {
  final String strongNumber; // G2316
  final String originalWord; // θεός (Theos)
  final String transliteration; // Theos
  final String definition;
  final List<VerseReference> otherOccurrences;
}
```

**Base de dados Strong's:**
- Baixar JSON completo de projeto open-source
- Popular no PostgreSQL
- ~15.000 palavras (Hebraico + Grego)

---

### 3. ABA PREGAÇÕES (FASE 2 - EM BREVE)

**No MVP:**
```dart
class SermonsTab extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.mic_none, size: 80, color: Colors.grey),
          SizedBox(height: 20),
          Text(
            'Análise de Pregações com IA',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 10),
          Text(
            'Em breve você poderá gravar e analisar\npregações com Inteligência Artificial',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey),
          ),
          SizedBox(height: 30),
          ElevatedButton(
            onPressed: () => showPremiumDialog(),
            child: Text('Notifique-me quando estiver pronto'),
          ),
        ],
      ),
    );
  }
}
```

---

### 4. ABA QUIZ

#### 4.1 Sistema de Gamificação

**Níveis e XP:**
```dart
class QuizStats {
  int totalXP = 0;
  int currentLevel = 1;
  int currentStreak = 0;
  int longestStreak = 0;
  
  // Fórmula de XP para próximo nível
  int xpForNextLevel() {
    return currentLevel * 100; // Nível 1 = 100 XP, Nível 2 = 200 XP, etc.
  }
  
  // XP ganho por questão
  int xpReward({required bool isCorrect, required String difficulty}) {
    if (!isCorrect) return 0;
    
    switch (difficulty) {
      case 'beginner':
        return 10;
      case 'intermediate':
        return 20;
      case 'advanced':
        return 30;
      default:
        return 10;
    }
  }
}
```

**Streaks:**
```dart
class StreakManager {
  Future<void> checkDailyQuiz(String userId) async {
    final lastQuizDate = await getLastQuizDate(userId);
    final today = DateTime.now();
    
    if (lastQuizDate == null) {
      // Primeiro quiz
      await updateStreak(userId, 1);
    } else if (isYesterday(lastQuizDate)) {
      // Mantém streak
      final currentStreak = await getCurrentStreak(userId);
      await updateStreak(userId, currentStreak + 1);
    } else if (!isToday(lastQuizDate)) {
      // Perdeu o streak
      await updateStreak(userId, 0);
    }
  }
}
```

**UI do Sistema de Níveis:**
```dart
Widget buildLevelProgress() {
  return Column(
    children: [
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text('Nível $currentLevel', style: boldStyle),
          Text('$currentXP / ${xpForNextLevel()} XP'),
        ],
      ),
      LinearProgressIndicator(
        value: currentXP / xpForNextLevel(),
      ),
      SizedBox(height: 20),
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          StatCard(icon: Icons.local_fire_department, 
                   label: 'Streak', 
                   value: '$currentStreak dias'),
          StatCard(icon: Icons.check_circle, 
                   label: 'Acertos', 
                   value: '$correctPercentage%'),
        ],
      ),
    ],
  );
}
```

#### 4.2 Tipos de Questões

**1. Múltipla Escolha:**
```dart
class MultipleChoiceQuestion {
  final String question;
  final String correctAnswer;
  final List<String> wrongAnswers;
  final String explanation;
  final List<VerseReference> relatedVerses;
}

// Exemplo
{
  "question": "Quem foi o primeiro rei de Israel?",
  "correctAnswer": "Saul",
  "wrongAnswers": ["Davi", "Salomão", "Samuel"],
  "explanation": "Saul foi ungido por Samuel como primeiro rei...",
  "relatedVerses": [{"book": 9, "chapter": 10, "verse": 1}]
}
```

**2. Complete o Versículo:**
```dart
class CompleteVerseQuestion {
  final String versePrefix; // "Porque Deus amou o mundo de tal maneira..."
  final String missingPart; // "que deu o seu Filho unigênito"
  final List<String> options; // 4 opções de completar
  final VerseReference reference;
}
```

**3. Associação:**
```dart
class AssociationQuestion {
  final String type; // "person_to_event", "book_to_author", etc.
  final List<String> leftColumn;
  final List<String> rightColumn;
  final Map<String, String> correctMatches;
}

// Exemplo: Associe o profeta ao seu livro
// Isaías -> Livro de Isaías
// Jeremias -> Livro de Jeremias
```

#### 4.3 Níveis de Dificuldade

**Beginner (Iniciante):**
- Histórias conhecidas (Noé, Moisés, Davi, Jesus)
- Personagens principais
- Eventos marcantes
- Versículos famosos

**Intermediate (Intermediário):**
- Profetas menores
- Cronologia
- Geografia
- Temas teológicos básicos
- Parábolas e milagres

**Advanced (Avançado):**
- Teologia sistemática
- Contexto histórico detalhado
- Idiomas originais (básico)
- Exegese
- Conexões AT-NT complexas

#### 4.4 Algoritmo de Adaptação

```dart
class AdaptiveQuizEngine {
  Future<Question> getNextQuestion(String userId) async {
    final stats = await getUserStats(userId);
    final recentPerformance = await getRecentPerformance(userId, limit: 10);
    
    // Se acertou >80% das últimas 10, aumenta dificuldade
    if (recentPerformance.correctPercentage > 0.8) {
      return getQuestionOfDifficulty(stats.currentLevel + 1);
    }
    
    // Se acertou <50%, diminui dificuldade
    if (recentPerformance.correctPercentage < 0.5) {
      return getQuestionOfDifficulty(max(1, stats.currentLevel - 1));
    }
    
    // Senão, mantém nível atual
    return getQuestionOfDifficulty(stats.currentLevel);
  }
}
```

#### 4.5 Ranking (Opcional)

**Leaderboards:**
- Ranking global (todos os usuários)
- Ranking de amigos (se implementar social)
- Ranking semanal
- Ranking mensal

```dart
class Leaderboard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<UserRank>>(
      future: api.getLeaderboard(period: 'weekly'),
      builder: (context, snapshot) {
        return ListView.builder(
          itemCount: snapshot.data!.length,
          itemBuilder: (context, index) {
            final rank = snapshot.data![index];
            return LeaderboardCard(
              position: index + 1,
              username: rank.displayName,
              xp: rank.totalXP,
              isCurrentUser: rank.userId == currentUserId,
            );
          },
        );
      },
    );
  }
}
```

---

### 5. ABA PERFIL

#### 5.1 Estatísticas de Leitura

```dart
class ReadingStats {
  int totalChaptersRead;
  int totalVersesRead;
  double bibleCompletionPercentage; // % da Bíblia lida
  Map<String, int> booksRead; // {"Genesis": 50, "Exodus": 40, ...}
  int currentStreak; // Dias consecutivos lendo
  int longestStreak;
  DateTime? lastReadDate;
  
  // Visualizações
  Widget buildBibleProgressChart() {
    return CircularPercentIndicator(
      percent: bibleCompletionPercentage / 100,
      radius: 120,
      lineWidth: 15,
      center: Text('${bibleCompletionPercentage.toInt()}%'),
      progressColor: Colors.blue,
    );
  }
  
  Widget buildBookProgressList() {
    return ListView(
      children: [
        BookProgressCard(book: 'Gênesis', progress: 0.5),
        BookProgressCard(book: 'Êxodo', progress: 0.3),
        // ...
      ],
    );
  }
}
```

#### 5.2 Estatísticas de Quiz

```dart
class QuizStatsWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        StatCard(
          title: 'Total de Questões',
          value: stats.totalQuestions.toString(),
          icon: Icons.quiz,
        ),
        StatCard(
          title: 'Taxa de Acerto',
          value: '${stats.correctPercentage}%',
          icon: Icons.check_circle,
        ),
        StatCard(
          title: 'Nível Atual',
          value: stats.currentLevel.toString(),
          icon: Icons.emoji_events,
        ),
        StatCard(
          title: 'XP Total',
          value: stats.totalXP.toString(),
          icon: Icons.star,
        ),
        
        // Gráfico de progresso (última semana)
        WeeklyProgressChart(data: stats.last7Days),
        
        // Conquistas desbloqueadas
        AchievementsGrid(achievements: stats.unlockedAchievements),
      ],
    );
  }
}
```

#### 5.3 Configurações

```dart
class SettingsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        // LEITURA
        SettingsSection(
          title: 'Preferências de Leitura',
          children: [
            DropdownSetting(
              label: 'Versão Padrão',
              options: ['ARA', 'ARC', 'ACF', 'KJV'],
              currentValue: prefs.defaultVersion,
            ),
            SliderSetting(
              label: 'Tamanho da Fonte',
              min: 12,
              max: 24,
              currentValue: prefs.fontSize,
            ),
            DropdownSetting(
              label: 'Tema',
              options: ['Claro', 'Escuro', 'Sépia'],
              currentValue: prefs.theme,
            ),
            SwitchSetting(
              label: 'Números de Versículos',
              value: prefs.showVerseNumbers,
            ),
          ],
        ),
        
        // NOTIFICAÇÕES
        SettingsSection(
          title: 'Notificações',
          children: [
            SwitchSetting(
              label: 'Lembrete Diário',
              value: prefs.dailyReminder,
            ),
            TimeSetting(
              label: 'Horário do Lembrete',
              currentTime: prefs.reminderTime,
            ),
            SwitchSetting(
              label: 'Lembrete de Streak',
              value: prefs.streakReminder,
            ),
          ],
        ),
        
        // IDIOMA
        SettingsSection(
          title: 'Idioma',
          children: [
            DropdownSetting(
              label: 'Idioma da Interface',
              options: ['Português', 'English'],
              currentValue: prefs.language,
            ),
          ],
        ),
        
        // CONTA
        SettingsSection(
          title: 'Conta',
          children: [
            ListTile(
              title: Text('Exportar Dados'),
              trailing: Icon(Icons.download),
              onTap: () => exportUserData(),
            ),
            ListTile(
              title: Text('Excluir Conta'),
              trailing: Icon(Icons.delete_forever),
              textColor: Colors.red,
              onTap: () => confirmDeleteAccount(),
            ),
          ],
        ),
        
        // SOBRE
        SettingsSection(
          title: 'Sobre',
          children: [
            ListTile(
              title: Text('Versão'),
              trailing: Text('1.0.0'),
            ),
            ListTile(
              title: Text('Termos de Uso'),
              trailing: Icon(Icons.arrow_forward_ios),
            ),
            ListTile(
              title: Text('Política de Privacidade'),
              trailing: Icon(Icons.arrow_forward_ios),
            ),
          ],
        ),
      ],
    );
  }
}
```

#### 5.4 Gestão de Conteúdo Offline

```dart
class OfflineManagementScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        Text('Versões Baixadas', style: headerStyle),
        BibleVersionCard(
          version: 'ARA',
          isDownloaded: true,
          size: '4.2 MB',
          onDelete: () => deleteVersion('ARA'),
        ),
        BibleVersionCard(
          version: 'ARC',
          isDownloaded: false,
          size: '4.5 MB',
          onDownload: () => downloadVersion('ARC'),
        ),
        // ...
        
        Divider(),
        
        Text('Espaço Utilizado', style: headerStyle),
        Text('Total: 8.7 MB de 500 MB'),
        LinearProgressIndicator(value: 0.017),
      ],
    );
  }
}
```

---

## 🎨 DESIGN E UI/UX

### Paleta de Cores

```dart
class AppColors {
  // Cores Primárias
  static const primary = Color(0xFF4A5FC1); // Azul profundo
  static const primaryDark = Color(0xFF2E3B8E);
  static const primaryLight = Color(0xFF6B7AD6);
  
  // Cores Secundárias
  static const secondary = Color(0xFFD4AF37); // Dourado
  static const secondaryDark = Color(0xFFB8941F);
  
  // Cores de Destaque
  static const success = Color(0xFF4CAF50); // Verde
  static const error = Color(0xFFE53935); // Vermelho
  static const warning = Color(0xFFFF9800); // Laranja
  static const info = Color(0xFF2196F3); // Azul claro
  
  // Cores de Destaque (Highlights)
  static const highlightYellow = Color(0xFFFFEB3B);
  static const highlightGreen = Color(0xFF8BC34A);
  static const highlightBlue = Color(0xFF03A9F4);
  static const highlightRed = Color(0xFFEF5350);
  static const highlightPurple = Color(0xFF9C27B0);
  
  // Temas
  static const lightBackground = Color(0xFFFAFAFA);
  static const darkBackground = Color(0xFF121212);
  static const sepiaBackground = Color(0xFFF4ECD8);
}
```

### Tipografia

```dart
class AppTypography {
  // Leitura da Bíblia
  static const reading = TextStyle(
    fontFamily: 'Georgia', // Serif para leitura
    fontSize: 16,
    height: 1.6,
    color: Colors.black87,
  );
  
  // Interface
  static const interface = TextStyle(
    fontFamily: 'Roboto', // Sans-serif para UI
    fontSize: 14,
  );
  
  // Títulos
  static const title = TextStyle(
    fontFamily: 'Roboto',
    fontSize: 24,
    fontWeight: FontWeight.bold,
  );
  
  // Referências (Gênesis 1:1)
  static const reference = TextStyle(
    fontFamily: 'Roboto',
    fontSize: 12,
    fontWeight: FontWeight.w500,
    color: Colors.grey,
  );
}
```

### Temas (Light/Dark/Sepia)

```dart
ThemeData lightTheme = ThemeData(
  brightness: Brightness.light,
  primaryColor: AppColors.primary,
  scaffoldBackgroundColor: AppColors.lightBackground,
  colorScheme: ColorScheme.light(
    primary: AppColors.primary,
    secondary: AppColors.secondary,
  ),
);

ThemeData darkTheme = ThemeData(
  brightness: Brightness.dark,
  primaryColor: AppColors.primaryLight,
  scaffoldBackgroundColor: AppColors.darkBackground,
  colorScheme: ColorScheme.dark(
    primary: AppColors.primaryLight,
    secondary: AppColors.secondary,
  ),
);

ThemeData sepiaTheme = ThemeData(
  brightness: Brightness.light,
  primaryColor: AppColors.primary,
  scaffoldBackgroundColor: AppColors.sepiaBackground,
  colorScheme: ColorScheme.light(
    primary: AppColors.primary,
    secondary: AppColors.secondary,
    background: AppColors.sepiaBackground,
  ),
);
```

### Componentes Reutilizáveis

```dart
// Cartão de versículo
class VerseCard extends StatelessWidget {
  final String verseText;
  final String reference;
  final Color? highlightColor;
  final VoidCallback? onTap;
  
  @override
  Widget build(BuildContext context) {
    return Card(
      color: highlightColor?.withOpacity(0.3),
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(verseText, style: AppTypography.reading),
              SizedBox(height: 8),
              Text(reference, style: AppTypography.reference),
            ],
          ),
        ),
      ),
    );
  }
}

// Botão de ação principal
class PrimaryButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  final bool isLoading;
  
  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.primary,
        padding: EdgeInsets.symmetric(horizontal: 32, vertical: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      child: isLoading
          ? CircularProgressIndicator(color: Colors.white)
          : Text(label, style: TextStyle(fontSize: 16)),
    );
  }
}
```

### Referências de Design

**Apps para inspiração:**
1. **YouVersion Bible App**
   - Navegação limpa
   - Cards de versículos
   - Compartilhamento de imagens
   
2. **Duolingo**
   - Sistema de gamificação
   - Animações de progresso
   - Feedback visual imediato

3. **Medium**
   - Tipografia para leitura
   - Espaçamento e respiração
   - Modo escuro elegante

**UI Kits Open Source:**
- Material Design 3 (Flutter)
- Fluent Design (Microsoft)
- Eva Design System
- Ant Design Mobile

---

## 🔄 SINCRONIZAÇÃO DE DADOS

### Estratégia de Sync

```dart
class SyncService {
  // 1. Sincronização ao abrir app
  Future<void> syncOnAppStart() async {
    if (!await hasInternetConnection()) return;
    
    await Future.wait([
      syncHighlights(),
      syncAnnotations(),
      syncBookmarks(),
      syncReadingProgress(),
      syncQuizHistory(),
      syncSettings(),
    ]);
  }
  
  // 2. Sincronização em tempo real (após cada ação)
  Future<void> syncHighlight(Highlight highlight) async {
    // Salvar localmente primeiro (offline-first)
    await localDB.saveHighlight(highlight);
    
    // Tentar sincronizar com servidor
    try {
      await api.syncHighlight(highlight);
      await localDB.markAsSynced(highlight.id);
    } catch (e) {
      // Manter na fila de sincronização
      await syncQueue.add(highlight);
    }
  }
  
  // 3. Resolver conflitos (last-write-wins)
  Future<void> resolveConflicts() async {
    final localData = await localDB.getUnsynced();
    final serverData = await api.getUpdatedData(lastSyncTimestamp);
    
    for (var item in localData) {
      if (serverData.contains(item)) {
        // Conflito: comparar timestamps
        if (item.updatedAt.isAfter(serverData.updatedAt)) {
          await api.update(item); // Local mais recente
        } else {
          await localDB.update(serverData); // Servidor mais recente
        }
      } else {
        await api.create(item);
      }
    }
  }
}
```

### Offline-First Architecture

```dart
class DataRepository {
  final LocalDatabase localDB;
  final ApiService api;
  
  // Sempre tenta local primeiro, depois API
  Future<List<Verse>> getVerses(int book, int chapter) async {
    // 1. Buscar no cache local
    final cached = await localDB.getVerses(book, chapter);
    if (cached.isNotEmpty) return cached;
    
    // 2. Se não tem, buscar na API
    if (await hasInternetConnection()) {
      final verses = await api.getVerses(book, chapter);
      // Cachear para próxima vez
      await localDB.saveVerses(verses);
      return verses;
    }
    
    // 3. Sem internet e sem cache = erro
    throw OfflineException('Baixe esta versão para ler offline');
  }
}
```

---

## 📊 ANALYTICS E MÉTRICAS

### Firebase Analytics - Eventos Rastreados

```dart
class AnalyticsService {
  final FirebaseAnalytics analytics = FirebaseAnalytics.instance;
  
  // Eventos de leitura
  Future<void> logVerseRead(int book, int chapter, int verse) async {
    await analytics.logEvent(
      name: 'verse_read',
      parameters: {
        'book': book,
        'chapter': chapter,
        'verse': verse,
        'version': currentVersion,
      },
    );
  }
  
  // Eventos de quiz
  Future<void> logQuizCompleted({
    required bool isCorrect,
    required String difficulty,
    required int timeSeconds,
  }) async {
    await analytics.logEvent(
      name: 'quiz_completed',
      parameters: {
        'is_correct': isCorrect,
        'difficulty': difficulty,
        'time_seconds': timeSeconds,
      },
    );
  }
  
  // Eventos de engajamento
  Future<void> logHighlightCreated(String color) async {
    await analytics.logEvent(
      name: 'highlight_created',
      parameters: {'color': color},
    );
  }
  
  Future<void> logAnnotationCreated() async {
    await analytics.logEvent(name: 'annotation_created');
  }
  
  Future<void> logVerseShared(String shareMethod) async {
    await analytics.logEvent(
      name: 'verse_shared',
      parameters: {'method': shareMethod}, // whatsapp, instagram, etc.
    );
  }
  
  // Sessões
  Future<void> logAppOpened() async {
    await analytics.logAppOpen();
  }
  
  Future<void> logScreenView(String screenName) async {
    await analytics.logScreenView(screenName: screenName);
  }
}
```

### Métricas Customizadas (Backend)

```python
# Backend Python - Tracking adicional
from datetime import datetime
from sqlalchemy import func

class AnalyticsController:
    
    async def get_user_metrics(self, user_id: str):
        """Métricas detalhadas do usuário"""
        return {
            # Leitura
            "total_verses_read": await self.count_verses_read(user_id),
            "bible_completion": await self.calculate_completion(user_id),
            "reading_streak": await self.get_reading_streak(user_id),
            "favorite_book": await self.get_most_read_book(user_id),
            
            # Quiz
            "quiz_accuracy": await self.calculate_quiz_accuracy(user_id),
            "total_xp": await self.get_total_xp(user_id),
            "current_level": await self.get_current_level(user_id),
            "quiz_streak": await self.get_quiz_streak(user_id),
            
            # Engajamento
            "total_highlights": await self.count_highlights(user_id),
            "total_annotations": await self.count_annotations(user_id),
            "days_active": await self.count_active_days(user_id),
        }
    
    async def get_global_metrics(self):
        """Métricas globais da plataforma"""
        return {
            "total_users": await self.count_users(),
            "daily_active_users": await self.count_dau(),
            "monthly_active_users": await self.count_mau(),
            "total_verses_read": await self.sum_verses_read(),
            "total_quizzes_completed": await self.count_quizzes(),
            "average_session_duration": await self.avg_session_duration(),
        }
```

### Dashboard de Analytics (Admin)

**Ferramentas:**
- Firebase Console (grátis)
- Metabase (open-source, self-hosted)
- Grafana (open-source, self-hosted)

**Métricas principais a acompanhar:**
1. **Retenção:**
   - D1 (dia 1), D7, D30 retention
   - Churn rate

2. **Engajamento:**
   - DAU/MAU ratio
   - Tempo médio de sessão
   - Funcionalidades mais usadas

3. **Crescimento:**
   - Novos usuários por dia/semana/mês
   - Taxa de conversão (gratuito → premium)

4. **Qualidade:**
   - Crash rate
   - Taxa de erro de API
   - Tempo de resposta das APIs

---

## 🚀 PLANO DE DESENVOLVIMENTO - MVP (2 MESES)

### Divisão de Tarefas (3 Desenvolvedores)

**DEV 1 - Flutter Mobile:**
- Setup inicial do projeto Flutter
- Telas de autenticação (Google/Apple Sign-in)
- Aba Bíblia (leitura, busca, highlights)
- Aba Perfil (estatísticas, configurações)
- Integração com Firebase
- Sincronização de dados

**DEV 2 - Flutter Mobile:**
- Aba Estudos (comentários, mapas, timeline)
- Aba Quiz (perguntas, gamificação, ranking)
- Sistema de notificações
- Download offline
- Compartilhamento de versículos (texto + imagem)

**DEV 3 - Backend Python:**
- Setup da API (FastAPI)
- Modelagem e população do banco de dados
- Endpoints de autenticação
- Endpoints de sincronização
- Endpoints de quiz
- Integração Firebase Admin SDK
- Deploy no servidor auto-hosted

### Cronograma (8 Semanas)

**SEMANA 1-2: FUNDAÇÃO**
- [ ] Setup dos repositórios Git
- [ ] Configuração do ambiente de desenvolvimento
- [ ] Design do banco de dados
- [ ] Criação da API básica (auth + CRUD)
- [ ] Setup do projeto Flutter
- [ ] Integração Firebase Authentication
- [ ] Telas de login/registro

**SEMANA 3-4: ABA BÍBLIA**
- [ ] Popular banco com textos bíblicos (ARA, ARC, ACF, KJV)
- [ ] Implementar leitura de versículos
- [ ] Sistema de busca (versículo + palavra-chave)
- [ ] Highlights (5 cores)
- [ ] Anotações (com criptografia E2E)
- [ ] Favoritos/marcadores
- [ ] Download offline de versões

**SEMANA 5: ABA ESTUDOS**
- [ ] Importar comentários bíblicos (domínio público)
- [ ] Implementar referências cruzadas (TSK)
- [ ] Linha do tempo histórica
- [ ] Mapas bíblicos (imagens estáticas)
- [ ] Palavras interativas (Strong's - versão simplificada)

**SEMANA 6: ABA QUIZ**
- [ ] Banco de questões (100-200 perguntas iniciais)
- [ ] Sistema de XP e níveis
- [ ] Streaks diários
- [ ] Tipos de questões (múltipla escolha, complete versículo)
- [ ] Feedback com explicações
- [ ] Ranking global

**SEMANA 7: ABA PERFIL + POLISH**
- [ ] Estatísticas de leitura
- [ ] Estatísticas de quiz
- [ ] Configurações (tema, fonte, notificações)
- [ ] Sincronização completa
- [ ] Compartilhamento de versículos (texto + imagem)
- [ ] Internacionalização (PT + EN)

**SEMANA 8: TESTES + DEPLOY**
- [ ] Testes de integração
- [ ] Testes em dispositivos reais
- [ ] Correção de bugs
- [ ] Otimização de performance
- [ ] Deploy do backend no servidor
- [ ] Build de APK/IPA
- [ ] Beta testing (TestFlight + Google Play Beta)

---

## 🛠️ FERRAMENTAS E TECNOLOGIAS

### Desenvolvimento

**Frontend (Flutter):**
```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  provider: ^6.1.1
  # ou riverpod: ^2.4.0
  
  # Networking
  dio: ^5.3.3
  http: ^1.1.0
  
  # Local Storage
  sqflite: ^2.3.0
  shared_preferences: ^2.2.2
  hive: ^2.2.3
  
  # Firebase
  firebase_core: ^2.20.0
  firebase_auth: ^4.12.1
  firebase_analytics: ^10.6.1
  firebase_messaging: ^14.7.3
  google_sign_in: ^6.1.5
  sign_in_with_apple: ^5.0.0
  
  # UI Components
  flutter_svg: ^2.0.9
  cached_network_image: ^3.3.0
  shimmer: ^3.0.0
  animations: ^2.0.8
  
  # Utilities
  intl: ^0.18.1
  url_launcher: ^6.2.1
  share_plus: ^7.2.1
  path_provider: ^2.1.1
  permission_handler: ^11.0.1
  
  # Encryption
  encrypt: ^5.0.3
  
  # Image Generation
  image: ^4.1.3
  screenshot: ^2.1.0
  
  # Charts
  fl_chart: ^0.64.0
  percent_indicator: ^4.2.3
```

**Backend (Python):**
```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pymongo==4.5.0
pydantic==2.4.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
firebase-admin==6.2.0
redis==5.0.1
celery==5.3.4

# Para Fase 2 (IA)
llama-cpp-python==0.2.11
openai-whisper==20231117
sentence-transformers==2.2.2
```

**DevOps:**
- Docker & Docker Compose
- Nginx (reverse proxy)
- PostgreSQL 15
- MongoDB 7
- Redis 7

### Infraestrutura Auto-Hosted

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  # Backend API
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/bibleapp
      - MONGODB_URL=mongodb://mongo:27017/bibleapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - mongo
      - redis
    volumes:
      - ./backend:/app
    restart: unless-stopped
  
  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=bibleapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
  
  # MongoDB
  mongo:
    image: mongo:7
    volumes:
      - mongo_data:/data/db
    restart: unless-stopped
  
  # Redis
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
  
  # Nginx (Reverse Proxy)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
  mongo_data:
  redis_data:
```

---

## 💰 MODELO FREEMIUM

### Recursos Gratuitos

✅ Leitura completa da Bíblia (4 versões)  
✅ Busca por versículos e palavras-chave  
✅ Destaques (cores limitadas: 2-3)  
✅ Anotações pessoais (limite: 50 anotações)  
✅ Favoritos (limite: 20 versículos)  
✅ Quiz básico (10 questões por dia)  
✅ Modo escuro  
✅ Compartilhamento de texto  
✅ Estatísticas básicas  

### Recursos Premium (💎)

**Plano Premium - R$ 14,90/mês ou R$ 119,90/ano**

✅ Versões bíblicas adicionais (mais de 10 versões)  
✅ Palavras interativas (Strong's) completo  
✅ Destaques ilimitados (5 cores)  
✅ Anotações ilimitadas  
✅ Favoritos ilimitados  
✅ Quiz ilimitado + modo desafio  
✅ Comentários bíblicos avançados  
✅ Mapas interativos (Fase 2)  
✅ **Análise de pregações com IA** (Fase 2)  
✅ Exportação de dados (PDF, DOCX)  
✅ Sem anúncios  
✅ Suporte prioritário  
✅ Estudos avançados  
✅ Novas funcionalidades em primeira mão  

### Implementação de Paywall

```dart
class FeatureGate {
  final SubscriptionService subscription;
  
  Future<bool> canUseFeature(Feature feature) async {
    if (feature.isFree) return true;
    return await subscription.isPremium();
  }
  
  Future<void> showPaywall(BuildContext context, Feature feature) async {
    await showModalBottomSheet(
      context: context,
      builder: (context) => PremiumUpsellSheet(
        feature: feature,
        onSubscribe: () => navigateToSubscription(),
      ),
    );
  }
}

// Uso
if (!await featureGate.canUseFeature(Feature.strongWords)) {
  await featureGate.showPaywall(context, Feature.strongWords);
  return;
}
```

**Integração de Pagamentos:**
- Google Play Billing (Android)
- App Store In-App Purchases (iOS)
- Pacote: `in_app_purchase: ^3.1.11`

---

## 🔮 ROADMAP FUTURO (PÓS-MVP)

### FASE 2 - IA e Recursos Avançados (3-4 meses após MVP)

**Integração de IA Local (Llama):**
- Hospedagem de modelo Llama 3.1 (8B ou 13B)
- Chat bíblico inteligente
- Sugestões personalizadas de leitura
- Explicações contextualizadas

**Análise de Pregações:**
- Gravação in-app
- Transcrição com Whisper
- Identificação automática de versículos
- Análise semântica
- Sugestões de aprofundamento

**Palavras Interativas Completas:**
- Todas as palavras clicáveis
- Análise morfológica
- Concordância completa

**Mapas Interativos:**
- Zoom e navegação
- Filtros por período
- Rotas animadas (viagens de Paulo, etc.)

### FASE 3 - Comunidade e Social (4-5 meses após Fase 2)

**Recursos Sociais:**
- Grupos de estudo
- Compartilhamento de anotações
- Planos de leitura comunitários
- Discussões por versículo

**Pregações Públicas:**
- Biblioteca de pregações compartilhadas
- Avaliações e comentários
- Busca por tema/pregador

**Integrações:**
- Calendário (planos de leitura)
- Apple Watch / Wear OS
- Alexa / Google Assistant (versículo do dia)

---

## 📋 CHECKLIST FINAL ANTES DE COMEÇAR

### Preparação

- [ ] Repositórios Git criados (mobile, backend, docs)
- [ ] Projeto Firebase configurado
- [ ] Servidor configurado (i3, 8GB, 500GB)
- [ ] Docker instalado no servidor
- [ ] Domínio registrado (opcional)
- [ ] SSL configurado (Let's Encrypt)

### Dados

- [ ] Textos bíblicos obtidos (ARA, ARC, ACF, KJV)
- [ ] Licenças verificadas
- [ ] Comentários bíblicos em domínio público baixados
- [ ] Referências cruzadas (TSK) importadas
- [ ] Strong's Concordance baixada
- [ ] Mapas bíblicos coletados
- [ ] Timeline histórica criada

### Banco de Questões

- [ ] 100-200 questões de quiz criadas
  - 50 iniciante
  - 50 intermediário
  - 50 avançado
- [ ] Explicações e referências adicionadas

### Design

- [ ] Paleta de cores definida
- [ ] Logo do app criado
- [ ] Ícones preparados
- [ ] Templates de compartilhamento criados (10-15)
- [ ] UI kit escolhido

### Legal

- [ ] Termos de Uso escritos
- [ ] Política de Privacidade escrita
- [ ] LGPD compliance verificado
- [ ] Conta Google Play criada
- [ ] Conta Apple Developer criada

---

## 🎯 PRÓXIMOS PASSOS IMEDIATOS

1. **Configurar ambiente:**
   - Instalar Flutter
   - Instalar Python + FastAPI
   - Configurar Firebase projeto
   - Preparar servidor

2. **Criar repositórios:**
   - `bible-app-mobile`
   - `bible-app-backend`
   - `bible-app-docs`

3. **Importar dados:**
   - Baixar textos bíblicos
   - Popular banco PostgreSQL
   - Preparar banco de questões

4. **Começar desenvolvimento:**
   - Seguir cronograma de 8 semanas
   - Daily standups entre os 3 devs
   - Code review semanal
   - Deploy contínuo no servidor de staging

---

## 📞 CONTATO E SUPORTE

**Equipe de Desenvolvimento:**
- Dev 1 (Flutter - Bíblia/Perfil): [nome]
- Dev 2 (Flutter - Estudos/Quiz): [nome]
- Dev 3 (Backend Python): [nome]

**Reuniões:**
- Daily standup: 15min por dia
- Sprint planning: Segunda-feira (1h)
- Sprint review: Sexta-feira (1h)

**Ferramentas de Comunicação:**
- Slack / Discord / Telegram
- Trello / Jira / Linear (gestão de tarefas)
- GitHub Projects (acompanhamento)

---

**ESTE DOCUMENTO SERVE COMO GUIA COMPLETO PARA O DESENVOLVIMENTO DO APP BÍBLICO INTELIGENTE.**

**Todas as decisões técnicas foram tomadas. Agora é hora de começar a codificar! 🚀**

---

*Versão 1.0 - Especificação Técnica Completa*  
*Data: [Inserir data]*  
*Revisado por: [Equipe]*
