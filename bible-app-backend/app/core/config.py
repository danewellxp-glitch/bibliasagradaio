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

    class Config:
        env_file = ".env"


settings = Settings()
