from uuid import UUID

from sqlalchemy.orm import Session

from app.models.bible import UserAnnotation, UserBookmark, UserHighlight


class UserContentService:
    def __init__(self, db: Session):
        self.db = db

    # Highlights
    def get_highlights(self, user_id: UUID) -> list[UserHighlight]:
        return (
            self.db.query(UserHighlight)
            .filter(UserHighlight.user_id == user_id)
            .all()
        )

    def create_highlight(self, user_id: UUID, data: dict) -> UserHighlight:
        highlight = UserHighlight(user_id=user_id, **data)
        self.db.add(highlight)
        self.db.commit()
        self.db.refresh(highlight)
        return highlight

    def delete_highlight(self, user_id: UUID, highlight_id: UUID) -> bool:
        result = (
            self.db.query(UserHighlight)
            .filter(
                UserHighlight.id == highlight_id,
                UserHighlight.user_id == user_id,
            )
            .delete()
        )
        self.db.commit()
        return result > 0

    # Annotations
    def get_annotations(self, user_id: UUID) -> list[UserAnnotation]:
        return (
            self.db.query(UserAnnotation)
            .filter(UserAnnotation.user_id == user_id)
            .all()
        )

    def create_annotation(self, user_id: UUID, data: dict) -> UserAnnotation:
        annotation = UserAnnotation(user_id=user_id, **data)
        self.db.add(annotation)
        self.db.commit()
        self.db.refresh(annotation)
        return annotation

    def update_annotation(
        self, user_id: UUID, annotation_id: UUID, note: str
    ) -> UserAnnotation | None:
        annotation = (
            self.db.query(UserAnnotation)
            .filter(
                UserAnnotation.id == annotation_id,
                UserAnnotation.user_id == user_id,
            )
            .first()
        )
        if annotation:
            annotation.note = note
            self.db.commit()
            self.db.refresh(annotation)
        return annotation

    def delete_annotation(self, user_id: UUID, annotation_id: UUID) -> bool:
        result = (
            self.db.query(UserAnnotation)
            .filter(
                UserAnnotation.id == annotation_id,
                UserAnnotation.user_id == user_id,
            )
            .delete()
        )
        self.db.commit()
        return result > 0

    # Bookmarks
    def get_bookmarks(self, user_id: UUID) -> list[UserBookmark]:
        return (
            self.db.query(UserBookmark)
            .filter(UserBookmark.user_id == user_id)
            .all()
        )

    def create_bookmark(self, user_id: UUID, data: dict) -> UserBookmark:
        bookmark = UserBookmark(user_id=user_id, **data)
        self.db.add(bookmark)
        self.db.commit()
        self.db.refresh(bookmark)
        return bookmark

    def delete_bookmark(self, user_id: UUID, bookmark_id: UUID) -> bool:
        result = (
            self.db.query(UserBookmark)
            .filter(
                UserBookmark.id == bookmark_id,
                UserBookmark.user_id == user_id,
            )
            .delete()
        )
        self.db.commit()
        return result > 0
