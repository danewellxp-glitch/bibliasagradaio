import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.user import User


class PremiumService:
    def __init__(self, db: Session):
        self.db = db

    def get_subscription(self, user_id: uuid.UUID) -> Subscription | None:
        return (
            self.db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "active",
            )
            .order_by(Subscription.created_at.desc())
            .first()
        )

    def is_premium(self, user_id: uuid.UUID) -> bool:
        sub = self.get_subscription(user_id)
        if not sub:
            return False
        if sub.plan == "free":
            return False
        if sub.expires_at and sub.expires_at < datetime.utcnow():
            sub.status = "expired"
            self.db.commit()
            return False
        return True

    def get_plan(self, user_id: uuid.UUID) -> str:
        sub = self.get_subscription(user_id)
        if not sub:
            return "free"
        return sub.plan

    def verify_and_activate(
        self,
        user_id: uuid.UUID,
        provider: str,
        purchase_token: str,
        product_id: str,
    ) -> Subscription:
        """Verify receipt and activate premium subscription.

        In production, this should validate the purchase_token with
        Google Play or App Store APIs. For now, we trust the client.
        """
        # Determine plan and expiry
        if "annual" in product_id:
            plan = "annual"
            expires_at = datetime.utcnow() + timedelta(days=365)
        else:
            plan = "monthly"
            expires_at = datetime.utcnow() + timedelta(days=30)

        # Deactivate existing subscriptions
        existing = (
            self.db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "active",
            )
            .all()
        )
        for sub in existing:
            sub.status = "cancelled"
            sub.cancelled_at = datetime.utcnow()

        # Create new subscription
        subscription = Subscription(
            user_id=user_id,
            plan=plan,
            status="active",
            provider=provider,
            provider_subscription_id=purchase_token,
            expires_at=expires_at,
        )
        self.db.add(subscription)

        # Update user is_premium flag
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_premium = True

        self.db.commit()
        self.db.refresh(subscription)
        return subscription
