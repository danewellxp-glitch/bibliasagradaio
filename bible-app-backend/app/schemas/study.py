from pydantic import BaseModel


class CommentaryResponse(BaseModel):
    id: int
    author: str
    book_number: int
    chapter: int | None
    verse_start: int | None
    verse_end: int | None
    commentary: str
    source: str | None
    language: str

    class Config:
        from_attributes = True


class CrossReferenceResponse(BaseModel):
    id: int
    from_book: int
    from_chapter: int
    from_verse: int
    to_book: int
    to_chapter: int
    to_verse: int
    relationship_type: str | None

    class Config:
        from_attributes = True


class TimelineEventResponse(BaseModel):
    id: int
    event_name: str
    description: str | None
    approximate_date: str | None
    date_start: int | None
    date_end: int | None
    event_type: str | None
    related_books: list[int] | None
    related_verses: list | None

    class Config:
        from_attributes = True


class BibleMapResponse(BaseModel):
    id: int
    title: str
    description: str | None
    period: str | None
    image_url: str
    related_books: list[int] | None

    class Config:
        from_attributes = True
