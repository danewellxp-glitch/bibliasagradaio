from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    authorization: str = Header(..., description="Bearer <firebase_token>"),
    db: Session = Depends(get_db),
):
    firebase_token = authorization.replace("Bearer ", "")
    service = AuthService(db)
    user, jwt_token = service.login_with_firebase(firebase_token)
    return TokenResponse(
        access_token=jwt_token,
        user=UserResponse.model_validate(user),
    )
