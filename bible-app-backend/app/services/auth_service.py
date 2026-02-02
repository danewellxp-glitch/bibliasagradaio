from sqlalchemy.orm import Session

from app.core.security import create_jwt_token, verify_firebase_token
from app.models.user import User


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login_with_firebase(self, firebase_token: str) -> tuple[User, str]:
        decoded = verify_firebase_token(firebase_token)
        firebase_uid = decoded["uid"]
        email = decoded.get("email", "")
        name = decoded.get("name")
        photo = decoded.get("picture")

        user = self.db.query(User).filter(User.firebase_uid == firebase_uid).first()

        if not user:
            user = User(
                firebase_uid=firebase_uid,
                email=email,
                display_name=name,
                photo_url=photo,
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

        jwt_token = create_jwt_token(str(user.id))
        return user, jwt_token
