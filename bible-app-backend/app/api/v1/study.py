from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.study import (
    BibleMapResponse,
    CommentaryResponse,
    CrossReferenceResponse,
    TimelineEventResponse,
)
from app.services.study_service import StudyService

router = APIRouter(prefix="/study", tags=["study"])


@router.get("/commentaries", response_model=list[CommentaryResponse])
async def get_commentaries(
    book: int = Query(..., ge=1, le=66),
    chapter: int | None = Query(None, ge=1, le=150),
    verse: int | None = Query(None, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = StudyService(db)
    return service.get_commentaries(book, chapter, verse, limit)


@router.get("/cross-references", response_model=list[CrossReferenceResponse])
async def get_cross_references(
    book: int = Query(..., ge=1, le=66),
    chapter: int = Query(..., ge=1, le=150),
    verse: int = Query(..., ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = StudyService(db)
    return service.get_cross_references(book, chapter, verse, limit)


@router.get("/timeline", response_model=list[TimelineEventResponse])
async def get_timeline(
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    service = StudyService(db)
    return service.get_timeline_events(limit)


@router.get("/maps", response_model=list[BibleMapResponse])
async def get_maps(
    period: str | None = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = StudyService(db)
    return service.get_maps(period, limit)
