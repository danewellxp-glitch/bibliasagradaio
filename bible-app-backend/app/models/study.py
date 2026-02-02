from sqlalchemy import Column, Index, Integer, String, Text
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
