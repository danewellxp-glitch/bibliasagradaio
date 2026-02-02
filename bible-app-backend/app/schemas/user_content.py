from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


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
