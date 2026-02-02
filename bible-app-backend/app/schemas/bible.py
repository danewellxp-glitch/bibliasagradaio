from pydantic import BaseModel


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
