from pydantic import BaseModel, Field


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


class LexiconEntryResponse(BaseModel):
    id: int
    strong_number: str
    language: str
    original_word: str | None
    transliteration: str | None
    pronunciation: str | None
    basic_meaning: str | None
    extended_definition: str | None
    usage_count: int | None
    first_occurrence: str | None

    class Config:
        from_attributes = True


class WordOccurrenceResponse(BaseModel):
    id: int
    lexicon_entry_id: int
    book_number: int
    chapter: int
    verse: int
    word_position: int | None
    word_in_verse: str | None

    class Config:
        from_attributes = True


class LexiconDetailResponse(BaseModel):
    entry: LexiconEntryResponse
    occurrences: list[WordOccurrenceResponse]


class VerseContextResponse(BaseModel):
    version: str
    book: int
    chapter: int
    verse: int
    commentaries: list[CommentaryResponse]
    cross_references: list[CrossReferenceResponse]
    timeline_events: list[TimelineEventResponse]


class VerseAskRequest(BaseModel):
    version: str
    book: int = Field(..., ge=1, le=66)
    chapter: int = Field(..., ge=1)
    verse: int = Field(..., ge=1)
    question: str = Field(..., min_length=3, max_length=500)


class VerseAskResponse(BaseModel):
    answer: str
    from_cache: bool
    remaining_questions: int
