import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import mongo_db
from app.models.bible import ReadingProgress, UserAnnotation, UserBookmark, UserHighlight
from app.models.quiz import Achievement, UserAchievement, UserQuizStats
from app.models.user import User


class StatsService:
    def __init__(self, db: Session):
        self.db = db

    def get_reading_stats(self, user_id: uuid.UUID) -> dict:
        chapters_count = (
            self.db.query(func.count(ReadingProgress.id))
            .filter(ReadingProgress.user_id == user_id)
            .scalar()
            or 0
        )
        completed_count = (
            self.db.query(func.count(ReadingProgress.id))
            .filter(
                ReadingProgress.user_id == user_id,
                ReadingProgress.completed == True,
            )
            .scalar()
            or 0
        )
        highlights_count = (
            self.db.query(func.count(UserHighlight.id))
            .filter(UserHighlight.user_id == user_id)
            .scalar()
            or 0
        )
        annotations_count = (
            self.db.query(func.count(UserAnnotation.id))
            .filter(UserAnnotation.user_id == user_id)
            .scalar()
            or 0
        )
        bookmarks_count = (
            self.db.query(func.count(UserBookmark.id))
            .filter(UserBookmark.user_id == user_id)
            .scalar()
            or 0
        )
        return {
            "chapters_read": chapters_count,
            "chapters_completed": completed_count,
            "highlights_count": highlights_count,
            "annotations_count": annotations_count,
            "bookmarks_count": bookmarks_count,
        }

    def get_quiz_stats(self, user_id: uuid.UUID) -> dict:
        stats = (
            self.db.query(UserQuizStats)
            .filter(UserQuizStats.user_id == user_id)
            .first()
        )
        if not stats:
            return {
                "total_xp": 0,
                "current_level": 1,
                "current_streak": 0,
                "longest_streak": 0,
                "total_questions_answered": 0,
                "total_correct_answers": 0,
            }
        return {
            "total_xp": stats.total_xp or 0,
            "current_level": stats.current_level or 1,
            "current_streak": stats.current_streak or 0,
            "longest_streak": stats.longest_streak or 0,
            "total_questions_answered": stats.total_questions_answered or 0,
            "total_correct_answers": stats.total_correct_answers or 0,
        }

    def get_settings(self, user_id: uuid.UUID) -> dict:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return {}
        firebase_uid = str(user.firebase_uid)
        coll = mongo_db.user_preferences
        doc = coll.find_one({"userId": firebase_uid})
        if not doc:
            return {
                "fontSize": 16,
                "fontFamily": "Georgia",
                "lineHeight": 1.5,
                "theme": "light",
                "showVerseNumbers": True,
                "showRedLetters": True,
                "defaultVersion": user.preferred_version or "ARA",
                "language": user.preferred_language or "pt-BR",
            }
        prefs = doc.get("preferences", {})
        return {
            "fontSize": prefs.get("fontSize", 16),
            "fontFamily": prefs.get("fontFamily", "Georgia"),
            "lineHeight": prefs.get("lineHeight", 1.5),
            "theme": prefs.get("theme", "light"),
            "showVerseNumbers": prefs.get("showVerseNumbers", True),
            "showRedLetters": prefs.get("showRedLetters", True),
            "defaultVersion": prefs.get("defaultVersion", user.preferred_version or "ARA"),
            "language": prefs.get("language", user.preferred_language or "pt-BR"),
        }

    def put_settings(self, user_id: uuid.UUID, settings: dict) -> dict:
        from datetime import datetime

        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        firebase_uid = str(user.firebase_uid)
        coll = mongo_db.user_preferences
        allowed = {
            "fontSize", "fontFamily", "lineHeight", "theme",
            "showVerseNumbers", "showRedLetters", "defaultVersion", "language",
        }
        current = self.get_settings(user_id)
        prefs = {**current, **{k: v for k, v in settings.items() if k in allowed}}
        coll.update_one(
            {"userId": firebase_uid},
            {"$set": {"preferences": prefs, "updatedAt": datetime.utcnow()}},
            upsert=True,
        )
        if "defaultVersion" in prefs:
            user.preferred_version = prefs["defaultVersion"]
        if "language" in prefs:
            user.preferred_language = prefs["language"]
        self.db.commit()
        self.db.refresh(user)
        return self.get_settings(user_id)

    def get_achievements(self, user_id: uuid.UUID) -> list[dict]:
        rows = (
            self.db.query(Achievement, UserAchievement)
            .join(UserAchievement, Achievement.id == UserAchievement.achievement_id)
            .filter(UserAchievement.user_id == user_id)
            .all()
        )
        return [
            {
                "id": a.id,
                "code": a.code,
                "name": a.name,
                "description": a.description,
                "icon_url": a.icon_url,
                "xp_reward": a.xp_reward or 0,
                "unlocked_at": ua.unlocked_at.isoformat() if ua.unlocked_at else None,
            }
            for a, ua in rows
        ]
