import uuid
from datetime import date, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.quiz import QuizQuestion, UserQuizHistory, UserQuizStats
from app.models.user import User


class QuizService:
    def __init__(self, db: Session):
        self.db = db

    def get_next_question(self, user_id: uuid.UUID) -> QuizQuestion | None:
        stats = self._get_or_create_stats(user_id)
        recent_ids = [
            r[0]
            for r in self.db.query(UserQuizHistory.question_id)
            .filter(UserQuizHistory.user_id == user_id)
            .order_by(UserQuizHistory.answered_at.desc())
            .limit(20)
            .all()
        ]
        difficulty = self._suggest_difficulty(stats, recent_ids)
        q = self.db.query(QuizQuestion).filter(
            QuizQuestion.difficulty_level == difficulty
        )
        if recent_ids:
            q = q.filter(~QuizQuestion.id.in_(recent_ids))
        q = q.order_by(func.random()).first()
        if q is None:
            q = self.db.query(QuizQuestion)
            if recent_ids:
                q = q.filter(~QuizQuestion.id.in_(recent_ids))
            q = q.order_by(func.random()).first()
        return q

    def _get_or_create_stats(self, user_id: uuid.UUID) -> UserQuizStats:
        stats = self.db.query(UserQuizStats).filter(UserQuizStats.user_id == user_id).first()
        if stats is None:
            stats = UserQuizStats(user_id=user_id)
            self.db.add(stats)
            self.db.commit()
            self.db.refresh(stats)
        return stats

    def _suggest_difficulty(self, stats: UserQuizStats, recent_ids: list) -> str:
        if stats.total_questions_answered < 5:
            return "beginner"
        correct_rate = (
            stats.total_correct_answers / stats.total_questions_answered
            if stats.total_questions_answered else 0
        )
        if correct_rate > 0.75:
            return "advanced"
        if correct_rate > 0.5:
            return "intermediate"
        return "beginner"

    def submit_answer(
        self,
        user_id: uuid.UUID,
        question_id: int,
        answer: str,
        time_taken_seconds: int | None,
    ) -> tuple[bool, str, str | None, int, int, int]:
        """Returns (is_correct, correct_answer, explanation, xp_earned, new_total_xp, streak)."""
        question = self.db.query(QuizQuestion).filter(QuizQuestion.id == question_id).first()
        if not question:
            raise ValueError("Question not found")
        is_correct = question.correct_answer.strip().lower() == answer.strip().lower()
        xp = 10 if is_correct else 0
        if is_correct and question.difficulty_level == "intermediate":
            xp = 15
        if is_correct and question.difficulty_level == "advanced":
            xp = 25

        # Prevent duplicate answer (same question already answered)
        existing = (
            self.db.query(UserQuizHistory)
            .filter(
                UserQuizHistory.user_id == user_id,
                UserQuizHistory.question_id == question_id,
            )
            .first()
        )
        if existing:
            raise ValueError("Question already answered")

        self.db.add(
            UserQuizHistory(
                user_id=user_id,
                question_id=question_id,
                is_correct=is_correct,
                time_taken_seconds=time_taken_seconds,
            )
        )
        stats = self._get_or_create_stats(user_id)
        stats.total_questions_answered += 1
        if is_correct:
            stats.total_correct_answers += 1
            stats.total_xp = (stats.total_xp or 0) + xp
            stats.current_level = 1 + (stats.total_xp or 0) // 100
            today = date.today()
            if stats.last_quiz_date == today - timedelta(days=1):
                stats.current_streak = (stats.current_streak or 0) + 1
            elif stats.last_quiz_date != today:
                stats.current_streak = 1
            stats.last_quiz_date = today
            if (stats.current_streak or 0) > (stats.longest_streak or 0):
                stats.longest_streak = stats.current_streak
        else:
            stats.current_streak = 0
        stats.last_quiz_date = stats.last_quiz_date or date.today()
        self.db.commit()
        self.db.refresh(stats)
        return (
            is_correct,
            question.correct_answer,
            question.explanation,
            xp,
            stats.total_xp or 0,
            stats.current_streak or 0,
        )

    def get_stats(self, user_id: uuid.UUID) -> UserQuizStats | None:
        return self.db.query(UserQuizStats).filter(UserQuizStats.user_id == user_id).first()

    def get_leaderboard(self, limit: int = 50) -> list[tuple[User, UserQuizStats]]:
        rows = (
            self.db.query(User, UserQuizStats)
            .join(UserQuizStats, User.id == UserQuizStats.user_id)
            .order_by(UserQuizStats.total_xp.desc())
            .limit(limit)
            .all()
        )
        return list(rows)
