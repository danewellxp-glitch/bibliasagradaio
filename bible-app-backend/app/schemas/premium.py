from datetime import datetime

from pydantic import BaseModel


class PremiumStatusResponse(BaseModel):
    is_premium: bool
    plan: str
    status: str
    expires_at: datetime | None
    ai_daily_limit: int


class VerifyReceiptRequest(BaseModel):
    provider: str  # google_play or app_store
    purchase_token: str
    product_id: str  # monthly_premium or annual_premium


class VerifyReceiptResponse(BaseModel):
    success: bool
    plan: str
    expires_at: datetime | None
    message: str
