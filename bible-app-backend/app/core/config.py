from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Bible App API"
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://bibleuser:biblepass@localhost:5432/bibleapp"
    MONGODB_URL: str = "mongodb://localhost:27017/bibleapp"
    REDIS_URL: str = "redis://localhost:6379"
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60 * 24 * 7
    FIREBASE_CREDENTIALS_PATH: str = "serviceAccountKey.json"
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b"
    AI_RATE_LIMIT_FREE: int = 3
    AI_RATE_LIMIT_PREMIUM: int = 100

    class Config:
        env_file = ".env"


settings = Settings()
