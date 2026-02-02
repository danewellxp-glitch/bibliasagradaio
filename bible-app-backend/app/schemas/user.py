from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    email: str
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    preferred_version: str
    preferred_language: str
    is_premium: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    preferred_version: Optional[str] = None
    preferred_language: Optional[str] = None
