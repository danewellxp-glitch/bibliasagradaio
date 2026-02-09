from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.bible import (
    BibleVersionResponse,
    ChapterResponse,
    SearchResult,
    VerseResponse,
)
from app.services.bible_service import BibleService

router = APIRouter(prefix="/bible", tags=["bible"])


@router.get("/verse-of-the-day", response_model=VerseResponse)
async def get_verse_of_the_day(
    version: str = "NVI",
    db: Session = Depends(get_db),
):
    service = BibleService(db)
    result = service.get_verse_of_the_day(version)
    if not result:
        raise HTTPException(status_code=404, detail="Verse not found")
    return VerseResponse.model_validate(result)


@router.get("/versions", response_model=list[BibleVersionResponse])
async def get_versions(db: Session = Depends(get_db)):
    service = BibleService(db)
    return service.get_versions()


@router.get("/{version}/{book}/{chapter}", response_model=ChapterResponse)
async def get_chapter(
    version: str,
    book: int = Path(..., ge=1, le=66),
    chapter: int = Path(..., ge=1, le=150),
    db: Session = Depends(get_db),
):
    service = BibleService(db)
    verses = service.get_chapter(version, book, chapter)
    if not verses:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return ChapterResponse(
        book_number=book,
        book_name=verses[0].book_name,
        chapter=chapter,
        verses=[VerseResponse.model_validate(v) for v in verses],
    )


@router.get("/{version}/{book}/{chapter}/{verse}", response_model=VerseResponse)
async def get_verse(
    version: str,
    book: int = Path(..., ge=1, le=66),
    chapter: int = Path(..., ge=1, le=150),
    verse: int = Path(..., ge=1, le=176),
    db: Session = Depends(get_db),
):
    service = BibleService(db)
    result = service.get_verse(version, book, chapter, verse)
    if not result:
        raise HTTPException(status_code=404, detail="Verse not found")
    return VerseResponse.model_validate(result)


@router.get("/{version}/search", response_model=SearchResult)
async def search_bible(
    version: str, q: str, limit: int = 50, db: Session = Depends(get_db)
):
    service = BibleService(db)
    results = service.search(version, q, limit)
    return SearchResult(
        total=len(results),
        results=[VerseResponse.model_validate(r) for r in results],
    )
