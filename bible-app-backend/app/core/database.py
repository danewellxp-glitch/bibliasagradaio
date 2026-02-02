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
