import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

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
