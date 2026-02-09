import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    plan = Column(String(20), nullable=False, default="free")  # free, monthly, annual
    status = Column(String(20), nullable=False, default="active")  # active, cancelled, expired
    provider = Column(String(20))  # google_play, app_store
    provider_subscription_id = Column(String(200))
    started_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime)
    cancelled_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
