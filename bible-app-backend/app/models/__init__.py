# Import all models so SQLAlchemy sees them when creating tables
from app.models.user import User
from app.models.bible import (
    BibleVersion,
    BibleText,
    UserHighlight,
    UserAnnotation,
    UserBookmark,
    ReadingProgress,
)
from app.models.quiz import (
    QuizQuestion,
    UserQuizHistory,
    UserQuizStats,
    Achievement,
    UserAchievement,
)
from app.models.study import (
    BibleCommentary,
    CrossReference,
    BibleMap,
    TimelineEvent,
)

__all__ = [
    "User",
    "BibleVersion",
    "BibleText",
    "UserHighlight",
    "UserAnnotation",
    "UserBookmark",
    "ReadingProgress",
    "QuizQuestion",
    "UserQuizHistory",
    "UserQuizStats",
    "Achievement",
    "UserAchievement",
    "BibleCommentary",
    "CrossReference",
    "BibleMap",
    "TimelineEvent",
]
