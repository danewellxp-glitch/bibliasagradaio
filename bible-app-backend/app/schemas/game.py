from pydantic import BaseModel, Field


class CreateRoomRequest(BaseModel):
    game_type: str = "quiz"
    difficulty: str = "beginner"
    max_players: int = Field(10, ge=2, le=20)
    total_questions: int = Field(10, ge=5, le=30)


class CreateRoomResponse(BaseModel):
    room_code: str
    room_id: str
    game_type: str
    difficulty: str
    max_players: int
    total_questions: int


class JoinRoomRequest(BaseModel):
    display_name: str | None = None


class ParticipantInfo(BaseModel):
    user_id: str
    display_name: str | None
    score: int
    answers_correct: int
    answers_total: int


class RoomStatusResponse(BaseModel):
    room_code: str
    room_id: str
    game_type: str
    difficulty: str
    status: str
    current_question: int
    total_questions: int
    max_players: int
    participants: list[ParticipantInfo]
    created_by: str


class GameQuestionResponse(BaseModel):
    question_index: int
    question_id: int
    question_text: str
    options: list[str]
    category: str | None
    time_limit_seconds: int = 30


class GameAnswerRequest(BaseModel):
    question_id: int
    answer: str
    time_taken_seconds: int | None = None


class GameAnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str | None
    points_earned: int
    total_score: int


class GameResultEntry(BaseModel):
    rank: int
    user_id: str
    display_name: str | None
    score: int
    answers_correct: int
    answers_total: int
    xp_earned: int
