import random
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.quiz import (
    AnswerRequest,
    AnswerResponse,
    LeaderboardEntry,
    QuestionResponse,
    QuizStatsResponse,
)
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/quiz", tags=["quiz"])


def _question_to_response(q) -> QuestionResponse:
    wrong = q.wrong_answers or []
    if not isinstance(wrong, list):
        wrong = list(wrong) if wrong else [wrong]
    options = [q.correct_answer] + list(wrong)
    random.shuffle(options)
    return QuestionResponse(
        id=q.id,
        difficulty_level=q.difficulty_level,
        question_type=q.question_type,
        question_text=q.question_text,
        options=options,
        category=q.category,
    )


@router.get("/next-question", response_model=QuestionResponse)
async def get_next_question(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = QuizService(db)
    q = service.get_next_question(user.id)
    if not q:
        raise HTTPException(status_code=404, detail="No questions available")
    return _question_to_response(q)


@router.post("/answer", response_model=AnswerResponse)
async def submit_answer(
    body: AnswerRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = QuizService(db)
    try:
        is_correct, correct_answer, explanation, xp, new_total_xp, streak = (
            service.submit_answer(
                user.id,
                body.question_id,
                body.answer,
                body.time_taken_seconds,
            )
        )
    except ValueError as e:
        if "already answered" in str(e).lower():
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=404, detail=str(e))
    return AnswerResponse(
        is_correct=is_correct,
        correct_answer=correct_answer,
        explanation=explanation,
        xp_earned=xp,
        new_total_xp=new_total_xp,
        streak=streak,
    )


@router.get("/stats", response_model=QuizStatsResponse)
async def get_stats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = QuizService(db)
    stats = service.get_stats(user.id)
    if not stats:
        return QuizStatsResponse(
            total_xp=0,
            current_level=1,
            current_streak=0,
            longest_streak=0,
            total_questions_answered=0,
            total_correct_answers=0,
        )
    return QuizStatsResponse(
        total_xp=stats.total_xp or 0,
        current_level=stats.current_level or 1,
        current_streak=stats.current_streak or 0,
        longest_streak=stats.longest_streak or 0,
        total_questions_answered=stats.total_questions_answered or 0,
        total_correct_answers=stats.total_correct_answers or 0,
    )


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard(
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    service = QuizService(db)
    rows = service.get_leaderboard(limit)
    return [
        LeaderboardEntry(
            rank=i + 1,
            user_id=str(u.id),
            display_name=u.display_name,
            total_xp=s.total_xp or 0,
            current_level=s.current_level or 1,
        )
        for i, (u, s) in enumerate(rows)
    ]
