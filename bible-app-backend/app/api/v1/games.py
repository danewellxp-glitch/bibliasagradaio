import random

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.game import (
    CreateRoomRequest,
    CreateRoomResponse,
    GameAnswerRequest,
    GameAnswerResponse,
    GameQuestionResponse,
    GameResultEntry,
    JoinRoomRequest,
    ParticipantInfo,
    RoomStatusResponse,
)
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/room/create", response_model=CreateRoomResponse)
async def create_room(
    body: CreateRoomRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GameService(db)
    room = service.create_room(
        user_id=user.id,
        game_type=body.game_type,
        difficulty=body.difficulty,
        max_players=body.max_players,
        total_questions=body.total_questions,
    )
    return CreateRoomResponse(
        room_code=room.room_code,
        room_id=str(room.id),
        game_type=room.game_type,
        difficulty=room.difficulty,
        max_players=room.max_players,
        total_questions=room.total_questions,
    )


@router.post("/room/{code}/join")
async def join_room(
    code: str,
    body: JoinRoomRequest = JoinRoomRequest(),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GameService(db)
    room = service.get_room_by_code(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.status != "waiting":
        raise HTTPException(status_code=400, detail="Game already started or finished")

    participants = service.get_participants(room.id)
    if len(participants) >= room.max_players:
        raise HTTPException(status_code=400, detail="Room is full")

    display_name = body.display_name or user.display_name
    service.join_room(room, user.id, display_name)
    return {"message": "Joined successfully", "room_code": code}


@router.get("/room/{code}/status", response_model=RoomStatusResponse)
async def get_room_status(
    code: str,
    db: Session = Depends(get_db),
):
    service = GameService(db)
    room = service.get_room_by_code(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    participants = service.get_participants(room.id)
    return RoomStatusResponse(
        room_code=room.room_code,
        room_id=str(room.id),
        game_type=room.game_type,
        difficulty=room.difficulty,
        status=room.status,
        current_question=room.current_question,
        total_questions=room.total_questions,
        max_players=room.max_players,
        created_by=str(room.created_by),
        participants=[
            ParticipantInfo(
                user_id=str(p.user_id),
                display_name=p.display_name,
                score=p.score or 0,
                answers_correct=p.answers_correct or 0,
                answers_total=p.answers_total or 0,
            )
            for p in participants
        ],
    )


@router.post("/room/{code}/start")
async def start_game(
    code: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GameService(db)
    room = service.get_room_by_code(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if str(room.created_by) != str(user.id):
        raise HTTPException(status_code=403, detail="Only the room creator can start the game")
    if room.status != "waiting":
        raise HTTPException(status_code=400, detail="Game already started or finished")

    service.start_game(room)
    return {"message": "Game started", "status": "playing"}


@router.get("/room/{code}/question", response_model=GameQuestionResponse)
async def get_current_question(
    code: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GameService(db)
    room = service.get_room_by_code(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.status != "playing":
        raise HTTPException(status_code=400, detail="Game is not in progress")

    question = service.get_question_for_room(room)
    if not question:
        raise HTTPException(status_code=404, detail="No more questions available")

    wrong = question.wrong_answers or []
    if not isinstance(wrong, list):
        wrong = list(wrong) if wrong else [wrong]
    options = [question.correct_answer] + list(wrong)
    random.shuffle(options)

    return GameQuestionResponse(
        question_index=room.current_question,
        question_id=question.id,
        question_text=question.question_text,
        options=options,
        category=question.category,
    )


@router.post("/room/{code}/answer", response_model=GameAnswerResponse)
async def submit_game_answer(
    code: str,
    body: GameAnswerRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = GameService(db)
    room = service.get_room_by_code(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.status != "playing":
        raise HTTPException(status_code=400, detail="Game is not in progress")

    try:
        is_correct, correct_answer, explanation, points, total = service.submit_answer(
            room, user.id, body.question_id, body.answer, body.time_taken_seconds
        )
    except ValueError as e:
        if "already answered" in str(e).lower():
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=404, detail=str(e))

    # Auto-advance if all players answered
    if service.check_all_answered(room):
        service.advance_question(room)

    return GameAnswerResponse(
        is_correct=is_correct,
        correct_answer=correct_answer,
        explanation=explanation,
        points_earned=points,
        total_score=total,
    )


@router.get("/room/{code}/results", response_model=list[GameResultEntry])
async def get_game_results(
    code: str,
    db: Session = Depends(get_db),
):
    service = GameService(db)
    room = service.get_room_by_code(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.status != "finished":
        raise HTTPException(status_code=400, detail="Game is not finished yet")

    participants = service.get_participants(room.id)
    return [
        GameResultEntry(
            rank=i + 1,
            user_id=str(p.user_id),
            display_name=p.display_name,
            score=p.score or 0,
            answers_correct=p.answers_correct or 0,
            answers_total=p.answers_total or 0,
            xp_earned=service.calculate_xp(i + 1, p.score or 0),
        )
        for i, p in enumerate(participants)
    ]
