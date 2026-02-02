from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: int
    difficulty_level: str
    question_type: str
    question_text: str
    options: list[str]
    category: str | None

    class Config:
        from_attributes = True


class AnswerRequest(BaseModel):
    question_id: int
    answer: str
    time_taken_seconds: int | None = None


class AnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str | None
    xp_earned: int
    new_total_xp: int
    streak: int


class QuizStatsResponse(BaseModel):
    total_xp: int
    current_level: int
    current_streak: int
    longest_streak: int
    total_questions_answered: int
    total_correct_answers: int

    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: str
    display_name: str | None
    total_xp: int
    current_level: int
