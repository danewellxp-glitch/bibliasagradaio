from sqlalchemy.orm import Session

from app.models.bible import BibleText, BibleVersion


class BibleService:
    def __init__(self, db: Session):
        self.db = db

    def get_versions(self) -> list[BibleVersion]:
        return self.db.query(BibleVersion).all()

    def get_chapter(
        self, version_code: str, book: int, chapter: int
    ) -> list[BibleText]:
        version = (
            self.db.query(BibleVersion)
            .filter(BibleVersion.code == version_code)
            .first()
        )
        if not version:
            return []
        return (
            self.db.query(BibleText)
            .filter(
                BibleText.version_id == version.id,
                BibleText.book_number == book,
                BibleText.chapter == chapter,
            )
            .order_by(BibleText.verse)
            .all()
        )

    def get_verse(
        self, version_code: str, book: int, chapter: int, verse: int
    ) -> BibleText | None:
        version = (
            self.db.query(BibleVersion)
            .filter(BibleVersion.code == version_code)
            .first()
        )
        if not version:
            return None
        return (
            self.db.query(BibleText)
            .filter(
                BibleText.version_id == version.id,
                BibleText.book_number == book,
                BibleText.chapter == chapter,
                BibleText.verse == verse,
            )
            .first()
        )

    def search(
        self, version_code: str, query: str, limit: int = 50
    ) -> list[BibleText]:
        version = (
            self.db.query(BibleVersion)
            .filter(BibleVersion.code == version_code)
            .first()
        )
        if not version:
            return []
        return (
            self.db.query(BibleText)
            .filter(
                BibleText.version_id == version.id,
                BibleText.text.ilike(f"%{query}%"),
            )
            .order_by(BibleText.book_number, BibleText.chapter, BibleText.verse)
            .limit(limit)
            .all()
        )
