from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.premium import (
    PremiumStatusResponse,
    VerifyReceiptRequest,
    VerifyReceiptResponse,
)
from app.services.premium_service import PremiumService

router = APIRouter(prefix="/premium", tags=["premium"])


@router.get("/status", response_model=PremiumStatusResponse)
async def get_premium_status(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PremiumService(db)
    is_premium = service.is_premium(user.id)
    plan = service.get_plan(user.id)
    sub = service.get_subscription(user.id)

    return PremiumStatusResponse(
        is_premium=is_premium,
        plan=plan,
        status=sub.status if sub else "none",
        expires_at=sub.expires_at if sub else None,
        ai_daily_limit=(
            settings.AI_RATE_LIMIT_PREMIUM
            if is_premium
            else settings.AI_RATE_LIMIT_FREE
        ),
    )


@router.post("/verify-receipt", response_model=VerifyReceiptResponse)
async def verify_receipt(
    body: VerifyReceiptRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = PremiumService(db)
    sub = service.verify_and_activate(
        user_id=user.id,
        provider=body.provider,
        purchase_token=body.purchase_token,
        product_id=body.product_id,
    )
    return VerifyReceiptResponse(
        success=True,
        plan=sub.plan,
        expires_at=sub.expires_at,
        message=f"Plano {sub.plan} ativado com sucesso!",
    )
