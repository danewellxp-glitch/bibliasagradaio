import random
import string
import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.game import GameAnswer, GameParticipant, GameRoom
from app.models.quiz import QuizQuestion


class GameService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_room_code(self) -> str:
        """Generate a unique 6-char room code."""
        for _ in range(10):
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            existing = (
                self.db.query(GameRoom)
                .filter(GameRoom.room_code == code)
                .first()
            )
            if not existing:
                return code
        raise ValueError("Could not generate unique room code")

    def create_room(
        self,
        user_id: uuid.UUID,
        game_type: str,
        difficulty: str,
        max_players: int,
        total_questions: int,
    ) -> GameRoom:
        room = GameRoom(
            room_code=self._generate_room_code(),
            game_type=game_type,
            difficulty=difficulty,
            max_players=max_players,
            total_questions=total_questions,
            created_by=user_id,
        )
        self.db.add(room)
        self.db.flush()

        # Auto-join the creator
        participant = GameParticipant(
            room_id=room.id,
            user_id=user_id,
        )
        self.db.add(participant)
        self.db.commit()
        self.db.refresh(room)
        return room

    def get_room_by_code(self, code: str) -> GameRoom | None:
        return (
            self.db.query(GameRoom)
            .filter(GameRoom.room_code == code.upper())
            .first()
        )

    def join_room(
        self, room: GameRoom, user_id: uuid.UUID, display_name: str | None
    ) -> GameParticipant:
        # Check if already joined
        existing = (
            self.db.query(GameParticipant)
            .filter(
                GameParticipant.room_id == room.id,
                GameParticipant.user_id == user_id,
            )
            .first()
        )
        if existing:
            return existing

        participant = GameParticipant(
            room_id=room.id,
            user_id=user_id,
            display_name=display_name,
        )
        self.db.add(participant)
        self.db.commit()
        self.db.refresh(participant)
        return participant

    def get_participants(self, room_id: uuid.UUID) -> list[GameParticipant]:
        return (
            self.db.query(GameParticipant)
            .filter(GameParticipant.room_id == room_id)
            .order_by(GameParticipant.score.desc())
            .all()
        )

    def start_game(self, room: GameRoom) -> GameRoom:
        room.status = "playing"
        room.current_question = 1
        room.started_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(room)
        return room

    def get_question_for_room(self, room: GameRoom) -> QuizQuestion | None:
        """Get the question for the current round."""
        # Get questions already used in this game
        used_ids = [
            r[0]
            for r in self.db.query(GameAnswer.question_id)
            .filter(GameAnswer.room_id == room.id)
            .distinct()
            .all()
        ]

        query = self.db.query(QuizQuestion)
        if room.difficulty != "mixed":
            query = query.filter(QuizQuestion.difficulty_level == room.difficulty)
        if used_ids:
            query = query.filter(~QuizQuestion.id.in_(used_ids))

        return query.order_by(func.random()).first()

    def submit_answer(
        self,
        room: GameRoom,
        user_id: uuid.UUID,
        question_id: int,
        answer: str,
        time_taken: int | None,
    ) -> tuple[bool, str, str | None, int, int]:
        """Returns (is_correct, correct_answer, explanation, points, total_score)."""
        question = (
            self.db.query(QuizQuestion)
            .filter(QuizQuestion.id == question_id)
            .first()
        )
        if not question:
            raise ValueError("Question not found")

        # Check for duplicate answer
        existing = (
            self.db.query(GameAnswer)
            .filter(
                GameAnswer.room_id == room.id,
                GameAnswer.user_id == user_id,
                GameAnswer.question_index == room.current_question,
            )
            .first()
        )
        if existing:
            raise ValueError("Already answered this question")

        is_correct = question.correct_answer.strip().lower() == answer.strip().lower()

        # Points: base + time bonus
        points = 0
        if is_correct:
            points = 100
            if time_taken and time_taken < 10:
                points += 50  # fast bonus
            elif time_taken and time_taken < 20:
                points += 25

        # Record answer
        self.db.add(
            GameAnswer(
                room_id=room.id,
                user_id=user_id,
                question_index=room.current_question,
                question_id=question_id,
                answer=answer,
                is_correct=1 if is_correct else 0,
                time_taken_seconds=time_taken,
            )
        )

        # Update participant score
        participant = (
            self.db.query(GameParticipant)
            .filter(
                GameParticipant.room_id == room.id,
                GameParticipant.user_id == user_id,
            )
            .first()
        )
        if participant:
            participant.score = (participant.score or 0) + points
            participant.answers_total = (participant.answers_total or 0) + 1
            if is_correct:
                participant.answers_correct = (participant.answers_correct or 0) + 1

        self.db.commit()

        return (
            is_correct,
            question.correct_answer,
            question.explanation,
            points,
            participant.score if participant else points,
        )

    def advance_question(self, room: GameRoom) -> bool:
        """Advance to next question. Returns False if game is over."""
        if room.current_question >= room.total_questions:
            room.status = "finished"
            room.finished_at = datetime.utcnow()
            self.db.commit()
            return False

        room.current_question = room.current_question + 1
        self.db.commit()
        return True

    def check_all_answered(self, room: GameRoom) -> bool:
        """Check if all participants answered the current question."""
        participant_count = (
            self.db.query(GameParticipant)
            .filter(GameParticipant.room_id == room.id)
            .count()
        )
        answer_count = (
            self.db.query(GameAnswer)
            .filter(
                GameAnswer.room_id == room.id,
                GameAnswer.question_index == room.current_question,
            )
            .count()
        )
        return answer_count >= participant_count

    def finish_game(self, room: GameRoom) -> list[GameParticipant]:
        """Finish the game and return ranked participants."""
        room.status = "finished"
        room.finished_at = datetime.utcnow()
        self.db.commit()
        return self.get_participants(room.id)

    def calculate_xp(self, rank: int, score: int) -> int:
        """Calculate XP earned based on rank and score."""
        base_xp = score // 10
        if rank == 1:
            base_xp += 50
        elif rank == 2:
            base_xp += 30
        elif rank == 3:
            base_xp += 20
        return base_xp
