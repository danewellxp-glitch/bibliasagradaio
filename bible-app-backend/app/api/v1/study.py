import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.ai_gateway import ask_ollama
from app.core.cache import check_rate_limit, get_cached, make_cache_key, set_cached
from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.study import AIRequestLog
from app.models.user import User
from app.schemas.study import (
    BibleMapResponse,
    CommentaryResponse,
    CrossReferenceResponse,
    LexiconDetailResponse,
    LexiconEntryResponse,
    TimelineEventResponse,
    VerseAskRequest,
    VerseAskResponse,
    VerseContextResponse,
)
from app.services.lexicon_service import LexiconService
from app.services.premium_service import PremiumService
from app.services.study_service import StudyService

logger = logging.getLogger(__name__)

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


@router.get(
    "/verse-context/{version}/{book}/{chapter}/{verse}",
    response_model=VerseContextResponse,
)
async def get_verse_context(
    version: str,
    book: int,
    chapter: int,
    verse: int,
    db: Session = Depends(get_db),
):
    service = StudyService(db)
    ctx = service.get_verse_context(book, chapter, verse)
    return VerseContextResponse(
        version=version,
        book=book,
        chapter=chapter,
        verse=verse,
        **ctx,
    )


@router.get("/lexicon/{strong_number}", response_model=LexiconDetailResponse)
async def get_lexicon_entry(
    strong_number: str,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    service = LexiconService(db)
    entry = service.get_lexicon_entry(strong_number)
    if entry is None:
        raise HTTPException(status_code=404, detail="Lexicon entry not found")
    occurrences = service.get_word_occurrences(strong_number, limit=limit)
    return LexiconDetailResponse(entry=entry, occurrences=occurrences)


@router.get("/lexicon/search/", response_model=list[LexiconEntryResponse])
async def search_lexicon(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = LexiconService(db)
    return service.search_lexicon(q, limit=limit)


@router.post("/verse-ask", response_model=VerseAskResponse)
async def verse_ask(
    body: VerseAskRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 1. Rate limit check (premium users get higher limit)
    premium_service = PremiumService(db)
    is_premium = premium_service.is_premium(user.id)
    limit = settings.AI_RATE_LIMIT_PREMIUM if is_premium else settings.AI_RATE_LIMIT_FREE
    allowed, remaining = check_rate_limit(str(user.id), limit)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Limite diario de perguntas atingido. Tente novamente amanha.",
        )

    # 2. Check cache
    cache_key = make_cache_key(
        body.version, body.book, body.chapter, body.verse, body.question
    )
    cached = get_cached(cache_key)
    if cached:
        db.add(AIRequestLog(
            user_id=user.id,
            request_type="verse_ask",
            input_hash=cache_key,
            input_text=body.question,
            output_text=cached,
            from_cache=True,
        ))
        db.commit()
        return VerseAskResponse(
            answer=cached, from_cache=True, remaining_questions=remaining
        )

    # 3. Call Ollama
    verse_ref = f"{body.version} {body.book}:{body.chapter}:{body.verse}"
    try:
        answer = await ask_ollama(
            verse_ref=verse_ref,
            verse_text="",  # verse text fetched by frontend
            question=body.question,
        )
    except Exception as exc:
        logger.error("Ollama error: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="Servico de IA indisponivel. Tente novamente mais tarde.",
        )

    # 4. Cache + log
    set_cached(cache_key, answer)
    db.add(AIRequestLog(
        user_id=user.id,
        request_type="verse_ask",
        input_hash=cache_key,
        input_text=body.question,
        output_text=answer,
        from_cache=False,
    ))
    db.commit()

    return VerseAskResponse(
        answer=answer, from_cache=False, remaining_questions=remaining
    )
