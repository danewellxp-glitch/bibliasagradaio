import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class GameRoom(Base):
    __tablename__ = "game_rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_code = Column(String(6), unique=True, nullable=False)
    game_type = Column(String(50), nullable=False, default="quiz")
    difficulty = Column(String(20), nullable=False, default="beginner")
    max_players = Column(Integer, default=10)
    created_by = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    status = Column(String(20), default="waiting")  # waiting, playing, finished
    current_question = Column(Integer, default=0)
    total_questions = Column(Integer, default=10)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())


class GameParticipant(Base):
    __tablename__ = "game_participants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(
        UUID(as_uuid=True),
        ForeignKey("game_rooms.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    display_name = Column(String(50))
    score = Column(Integer, default=0)
    answers_correct = Column(Integer, default=0)
    answers_total = Column(Integer, default=0)
    joined_at = Column(DateTime, server_default=func.now())


class GameAnswer(Base):
    __tablename__ = "game_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(
        UUID(as_uuid=True),
        ForeignKey("game_rooms.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    question_index = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    answer = Column(String(500), nullable=False)
    is_correct = Column(Integer, default=0)  # 0=wrong, 1=correct
    time_taken_seconds = Column(Integer)
    answered_at = Column(DateTime, server_default=func.now())
