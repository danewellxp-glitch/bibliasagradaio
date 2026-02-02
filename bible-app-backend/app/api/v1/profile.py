from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.stats_service import StatsService

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/reading-stats")
async def get_reading_stats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return StatsService(db).get_reading_stats(user.id)


@router.get("/quiz-stats")
async def get_quiz_stats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return StatsService(db).get_quiz_stats(user.id)


@router.get("/settings")
async def get_settings(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return StatsService(db).get_settings(user.id)


@router.put("/settings")
async def put_settings(
    settings: dict,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return StatsService(db).put_settings(user.id, settings)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/achievements")
async def get_achievements(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return StatsService(db).get_achievements(user.id)
