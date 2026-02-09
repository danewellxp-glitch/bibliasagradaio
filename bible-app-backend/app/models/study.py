import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

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


class LexiconEntry(Base):
    __tablename__ = "lexicon_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    strong_number = Column(String(10), unique=True, nullable=False)
    language = Column(String(10), nullable=False)  # hebrew, greek, aramaic
    original_word = Column(String(100))
    transliteration = Column(String(100))
    pronunciation = Column(String(100))
    basic_meaning = Column(Text)
    extended_definition = Column(Text)
    usage_count = Column(Integer)
    first_occurrence = Column(String(20))  # e.g. GEN.1.1

    __table_args__ = (
        Index("idx_lexicon_strong", "strong_number"),
        Index("idx_lexicon_language", "language"),
    )


class WordOccurrence(Base):
    __tablename__ = "word_occurrences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lexicon_entry_id = Column(Integer, ForeignKey("lexicon_entries.id"), nullable=False)
    book_number = Column(Integer, nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    word_position = Column(Integer)
    word_in_verse = Column(String(100))

    __table_args__ = (
        Index("idx_word_occ_verse", "book_number", "chapter", "verse"),
        Index("idx_word_occ_lexicon", "lexicon_entry_id"),
    )


class AIRequestLog(Base):
    __tablename__ = "ai_requests_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    request_type = Column(String(50), default="verse_ask")
    input_hash = Column(String(64))
    input_text = Column(Text)
    output_text = Column(Text)
    from_cache = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
