# Biblia Sagrada App - MVP Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a cross-platform Bible app (Flutter) with Python backend (FastAPI), featuring Bible reading, studies, quiz gamification, and user profiles with sync.

**Architecture:** Flutter mobile app communicating via REST API with a FastAPI backend. PostgreSQL for structured data (Bible texts, users, quiz), MongoDB for flexible data (preferences, cache). Firebase for auth, analytics, and push notifications. Offline-first with local SQLite on mobile. State management via Riverpod.

**Tech Stack:** Flutter 3.x, Riverpod, sqflite, Dio, Firebase Auth/Analytics/Messaging | Python 3.11, FastAPI, SQLAlchemy, PostgreSQL 15, MongoDB 7, Redis 7, Docker Compose

---

## Sprint Overview

| Sprint | Semana | Foco | Entregavel |
|--------|--------|------|------------|
| 1 | 1-2 | Fundacao (Backend + Mobile setup + Auth) | Login funcional, API rodando |
| 2 | 3-4 | Aba Biblia (Leitura, busca, highlights, anotacoes) | Leitura biblica completa |
| 3 | 5 | Aba Estudos (Comentarios, ref. cruzadas, timeline, mapas) | Recursos de estudo |
| 4 | 6 | Aba Quiz (Gamificacao, XP, streaks, ranking) | Quiz funcional |
| 5 | 7 | Aba Perfil + Polimento (Stats, config, sync, compartilhamento) | App completo |
| 6 | 8 | Testes, QA, Deploy, Beta | App publicado em beta |

---

# SPRINT 1 - FUNDACAO (Semanas 1-2)

## Task 1.1: Setup do Repositorio Backend

**Files:**
- Create: `bible-app-backend/requirements.txt`
- Create: `bible-app-backend/app/__init__.py`
- Create: `bible-app-backend/app/main.py`
- Create: `bible-app-backend/app/core/config.py`
- Create: `bible-app-backend/app/core/database.py`
- Create: `bible-app-backend/Dockerfile`
- Create: `bible-app-backend/.env.example`

**Step 1: Criar estrutura de pastas do backend**

```
bible-app-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── router.py
│   └── services/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── conftest.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── .gitignore
```

**Step 2: Escrever `requirements.txt`**

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pymongo==4.5.0
pydantic==2.4.2
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
firebase-admin==6.2.0
redis==5.0.1
alembic==1.13.0
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.23.2
```

**Step 3: Escrever `app/core/config.py`**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Bible App API"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/bibleapp"
    MONGODB_URL: str = "mongodb://localhost:27017/bibleapp"
    REDIS_URL: str = "redis://localhost:6379"
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24 * 7  # 7 days
    FIREBASE_CREDENTIALS_PATH: str = "serviceAccountKey.json"

    class Config:
        env_file = ".env"

settings = Settings()
```

**Step 4: Escrever `app/core/database.py`**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pymongo import MongoClient
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

mongo_client = MongoClient(settings.MONGODB_URL)
mongo_db = mongo_client.bibleapp

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Step 5: Escrever `app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}
```

**Step 6: Escrever teste basico**

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
```

```python
# tests/test_health.py
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

**Step 7: Rodar teste**

Run: `cd bible-app-backend && pip install -r requirements.txt && pytest tests/test_health.py -v`
Expected: PASS

**Step 8: Commit**

```bash
git add bible-app-backend/
git commit -m "feat(backend): setup FastAPI project structure with config, database, and health check"
```

---

## Task 1.2: Docker Compose - Infraestrutura

**Files:**
- Create: `docker-compose.yml`
- Create: `bible-app-backend/Dockerfile`
- Create: `nginx/nginx.conf`

**Step 1: Escrever `docker-compose.yml`**

```yaml
version: '3.8'

services:
  api:
    build: ./bible-app-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://bibleuser:biblepass@postgres:5432/bibleapp
      - MONGODB_URL=mongodb://mongo:27017/bibleapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - mongo
      - redis
    volumes:
      - ./bible-app-backend:/app
    restart: unless-stopped
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: bibleuser
      POSTGRES_PASSWORD: biblepass
      POSTGRES_DB: bibleapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  mongo_data:
  redis_data:
```

**Step 2: Escrever `Dockerfile`**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Step 3: Subir infraestrutura**

Run: `docker-compose up -d postgres mongo redis`
Expected: 3 containers rodando

**Step 4: Commit**

```bash
git add docker-compose.yml bible-app-backend/Dockerfile
git commit -m "infra: add Docker Compose with PostgreSQL, MongoDB, Redis"
```

---

## Task 1.3: Modelos do Banco de Dados (PostgreSQL)

**Files:**
- Create: `bible-app-backend/app/models/user.py`
- Create: `bible-app-backend/app/models/bible.py`
- Create: `bible-app-backend/app/models/quiz.py`
- Create: `bible-app-backend/app/models/study.py`
- Create: `bible-app-backend/alembic.ini`
- Create: `bible-app-backend/alembic/env.py`

**Step 1: Escrever modelo User**

```python
# app/models/user.py
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firebase_uid = Column(String(128), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(100))
    photo_url = Column(String)
    preferred_version = Column(String(10), default="ARA")
    preferred_language = Column(String(5), default="pt-BR")
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
```

**Step 2: Escrever modelos Bible**

```python
# app/models/bible.py
import uuid
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Numeric, DateTime, func, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base

class BibleVersion(Base):
    __tablename__ = "bible_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    language = Column(String(5), nullable=False)
    description = Column(Text)
    is_premium = Column(Boolean, default=False)
    file_size_mb = Column(Numeric(10, 2))
    is_available_offline = Column(Boolean, default=True)

class BibleText(Base):
    __tablename__ = "bible_texts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version_id = Column(Integer, ForeignKey("bible_versions.id"), nullable=False)
    book_number = Column(Integer, nullable=False)
    book_name = Column(String(50), nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint("version_id", "book_number", "chapter", "verse"),
        Index("idx_bible_texts_reference", "version_id", "book_number", "chapter", "verse"),
    )

class UserHighlight(Base):
    __tablename__ = "user_highlights"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    version_id = Column(Integer, ForeignKey("bible_versions.id"), nullable=False)
    book_number = Column(Integer, nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    color = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "version_id", "book_number", "chapter", "verse"),
        Index("idx_highlights_user", "user_id"),
    )

class UserAnnotation(Base):
    __tablename__ = "user_annotations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    version_id = Column(Integer, ForeignKey("bible_versions.id"), nullable=False)
    book_number = Column(Integer, nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_annotations_user", "user_id"),
    )

class UserBookmark(Base):
    __tablename__ = "user_bookmarks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    version_id = Column(Integer, ForeignKey("bible_versions.id"), nullable=False)
    book_number = Column(Integer, nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    title = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "version_id", "book_number", "chapter", "verse"),
    )

class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_number = Column(Integer, nullable=False)
    chapter = Column(Integer, nullable=False)
    last_verse_read = Column(Integer)
    completed = Column(Boolean, default=False)
    read_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "book_number", "chapter"),
    )
```

**Step 3: Escrever modelos Quiz**

```python
# app/models/quiz.py
import uuid
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Date, DateTime, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    difficulty_level = Column(String(20), nullable=False)
    question_type = Column(String(30), nullable=False)
    question_text = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    wrong_answers = Column(JSONB)
    explanation = Column(Text)
    related_verses = Column(JSONB)
    category = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())

class UserQuizHistory(Base):
    __tablename__ = "user_quiz_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_taken_seconds = Column(Integer)
    answered_at = Column(DateTime, server_default=func.now())

class UserQuizStats(Base):
    __tablename__ = "user_quiz_stats"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    total_xp = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_quiz_date = Column(Date)
    total_questions_answered = Column(Integer, default=0)
    total_correct_answers = Column(Integer, default=0)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon_url = Column(Text)
    xp_reward = Column(Integer, default=0)
    requirement_type = Column(String(50))
    requirement_value = Column(Integer)

class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    unlocked_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "achievement_id"),
    )
```

**Step 4: Escrever modelos Study**

```python
# app/models/study.py
from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base

class BibleCommentary(Base):
    __tablename__ = "bible_commentaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(100), nullable=False)
    book_number = Column(Integer, nullable=False)
    chapter = Column(Integer)
    verse_start = Column(Integer)
    verse_end = Column(Integer)
    commentary = Column(Text, nullable=False)
    source = Column(String(100))
    language = Column(String(5), default="pt-BR")

    __table_args__ = (
        Index("idx_commentaries_reference", "book_number", "chapter", "verse_start"),
    )

class CrossReference(Base):
    __tablename__ = "cross_references"

    id = Column(Integer, primary_key=True, autoincrement=True)
    from_book = Column(Integer, nullable=False)
    from_chapter = Column(Integer, nullable=False)
    from_verse = Column(Integer, nullable=False)
    to_book = Column(Integer, nullable=False)
    to_chapter = Column(Integer, nullable=False)
    to_verse = Column(Integer, nullable=False)
    relationship_type = Column(String(50))

class BibleMap(Base):
    __tablename__ = "bible_maps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    period = Column(String(100))
    image_url = Column(Text, nullable=False)
    related_books = Column(JSONB)

class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String(200), nullable=False)
    description = Column(Text)
    approximate_date = Column(String(50))
    date_start = Column(Integer)
    date_end = Column(Integer)
    event_type = Column(String(50))
    related_books = Column(JSONB)
    related_verses = Column(JSONB)
```

**Step 5: Configurar Alembic e rodar migration**

Run: `cd bible-app-backend && alembic init alembic`

Editar `alembic/env.py` para importar os modelos e usar `settings.DATABASE_URL`.

Run: `alembic revision --autogenerate -m "initial schema"`
Run: `alembic upgrade head`

**Step 6: Commit**

```bash
git add bible-app-backend/app/models/ bible-app-backend/alembic/ bible-app-backend/alembic.ini
git commit -m "feat(backend): add all database models - users, bible, quiz, study"
```

---

## Task 1.4: API de Autenticacao (Firebase + JWT)

**Files:**
- Create: `bible-app-backend/app/core/security.py`
- Create: `bible-app-backend/app/api/v1/auth.py`
- Create: `bible-app-backend/app/schemas/auth.py`
- Create: `bible-app-backend/app/schemas/user.py`
- Create: `bible-app-backend/app/services/auth_service.py`
- Test: `bible-app-backend/tests/test_auth.py`

**Step 1: Escrever schemas**

```python
# app/schemas/user.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserResponse(BaseModel):
    id: UUID
    email: str
    display_name: Optional[str]
    photo_url: Optional[str]
    preferred_version: str
    preferred_language: str
    is_premium: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    preferred_version: Optional[str] = None
    preferred_language: Optional[str] = None
```

```python
# app/schemas/auth.py
from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"

from app.schemas.user import UserResponse
TokenResponse.model_rebuild()
```

**Step 2: Escrever security.py**

```python
# app/core/security.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth, credentials, initialize_app
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
import os

# Initialize Firebase Admin (only if credentials file exists)
if os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    initialize_app(cred)

security = HTTPBearer()

def create_jwt_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    payload = verify_jwt_token(credentials.credentials)
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def verify_firebase_token(token: str) -> dict:
    try:
        decoded = firebase_auth.verify_id_token(token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
```

**Step 3: Escrever auth service**

```python
# app/services/auth_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import create_jwt_token, verify_firebase_token

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login_with_firebase(self, firebase_token: str) -> tuple[User, str]:
        decoded = verify_firebase_token(firebase_token)
        firebase_uid = decoded["uid"]
        email = decoded.get("email", "")
        name = decoded.get("name")
        photo = decoded.get("picture")

        user = self.db.query(User).filter(User.firebase_uid == firebase_uid).first()

        if not user:
            user = User(
                firebase_uid=firebase_uid,
                email=email,
                display_name=name,
                photo_url=photo,
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

        jwt_token = create_jwt_token(str(user.id))
        return user, jwt_token
```

**Step 4: Escrever endpoint auth**

```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(
    authorization: str = Header(..., description="Bearer <firebase_token>"),
    db: Session = Depends(get_db),
):
    firebase_token = authorization.replace("Bearer ", "")
    service = AuthService(db)
    user, jwt_token = service.login_with_firebase(firebase_token)
    return TokenResponse(
        access_token=jwt_token,
        user=UserResponse.model_validate(user),
    )
```

**Step 5: Registrar router no main.py**

```python
# Adicionar em app/main.py
from app.api.v1.auth import router as auth_router
app.include_router(auth_router, prefix="/api/v1")
```

**Step 6: Escrever teste (mock Firebase)**

```python
# tests/test_auth.py
from unittest.mock import patch, MagicMock
from app.core.security import create_jwt_token, verify_jwt_token

def test_create_and_verify_jwt():
    token = create_jwt_token("test-user-id")
    payload = verify_jwt_token(token)
    assert payload["sub"] == "test-user-id"

def test_health_still_works(client):
    response = client.get("/health")
    assert response.status_code == 200
```

**Step 7: Rodar testes**

Run: `cd bible-app-backend && pytest tests/ -v`
Expected: PASS

**Step 8: Commit**

```bash
git add bible-app-backend/app/core/security.py bible-app-backend/app/api/ bible-app-backend/app/schemas/ bible-app-backend/app/services/
git commit -m "feat(backend): add Firebase auth + JWT token system"
```

---

## Task 1.5: API de Biblia (CRUD + Busca)

**Files:**
- Create: `bible-app-backend/app/api/v1/bible.py`
- Create: `bible-app-backend/app/schemas/bible.py`
- Create: `bible-app-backend/app/services/bible_service.py`
- Test: `bible-app-backend/tests/test_bible.py`

**Step 1: Escrever schemas**

```python
# app/schemas/bible.py
from pydantic import BaseModel
from typing import Optional

class VerseResponse(BaseModel):
    book_number: int
    book_name: str
    chapter: int
    verse: int
    text: str

    class Config:
        from_attributes = True

class ChapterResponse(BaseModel):
    book_number: int
    book_name: str
    chapter: int
    verses: list[VerseResponse]

class BibleVersionResponse(BaseModel):
    id: int
    code: str
    name: str
    language: str
    is_premium: bool

    class Config:
        from_attributes = True

class SearchResult(BaseModel):
    total: int
    results: list[VerseResponse]
```

**Step 2: Escrever bible_service.py**

```python
# app/services/bible_service.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.bible import BibleText, BibleVersion

class BibleService:
    def __init__(self, db: Session):
        self.db = db

    def get_versions(self) -> list[BibleVersion]:
        return self.db.query(BibleVersion).all()

    def get_chapter(self, version_code: str, book: int, chapter: int) -> list[BibleText]:
        version = self.db.query(BibleVersion).filter(BibleVersion.code == version_code).first()
        if not version:
            return []
        return (
            self.db.query(BibleText)
            .filter(
                BibleText.version_id == version.id,
                BibleText.book_number == book,
                BibleText.chapter == chapter,
            )
            .order_by(BibleText.verse)
            .all()
        )

    def get_verse(self, version_code: str, book: int, chapter: int, verse: int) -> BibleText | None:
        version = self.db.query(BibleVersion).filter(BibleVersion.code == version_code).first()
        if not version:
            return None
        return (
            self.db.query(BibleText)
            .filter(
                BibleText.version_id == version.id,
                BibleText.book_number == book,
                BibleText.chapter == chapter,
                BibleText.verse == verse,
            )
            .first()
        )

    def search(self, version_code: str, query: str, limit: int = 50) -> list[BibleText]:
        version = self.db.query(BibleVersion).filter(BibleVersion.code == version_code).first()
        if not version:
            return []
        return (
            self.db.query(BibleText)
            .filter(
                BibleText.version_id == version.id,
                BibleText.text.ilike(f"%{query}%"),
            )
            .order_by(BibleText.book_number, BibleText.chapter, BibleText.verse)
            .limit(limit)
            .all()
        )
```

**Step 3: Escrever endpoints**

```python
# app/api/v1/bible.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.bible import VerseResponse, ChapterResponse, BibleVersionResponse, SearchResult
from app.services.bible_service import BibleService

router = APIRouter(prefix="/bible", tags=["bible"])

@router.get("/versions", response_model=list[BibleVersionResponse])
async def get_versions(db: Session = Depends(get_db)):
    service = BibleService(db)
    return service.get_versions()

@router.get("/{version}/{book}/{chapter}", response_model=ChapterResponse)
async def get_chapter(version: str, book: int, chapter: int, db: Session = Depends(get_db)):
    service = BibleService(db)
    verses = service.get_chapter(version, book, chapter)
    if not verses:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return ChapterResponse(
        book_number=book,
        book_name=verses[0].book_name,
        chapter=chapter,
        verses=[VerseResponse.model_validate(v) for v in verses],
    )

@router.get("/{version}/{book}/{chapter}/{verse}", response_model=VerseResponse)
async def get_verse(version: str, book: int, chapter: int, verse: int, db: Session = Depends(get_db)):
    service = BibleService(db)
    result = service.get_verse(version, book, chapter, verse)
    if not result:
        raise HTTPException(status_code=404, detail="Verse not found")
    return VerseResponse.model_validate(result)

@router.get("/{version}/search", response_model=SearchResult)
async def search(version: str, q: str, limit: int = 50, db: Session = Depends(get_db)):
    service = BibleService(db)
    results = service.search(version, q, limit)
    return SearchResult(
        total=len(results),
        results=[VerseResponse.model_validate(r) for r in results],
    )
```

**Step 4: Registrar router**

Adicionar em `app/main.py`:
```python
from app.api.v1.bible import router as bible_router
app.include_router(bible_router, prefix="/api/v1")
```

**Step 5: Commit**

```bash
git add bible-app-backend/app/api/v1/bible.py bible-app-backend/app/schemas/bible.py bible-app-backend/app/services/bible_service.py
git commit -m "feat(backend): add Bible API - versions, chapters, verses, search"
```

---

## Task 1.6: APIs de Highlights, Anotacoes e Bookmarks

**Files:**
- Create: `bible-app-backend/app/api/v1/user_content.py`
- Create: `bible-app-backend/app/schemas/user_content.py`
- Create: `bible-app-backend/app/services/user_content_service.py`

**Step 1: Escrever schemas**

```python
# app/schemas/user_content.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class HighlightCreate(BaseModel):
    version_id: int
    book_number: int
    chapter: int
    verse: int
    color: str

class HighlightResponse(HighlightCreate):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class AnnotationCreate(BaseModel):
    version_id: int
    book_number: int
    chapter: int
    verse: int
    note: str

class AnnotationResponse(AnnotationCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class BookmarkCreate(BaseModel):
    version_id: int
    book_number: int
    chapter: int
    verse: int
    title: Optional[str] = None

class BookmarkResponse(BookmarkCreate):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True
```

**Step 2: Escrever service**

```python
# app/services/user_content_service.py
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.bible import UserHighlight, UserAnnotation, UserBookmark

class UserContentService:
    def __init__(self, db: Session):
        self.db = db

    # Highlights
    def get_highlights(self, user_id: UUID) -> list[UserHighlight]:
        return self.db.query(UserHighlight).filter(UserHighlight.user_id == user_id).all()

    def create_highlight(self, user_id: UUID, data: dict) -> UserHighlight:
        highlight = UserHighlight(user_id=user_id, **data)
        self.db.add(highlight)
        self.db.commit()
        self.db.refresh(highlight)
        return highlight

    def delete_highlight(self, user_id: UUID, highlight_id: UUID) -> bool:
        result = self.db.query(UserHighlight).filter(
            UserHighlight.id == highlight_id, UserHighlight.user_id == user_id
        ).delete()
        self.db.commit()
        return result > 0

    # Annotations
    def get_annotations(self, user_id: UUID) -> list[UserAnnotation]:
        return self.db.query(UserAnnotation).filter(UserAnnotation.user_id == user_id).all()

    def create_annotation(self, user_id: UUID, data: dict) -> UserAnnotation:
        annotation = UserAnnotation(user_id=user_id, **data)
        self.db.add(annotation)
        self.db.commit()
        self.db.refresh(annotation)
        return annotation

    def update_annotation(self, user_id: UUID, annotation_id: UUID, note: str) -> UserAnnotation | None:
        annotation = self.db.query(UserAnnotation).filter(
            UserAnnotation.id == annotation_id, UserAnnotation.user_id == user_id
        ).first()
        if annotation:
            annotation.note = note
            self.db.commit()
            self.db.refresh(annotation)
        return annotation

    def delete_annotation(self, user_id: UUID, annotation_id: UUID) -> bool:
        result = self.db.query(UserAnnotation).filter(
            UserAnnotation.id == annotation_id, UserAnnotation.user_id == user_id
        ).delete()
        self.db.commit()
        return result > 0

    # Bookmarks
    def get_bookmarks(self, user_id: UUID) -> list[UserBookmark]:
        return self.db.query(UserBookmark).filter(UserBookmark.user_id == user_id).all()

    def create_bookmark(self, user_id: UUID, data: dict) -> UserBookmark:
        bookmark = UserBookmark(user_id=user_id, **data)
        self.db.add(bookmark)
        self.db.commit()
        self.db.refresh(bookmark)
        return bookmark

    def delete_bookmark(self, user_id: UUID, bookmark_id: UUID) -> bool:
        result = self.db.query(UserBookmark).filter(
            UserBookmark.id == bookmark_id, UserBookmark.user_id == user_id
        ).delete()
        self.db.commit()
        return result > 0
```

**Step 3: Escrever endpoints**

```python
# app/api/v1/user_content.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user_content import *
from app.services.user_content_service import UserContentService

router = APIRouter(tags=["user-content"])

# --- Highlights ---
@router.get("/highlights", response_model=list[HighlightResponse])
async def get_highlights(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserContentService(db).get_highlights(user.id)

@router.post("/highlights", response_model=HighlightResponse, status_code=201)
async def create_highlight(data: HighlightCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserContentService(db).create_highlight(user.id, data.model_dump())

@router.delete("/highlights/{highlight_id}", status_code=204)
async def delete_highlight(highlight_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not UserContentService(db).delete_highlight(user.id, highlight_id):
        raise HTTPException(status_code=404)

# --- Annotations ---
@router.get("/annotations", response_model=list[AnnotationResponse])
async def get_annotations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserContentService(db).get_annotations(user.id)

@router.post("/annotations", response_model=AnnotationResponse, status_code=201)
async def create_annotation(data: AnnotationCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserContentService(db).create_annotation(user.id, data.model_dump())

@router.delete("/annotations/{annotation_id}", status_code=204)
async def delete_annotation(annotation_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not UserContentService(db).delete_annotation(user.id, annotation_id):
        raise HTTPException(status_code=404)

# --- Bookmarks ---
@router.get("/bookmarks", response_model=list[BookmarkResponse])
async def get_bookmarks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserContentService(db).get_bookmarks(user.id)

@router.post("/bookmarks", response_model=BookmarkResponse, status_code=201)
async def create_bookmark(data: BookmarkCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserContentService(db).create_bookmark(user.id, data.model_dump())

@router.delete("/bookmarks/{bookmark_id}", status_code=204)
async def delete_bookmark(bookmark_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not UserContentService(db).delete_bookmark(user.id, bookmark_id):
        raise HTTPException(status_code=404)
```

**Step 4: Registrar router**

```python
from app.api.v1.user_content import router as user_content_router
app.include_router(user_content_router, prefix="/api/v1")
```

**Step 5: Commit**

```bash
git add bible-app-backend/app/api/v1/user_content.py bible-app-backend/app/schemas/user_content.py bible-app-backend/app/services/user_content_service.py
git commit -m "feat(backend): add highlights, annotations, bookmarks CRUD APIs"
```

---

## Task 1.7: Setup do Projeto Flutter

**Files:**
- Create: `bible-app-mobile/` (Flutter project)

**Step 1: Criar projeto Flutter**

Run: `flutter create --org com.bibliasagrada bible_app_mobile`

**Step 2: Configurar `pubspec.yaml`**

```yaml
dependencies:
  flutter:
    sdk: flutter

  # State Management
  flutter_riverpod: ^2.4.0
  riverpod_annotation: ^2.3.0

  # Networking
  dio: ^5.3.3

  # Local Storage
  sqflite: ^2.3.0
  shared_preferences: ^2.2.2
  hive: ^2.2.3
  hive_flutter: ^1.1.0

  # Firebase
  firebase_core: ^2.20.0
  firebase_auth: ^4.12.1
  firebase_analytics: ^10.6.1
  firebase_messaging: ^14.7.3
  google_sign_in: ^6.1.5
  sign_in_with_apple: ^5.0.0

  # UI
  flutter_svg: ^2.0.9
  cached_network_image: ^3.3.0
  shimmer: ^3.0.0
  fl_chart: ^0.64.0
  percent_indicator: ^4.2.3

  # Utilities
  intl: ^0.18.1
  url_launcher: ^6.2.1
  share_plus: ^7.2.1
  path_provider: ^2.1.1
  encrypt: ^5.0.3
  screenshot: ^2.1.0
  go_router: ^12.1.3

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
  riverpod_generator: ^2.3.0
  build_runner: ^2.4.7
```

**Step 3: Criar estrutura de pastas**

```
lib/
├── core/
│   ├── constants/
│   │   └── app_constants.dart
│   ├── theme/
│   │   ├── app_colors.dart
│   │   ├── app_typography.dart
│   │   └── app_theme.dart
│   ├── utils/
│   │   └── helpers.dart
│   └── services/
│       ├── api_service.dart
│       ├── auth_service.dart
│       └── storage_service.dart
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
│   │   ├── widgets/
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
├── routing/
│   └── app_router.dart
└── main.dart
```

**Step 4: Escrever `app_colors.dart`**

```dart
// lib/core/theme/app_colors.dart
import 'package:flutter/material.dart';

class AppColors {
  static const primary = Color(0xFF4A5FC1);
  static const primaryDark = Color(0xFF2E3B8E);
  static const primaryLight = Color(0xFF6B7AD6);
  static const secondary = Color(0xFFD4AF37);
  static const secondaryDark = Color(0xFFB8941F);
  static const success = Color(0xFF4CAF50);
  static const error = Color(0xFFE53935);
  static const warning = Color(0xFFFF9800);
  static const info = Color(0xFF2196F3);
  static const highlightYellow = Color(0xFFFFEB3B);
  static const highlightGreen = Color(0xFF8BC34A);
  static const highlightBlue = Color(0xFF03A9F4);
  static const highlightRed = Color(0xFFEF5350);
  static const highlightPurple = Color(0xFF9C27B0);
  static const lightBackground = Color(0xFFFAFAFA);
  static const darkBackground = Color(0xFF121212);
  static const sepiaBackground = Color(0xFFF4ECD8);
}
```

**Step 5: Escrever `app_theme.dart`**

```dart
// lib/core/theme/app_theme.dart
import 'package:flutter/material.dart';
import 'app_colors.dart';

class AppTheme {
  static ThemeData light = ThemeData(
    brightness: Brightness.light,
    primaryColor: AppColors.primary,
    scaffoldBackgroundColor: AppColors.lightBackground,
    colorScheme: const ColorScheme.light(
      primary: AppColors.primary,
      secondary: AppColors.secondary,
    ),
    fontFamily: 'Roboto',
  );

  static ThemeData dark = ThemeData(
    brightness: Brightness.dark,
    primaryColor: AppColors.primaryLight,
    scaffoldBackgroundColor: AppColors.darkBackground,
    colorScheme: const ColorScheme.dark(
      primary: AppColors.primaryLight,
      secondary: AppColors.secondary,
    ),
    fontFamily: 'Roboto',
  );

  static ThemeData sepia = ThemeData(
    brightness: Brightness.light,
    primaryColor: AppColors.primary,
    scaffoldBackgroundColor: AppColors.sepiaBackground,
    colorScheme: const ColorScheme.light(
      primary: AppColors.primary,
      secondary: AppColors.secondary,
    ),
    fontFamily: 'Roboto',
  );
}
```

**Step 6: Escrever `api_service.dart`**

```dart
// lib/core/services/api_service.dart
import 'package:dio/dio.dart';

class ApiService {
  late final Dio _dio;

  ApiService({String? baseUrl}) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl ?? 'http://10.0.2.2:8000/api/v1',
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
    ));
  }

  void setToken(String token) {
    _dio.options.headers['Authorization'] = 'Bearer $token';
  }

  Future<Response> get(String path, {Map<String, dynamic>? params}) =>
      _dio.get(path, queryParameters: params);

  Future<Response> post(String path, {dynamic data}) =>
      _dio.post(path, data: data);

  Future<Response> put(String path, {dynamic data}) =>
      _dio.put(path, data: data);

  Future<Response> delete(String path) => _dio.delete(path);
}
```

**Step 7: Escrever `main.dart` com navegacao basica**

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/theme/app_theme.dart';
import 'routing/app_router.dart';

void main() {
  runApp(const ProviderScope(child: BibleApp()));
}

class BibleApp extends ConsumerWidget {
  const BibleApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(appRouterProvider);
    return MaterialApp.router(
      title: 'Biblia Sagrada',
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      routerConfig: router,
      debugShowCheckedModeBanner: false,
    );
  }
}
```

**Step 8: Escrever shell com Bottom Navigation**

```dart
// lib/routing/app_router.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/bible',
    routes: [
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) {
          return ScaffoldWithNavBar(navigationShell: navigationShell);
        },
        branches: [
          StatefulShellBranch(routes: [
            GoRoute(path: '/bible', builder: (context, state) => const PlaceholderScreen(title: 'Biblia')),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/studies', builder: (context, state) => const PlaceholderScreen(title: 'Estudos')),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/sermons', builder: (context, state) => const PlaceholderScreen(title: 'Pregacoes - Em Breve')),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/quiz', builder: (context, state) => const PlaceholderScreen(title: 'Quiz')),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/profile', builder: (context, state) => const PlaceholderScreen(title: 'Perfil')),
          ]),
        ],
      ),
    ],
  );
});

class ScaffoldWithNavBar extends StatelessWidget {
  final StatefulNavigationShell navigationShell;
  const ScaffoldWithNavBar({super.key, required this.navigationShell});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: NavigationBar(
        selectedIndex: navigationShell.currentIndex,
        onDestinationSelected: (index) => navigationShell.goBranch(index),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.book), label: 'Biblia'),
          NavigationDestination(icon: Icon(Icons.school), label: 'Estudos'),
          NavigationDestination(icon: Icon(Icons.mic), label: 'Pregacoes'),
          NavigationDestination(icon: Icon(Icons.quiz), label: 'Quiz'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Perfil'),
        ],
      ),
    );
  }
}

class PlaceholderScreen extends StatelessWidget {
  final String title;
  const PlaceholderScreen({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(child: Text(title, style: const TextStyle(fontSize: 24))),
    );
  }
}
```

**Step 9: Rodar o app**

Run: `cd bible-app-mobile && flutter pub get && flutter run`
Expected: App abre com 5 tabs de navegacao

**Step 10: Commit**

```bash
git add bible-app-mobile/
git commit -m "feat(mobile): setup Flutter project with Riverpod, theming, and bottom navigation"
```

---

## Task 1.8: Telas de Autenticacao (Flutter + Firebase)

**Files:**
- Create: `lib/features/auth/screens/login_screen.dart`
- Create: `lib/features/auth/providers/auth_provider.dart`
- Modify: `lib/core/services/auth_service.dart`
- Modify: `lib/routing/app_router.dart`

**Step 1: Escrever auth_service.dart (Flutter)**

```dart
// lib/core/services/auth_service.dart
import 'package:firebase_auth/firebase_auth.dart' as fb;
import 'package:google_sign_in/google_sign_in.dart';
import 'api_service.dart';

class AuthService {
  final fb.FirebaseAuth _firebaseAuth = fb.FirebaseAuth.instance;
  final GoogleSignIn _googleSignIn = GoogleSignIn();
  final ApiService _api;

  AuthService(this._api);

  fb.User? get currentUser => _firebaseAuth.currentUser;
  Stream<fb.User?> get authStateChanges => _firebaseAuth.authStateChanges();

  Future<String?> signInWithGoogle() async {
    final googleUser = await _googleSignIn.signIn();
    if (googleUser == null) return null;
    final googleAuth = await googleUser.authentication;
    final credential = fb.GoogleAuthProvider.credential(
      accessToken: googleAuth.accessToken,
      idToken: googleAuth.idToken,
    );
    final userCredential = await _firebaseAuth.signInWithCredential(credential);
    final idToken = await userCredential.user?.getIdToken();
    if (idToken == null) return null;
    // Login no backend
    final response = await _api.post('/auth/login',
        data: {}, // body vazio, token vai no header
    );
    final jwt = response.data['access_token'];
    _api.setToken(jwt);
    return jwt;
  }

  Future<void> signOut() async {
    await _googleSignIn.signOut();
    await _firebaseAuth.signOut();
  }
}
```

**Step 2: Escrever auth_provider.dart**

```dart
// lib/features/auth/providers/auth_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/services/auth_service.dart';
import '../../../core/services/api_service.dart';

final apiServiceProvider = Provider<ApiService>((ref) => ApiService());

final authServiceProvider = Provider<AuthService>((ref) {
  return AuthService(ref.read(apiServiceProvider));
});

final authStateProvider = StreamProvider((ref) {
  return ref.read(authServiceProvider).authStateChanges;
});
```

**Step 3: Escrever login_screen.dart**

```dart
// lib/features/auth/screens/login_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/auth_provider.dart';
import '../../../core/theme/app_colors.dart';

class LoginScreen extends ConsumerWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.book, size: 100, color: AppColors.primary),
              const SizedBox(height: 24),
              const Text('Biblia Sagrada',
                  style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              const Text('Seu companheiro de estudos biblicos',
                  style: TextStyle(fontSize: 16, color: Colors.grey)),
              const SizedBox(height: 48),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () async {
                    await ref.read(authServiceProvider).signInWithGoogle();
                  },
                  icon: const Icon(Icons.login),
                  label: const Text('Entrar com Google'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

**Step 4: Atualizar router com guard de autenticacao**

Atualizar `app_router.dart` para redirecionar para login se nao autenticado.

**Step 5: Commit**

```bash
git add bible-app-mobile/lib/
git commit -m "feat(mobile): add Firebase Google sign-in with auth flow"
```

---

# SPRINT 2 - ABA BIBLIA (Semanas 3-4)

## Task 2.1: Modelo e Repository de Biblia (Flutter)

**Files:**
- Create: `lib/data/models/bible_models.dart`
- Create: `lib/data/repositories/bible_repository.dart`
- Create: `lib/features/bible/providers/bible_provider.dart`

**Step 1: Escrever modelos Dart**

```dart
// lib/data/models/bible_models.dart
class BibleVersion {
  final int id;
  final String code;
  final String name;
  final String language;
  final bool isPremium;

  BibleVersion({required this.id, required this.code, required this.name, required this.language, required this.isPremium});

  factory BibleVersion.fromJson(Map<String, dynamic> json) => BibleVersion(
    id: json['id'], code: json['code'], name: json['name'],
    language: json['language'], isPremium: json['is_premium'],
  );
}

class Verse {
  final int bookNumber;
  final String bookName;
  final int chapter;
  final int verse;
  final String text;

  Verse({required this.bookNumber, required this.bookName, required this.chapter, required this.verse, required this.text});

  factory Verse.fromJson(Map<String, dynamic> json) => Verse(
    bookNumber: json['book_number'], bookName: json['book_name'],
    chapter: json['chapter'], verse: json['verse'], text: json['text'],
  );
}
```

**Step 2: Escrever repository**

```dart
// lib/data/repositories/bible_repository.dart
import '../../core/services/api_service.dart';
import '../models/bible_models.dart';

class BibleRepository {
  final ApiService _api;
  BibleRepository(this._api);

  Future<List<BibleVersion>> getVersions() async {
    final response = await _api.get('/bible/versions');
    return (response.data as List).map((e) => BibleVersion.fromJson(e)).toList();
  }

  Future<List<Verse>> getChapter(String version, int book, int chapter) async {
    final response = await _api.get('/bible/$version/$book/$chapter');
    return (response.data['verses'] as List).map((e) => Verse.fromJson(e)).toList();
  }

  Future<List<Verse>> search(String version, String query) async {
    final response = await _api.get('/bible/$version/search', params: {'q': query});
    return (response.data['results'] as List).map((e) => Verse.fromJson(e)).toList();
  }
}
```

**Step 3: Escrever providers**

```dart
// lib/features/bible/providers/bible_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../data/repositories/bible_repository.dart';
import '../../../data/models/bible_models.dart';
import '../../auth/providers/auth_provider.dart';

final bibleRepositoryProvider = Provider<BibleRepository>((ref) {
  return BibleRepository(ref.read(apiServiceProvider));
});

final versionsProvider = FutureProvider<List<BibleVersion>>((ref) {
  return ref.read(bibleRepositoryProvider).getVersions();
});

final selectedVersionProvider = StateProvider<String>((ref) => 'ARA');
final selectedBookProvider = StateProvider<int>((ref) => 1);
final selectedChapterProvider = StateProvider<int>((ref) => 1);

final chapterVersesProvider = FutureProvider<List<Verse>>((ref) {
  final version = ref.watch(selectedVersionProvider);
  final book = ref.watch(selectedBookProvider);
  final chapter = ref.watch(selectedChapterProvider);
  return ref.read(bibleRepositoryProvider).getChapter(version, book, chapter);
});
```

**Step 4: Commit**

```bash
git commit -m "feat(mobile): add Bible data models, repository, and providers"
```

---

## Task 2.2: Tela de Leitura da Biblia

**Files:**
- Create: `lib/features/bible/screens/bible_reader_screen.dart`
- Create: `lib/features/bible/screens/book_selector_screen.dart`
- Create: `lib/features/bible/widgets/verse_card.dart`
- Create: `lib/core/constants/bible_books.dart`

**Step 1: Criar lista de livros da Biblia**

```dart
// lib/core/constants/bible_books.dart
class BibleBook {
  final int number;
  final String name;
  final String abbreviation;
  final int chapters;
  final String testament; // "AT" ou "NT"

  const BibleBook({required this.number, required this.name, required this.abbreviation, required this.chapters, required this.testament});
}

const List<BibleBook> bibleBooks = [
  BibleBook(number: 1, name: 'Genesis', abbreviation: 'Gn', chapters: 50, testament: 'AT'),
  BibleBook(number: 2, name: 'Exodo', abbreviation: 'Ex', chapters: 40, testament: 'AT'),
  // ... todos os 66 livros
  BibleBook(number: 66, name: 'Apocalipse', abbreviation: 'Ap', chapters: 22, testament: 'NT'),
];
```

**Step 2: Escrever tela de leitura**

```dart
// lib/features/bible/screens/bible_reader_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/bible_provider.dart';
import '../widgets/verse_card.dart';
import '../../../core/constants/bible_books.dart';

class BibleReaderScreen extends ConsumerWidget {
  const BibleReaderScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final versesAsync = ref.watch(chapterVersesProvider);
    final book = ref.watch(selectedBookProvider);
    final chapter = ref.watch(selectedChapterProvider);
    final bookInfo = bibleBooks.firstWhere((b) => b.number == book);

    return Scaffold(
      appBar: AppBar(
        title: GestureDetector(
          onTap: () => _showBookSelector(context, ref),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('${bookInfo.name} $chapter'),
              const Icon(Icons.arrow_drop_down),
            ],
          ),
        ),
        actions: [
          IconButton(icon: const Icon(Icons.search), onPressed: () => _goToSearch(context)),
        ],
      ),
      body: versesAsync.when(
        data: (verses) => ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: verses.length,
          itemBuilder: (context, index) => VerseCard(
            verse: verses[index],
            onTap: () => _showVerseOptions(context, ref, verses[index]),
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Erro: $e')),
      ),
    );
  }
}
```

**Step 3: Escrever VerseCard widget**

```dart
// lib/features/bible/widgets/verse_card.dart
import 'package:flutter/material.dart';
import '../../../data/models/bible_models.dart';

class VerseCard extends StatelessWidget {
  final Verse verse;
  final VoidCallback? onTap;
  final Color? highlightColor;

  const VerseCard({super.key, required this.verse, this.onTap, this.highlightColor});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 4),
        color: highlightColor?.withOpacity(0.3),
        child: RichText(
          text: TextSpan(
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              fontFamily: 'Georgia', height: 1.6,
            ),
            children: [
              TextSpan(
                text: ' ${verse.verse} ',
                style: TextStyle(
                  fontSize: 12, fontWeight: FontWeight.bold,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
              TextSpan(text: verse.text),
            ],
          ),
        ),
      ),
    );
  }
}
```

**Step 4: Commit**

```bash
git commit -m "feat(mobile): add Bible reader screen with verse cards and book selector"
```

---

## Task 2.3: Sistema de Highlights e Anotacoes (Flutter)

**Files:**
- Create: `lib/features/bible/widgets/highlight_menu.dart`
- Create: `lib/features/bible/widgets/annotation_dialog.dart`
- Create: `lib/data/repositories/user_content_repository.dart`

Implementar menu de opcoes ao tocar em versiculo (highlight 5 cores, anotar, favoritar, compartilhar).

**Step 1-5:** Escrever repository, provider, widgets de highlight e anotacao.

**Step 6: Commit**

```bash
git commit -m "feat(mobile): add highlights (5 colors), annotations, and bookmarks"
```

---

## Task 2.4: Busca Biblica (Flutter)

**Files:**
- Create: `lib/features/bible/screens/bible_search_screen.dart`

Implementar tela de busca com filtros (versao, testamento, livro).

**Commit:**
```bash
git commit -m "feat(mobile): add Bible search with filters"
```

---

## Task 2.5: Download Offline + SQLite Local

**Files:**
- Create: `lib/core/services/offline_service.dart`
- Create: `lib/data/repositories/offline_bible_repository.dart`

Implementar download de versoes para SQLite local, leitura offline-first.

**Commit:**
```bash
git commit -m "feat(mobile): add offline Bible download with SQLite"
```

---

## Task 2.6: Script de Populacao dos Textos Biblicos (Backend)

**Files:**
- Create: `bible-app-backend/scripts/populate_bible.py`

Script Python para popular PostgreSQL com textos de ARA, ARC, ACF, KJV a partir de fontes JSON/CSV.

**Commit:**
```bash
git commit -m "data(backend): add Bible text population script for ARA, ARC, ACF, KJV"
```

---

# SPRINT 3 - ABA ESTUDOS (Semana 5)

## Task 3.1: API de Estudos (Backend)

**Files:**
- Create: `bible-app-backend/app/api/v1/study.py`
- Create: `bible-app-backend/app/schemas/study.py`
- Create: `bible-app-backend/app/services/study_service.py`

Endpoints: GET commentaries, GET cross-references, GET timeline, GET maps.

**Commit:**
```bash
git commit -m "feat(backend): add study API - commentaries, cross-references, timeline, maps"
```

---

## Task 3.2: Importar Dados de Estudo (Backend)

**Files:**
- Create: `bible-app-backend/scripts/populate_commentaries.py`
- Create: `bible-app-backend/scripts/populate_cross_references.py`
- Create: `bible-app-backend/scripts/populate_timeline.py`

Scripts para importar comentarios (Matthew Henry, etc.), TSK cross-references, e timeline.

**Commit:**
```bash
git commit -m "data(backend): import commentaries, cross-references, and timeline events"
```

---

## Task 3.3: Tela de Estudos (Flutter)

**Files:**
- Create: `lib/features/study/screens/study_home_screen.dart`
- Create: `lib/features/study/screens/commentary_screen.dart`
- Create: `lib/features/study/screens/cross_references_screen.dart`
- Create: `lib/features/study/screens/timeline_screen.dart`
- Create: `lib/features/study/screens/maps_screen.dart`
- Create: `lib/features/study/providers/study_provider.dart`

Implementar todas as sub-telas de estudo.

**Commit:**
```bash
git commit -m "feat(mobile): add Studies tab - commentaries, cross-references, timeline, maps"
```

---

# SPRINT 4 - ABA QUIZ (Semana 6)

## Task 4.1: API de Quiz (Backend)

**Files:**
- Create: `bible-app-backend/app/api/v1/quiz.py`
- Create: `bible-app-backend/app/schemas/quiz.py`
- Create: `bible-app-backend/app/services/quiz_service.py`

Endpoints: GET next-question (adaptativo), POST answer, GET stats, GET leaderboard.

**Commit:**
```bash
git commit -m "feat(backend): add Quiz API with adaptive difficulty and leaderboard"
```

---

## Task 4.2: Banco de Questoes Inicial

**Files:**
- Create: `bible-app-backend/scripts/populate_quiz.py`
- Create: `bible-app-backend/data/quiz_questions.json`

Criar 150+ questoes (50 beginner, 50 intermediate, 50 advanced) em JSON e popular no banco.

**Commit:**
```bash
git commit -m "data(backend): add initial quiz question bank (150+ questions)"
```

---

## Task 4.3: Tela de Quiz com Gamificacao (Flutter)

**Files:**
- Create: `lib/features/quiz/screens/quiz_home_screen.dart`
- Create: `lib/features/quiz/screens/quiz_play_screen.dart`
- Create: `lib/features/quiz/screens/quiz_result_screen.dart`
- Create: `lib/features/quiz/screens/leaderboard_screen.dart`
- Create: `lib/features/quiz/widgets/question_card.dart`
- Create: `lib/features/quiz/widgets/xp_progress.dart`
- Create: `lib/features/quiz/providers/quiz_provider.dart`

Implementar quiz com XP, niveis, streaks, animacoes de feedback, e ranking.

**Commit:**
```bash
git commit -m "feat(mobile): add Quiz tab with XP, levels, streaks, and leaderboard"
```

---

# SPRINT 5 - PERFIL + POLIMENTO (Semana 7)

## Task 5.1: API de Perfil e Estatisticas (Backend)

**Files:**
- Create: `bible-app-backend/app/api/v1/profile.py`
- Create: `bible-app-backend/app/services/stats_service.py`

Endpoints: GET reading-stats, GET quiz-stats, PUT settings, GET achievements.

**Commit:**
```bash
git commit -m "feat(backend): add profile API - stats, settings, achievements"
```

---

## Task 5.2: Tela de Perfil e Configuracoes (Flutter)

**Files:**
- Create: `lib/features/profile/screens/profile_screen.dart`
- Create: `lib/features/profile/screens/settings_screen.dart`
- Create: `lib/features/profile/screens/reading_stats_screen.dart`
- Create: `lib/features/profile/screens/offline_management_screen.dart`
- Create: `lib/features/profile/widgets/stat_card.dart`
- Create: `lib/features/profile/providers/profile_provider.dart`

Implementar perfil com graficos de progresso, configuracoes, e gestao de offline.

**Commit:**
```bash
git commit -m "feat(mobile): add Profile tab with stats, settings, and offline management"
```

---

## Task 5.3: Compartilhamento de Versiculos

**Files:**
- Create: `lib/features/bible/widgets/share_verse_sheet.dart`
- Create: `lib/features/bible/services/verse_image_generator.dart`

Compartilhamento em texto + geracao de imagem com templates.

**Commit:**
```bash
git commit -m "feat(mobile): add verse sharing as text and image with templates"
```

---

## Task 5.4: Sincronizacao Completa

**Files:**
- Create: `lib/core/services/sync_service.dart`

Implementar sync offline-first: highlights, anotacoes, bookmarks, progresso, quiz, configuracoes.

**Commit:**
```bash
git commit -m "feat(mobile): add full data sync service (offline-first)"
```

---

## Task 5.5: Tela de Pregacoes (Placeholder)

**Files:**
- Create: `lib/features/sermons/screens/sermons_screen.dart`

Tela "Em Breve" com opcao de notificacao.

**Commit:**
```bash
git commit -m "feat(mobile): add Sermons placeholder screen (coming soon)"
```

---

# SPRINT 6 - TESTES, QA e DEPLOY (Semana 8)

## Task 6.1: Testes de Integracao Backend

**Files:**
- Create: `bible-app-backend/tests/test_bible_api.py`
- Create: `bible-app-backend/tests/test_quiz_api.py`
- Create: `bible-app-backend/tests/test_user_content_api.py`

Escrever testes de integracao para todos os endpoints.

**Commit:**
```bash
git commit -m "test(backend): add integration tests for all API endpoints"
```

---

## Task 6.2: Testes Widget Flutter

**Files:**
- Create: `bible-app-mobile/test/bible_reader_test.dart`
- Create: `bible-app-mobile/test/quiz_test.dart`

Escrever testes de widget para telas principais.

**Commit:**
```bash
git commit -m "test(mobile): add widget tests for Bible reader and Quiz"
```

---

## Task 6.3: Deploy Backend em Producao

**Files:**
- Create: `nginx/nginx.conf`
- Modify: `docker-compose.yml` (adicionar nginx)
- Create: `bible-app-backend/.env.production`

Configurar nginx como reverse proxy, SSL com Let's Encrypt, deploy com docker-compose.

**Commit:**
```bash
git commit -m "infra: add production deployment with nginx, SSL, and docker-compose"
```

---

## Task 6.4: Build e Publicacao Beta

**Steps:**
1. `flutter build apk --release` (Android)
2. `flutter build ios --release` (iOS)
3. Upload para Google Play Beta
4. Upload para TestFlight
5. Testes em dispositivos reais
6. Corrigir bugs encontrados

**Commit:**
```bash
git commit -m "release: prepare v1.0.0-beta builds for Android and iOS"
```

---

## Resumo de Dependencias entre Sprints

```
Sprint 1 (Fundacao)
  ├── Task 1.1-1.2: Backend setup + Docker  [SEM DEPENDENCIA]
  ├── Task 1.3: DB Models                   [depende de 1.1]
  ├── Task 1.4: Auth API                    [depende de 1.3]
  ├── Task 1.5: Bible API                   [depende de 1.3]
  ├── Task 1.6: User Content API            [depende de 1.3, 1.4]
  ├── Task 1.7: Flutter Setup               [SEM DEPENDENCIA, paralelo com backend]
  └── Task 1.8: Flutter Auth                [depende de 1.4, 1.7]

Sprint 2 (Biblia) [depende de Sprint 1]
Sprint 3 (Estudos) [depende de Sprint 1]
Sprint 4 (Quiz) [depende de Sprint 1]
Sprint 5 (Perfil) [depende de Sprints 2-4]
Sprint 6 (Deploy) [depende de Sprint 5]
```

**Nota:** Sprints 2, 3 e 4 podem ter trabalho paralelo entre devs frontend e backend.
