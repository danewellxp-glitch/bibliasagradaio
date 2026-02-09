from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.bible import BibleText, BibleVersion

# Curated list of popular/inspirational verses (book, chapter, verse)
VERSE_OF_THE_DAY_LIST = [
    (43, 3, 16), (19, 23, 1), (45, 8, 28), (50, 4, 13), (23, 41, 10),
    (20, 3, 5), (24, 29, 11), (19, 46, 10), (45, 12, 2), (58, 11, 1),
    (19, 119, 105), (40, 11, 28), (1, 1, 1), (43, 14, 6), (19, 27, 1),
    (23, 40, 31), (50, 4, 6), (20, 22, 6), (45, 8, 38), (19, 91, 1),
    (40, 6, 33), (43, 8, 32), (19, 37, 4), (46, 13, 4), (19, 121, 1),
    (40, 5, 14), (43, 16, 33), (19, 34, 18), (55, 1, 7), (19, 103, 1),
    (40, 28, 20), (45, 5, 8), (19, 139, 14), (48, 5, 22), (19, 150, 6),
    (59, 1, 5), (43, 1, 1), (19, 51, 10), (49, 2, 8), (19, 100, 4),
    (42, 1, 37), (43, 15, 13), (19, 63, 1), (20, 16, 3), (19, 145, 18),
    (40, 7, 7), (43, 10, 10), (19, 40, 1), (51, 3, 23), (19, 118, 24),
    (62, 4, 8), (19, 56, 3), (45, 15, 13), (40, 22, 37), (19, 19, 1),
    (43, 11, 25), (19, 90, 12), (47, 5, 17), (19, 86, 5), (44, 1, 8),
    (20, 18, 10), (19, 46, 1), (58, 12, 2), (19, 33, 4), (60, 5, 7),
    (42, 6, 31), (19, 62, 1), (23, 53, 5), (19, 73, 26), (40, 19, 26),
    (43, 13, 34), (19, 42, 1), (20, 4, 23), (19, 84, 11), (45, 1, 16),
    (19, 16, 11), (40, 5, 16), (43, 6, 35), (19, 23, 4), (49, 6, 10),
    (19, 37, 5), (43, 3, 30), (19, 95, 1), (57, 4, 13), (19, 107, 1),
    (23, 9, 6), (19, 8, 1), (40, 5, 6), (19, 111, 10), (43, 4, 14),
    (19, 1, 1), (40, 4, 4), (19, 22, 1), (20, 1, 7), (19, 24, 1),
    (46, 10, 13), (19, 31, 24), (40, 6, 9), (19, 133, 1), (43, 17, 3),
    (19, 139, 1), (40, 10, 28), (19, 5, 3), (20, 31, 30), (19, 18, 2),
    (40, 16, 26), (19, 143, 8), (43, 20, 31), (19, 147, 3), (45, 10, 17),
    (19, 119, 11), (40, 11, 29), (19, 65, 1), (23, 26, 3), (19, 130, 5),
    (42, 11, 9), (19, 68, 19), (53, 3, 3), (19, 89, 1), (45, 6, 23),
    (19, 113, 3), (40, 5, 44), (19, 30, 5), (20, 15, 1), (19, 138, 8),
    (43, 14, 27), (19, 71, 1), (58, 4, 16), (19, 9, 1), (52, 5, 16),
    (19, 25, 4), (40, 18, 20), (19, 32, 8), (20, 2, 6), (19, 40, 3),
    (43, 5, 24), (19, 55, 22), (48, 2, 20), (19, 77, 1), (54, 4, 12),
    (19, 146, 1), (40, 5, 9), (19, 85, 10), (20, 27, 17), (19, 57, 1),
    (42, 12, 32), (19, 104, 1), (23, 55, 6), (19, 116, 1), (44, 2, 38),
    (19, 34, 1), (40, 6, 14), (19, 148, 1), (20, 12, 1), (19, 102, 1),
    (43, 12, 46), (19, 127, 1), (49, 3, 20), (19, 108, 1), (45, 3, 23),
    (19, 96, 1), (40, 5, 3), (19, 66, 1), (23, 12, 2), (19, 126, 3),
    (42, 10, 27), (19, 103, 12), (58, 13, 5), (19, 145, 3), (60, 2, 9),
    (19, 106, 1), (40, 11, 30), (19, 72, 18), (20, 10, 12), (19, 112, 1),
    (43, 21, 17), (19, 119, 130), (47, 12, 9), (19, 136, 1), (46, 15, 58),
    (19, 149, 1), (40, 6, 21), (19, 93, 1), (20, 3, 1), (19, 91, 11),
    (42, 15, 7), (19, 92, 1), (23, 43, 19), (19, 11, 1), (45, 8, 1),
    (19, 20, 4), (40, 5, 10), (19, 4, 8), (20, 19, 21), (19, 109, 26),
    (43, 15, 5), (19, 115, 1), (48, 6, 9), (19, 69, 30), (52, 5, 18),
    (19, 144, 1), (40, 24, 35), (19, 97, 1), (20, 11, 25), (19, 48, 1),
    (42, 18, 27), (19, 67, 1), (23, 49, 15), (19, 60, 1), (44, 4, 12),
    (19, 119, 9), (40, 17, 20), (19, 114, 1), (20, 14, 26), (19, 36, 5),
    (43, 14, 1), (19, 121, 7), (50, 1, 6), (19, 105, 1), (45, 11, 33),
    (19, 19, 14), (40, 7, 12), (19, 117, 1), (20, 16, 9), (19, 37, 23),
    (42, 2, 10), (19, 99, 1), (23, 58, 11), (19, 135, 1), (45, 12, 12),
    (19, 142, 1), (40, 5, 7), (19, 83, 1), (20, 6, 6), (19, 101, 1),
    (43, 8, 12), (19, 128, 1), (49, 4, 32), (19, 78, 1), (54, 6, 12),
    (19, 110, 1), (40, 5, 8), (19, 26, 1), (20, 28, 26), (19, 141, 1),
    (42, 9, 23), (19, 47, 1), (23, 60, 1), (19, 61, 1), (44, 16, 31),
    (19, 119, 133), (40, 21, 22), (19, 7, 1), (20, 8, 11), (19, 39, 7),
    (43, 7, 37), (19, 131, 1), (47, 4, 18), (19, 88, 1), (46, 2, 9),
]


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

    def get_verse_of_the_day(self, version_code: str) -> BibleText | None:
        """Get a deterministic verse of the day based on date."""
        day_index = date.today().timetuple().tm_yday % len(VERSE_OF_THE_DAY_LIST)
        book, chapter, verse = VERSE_OF_THE_DAY_LIST[day_index]
        return self.get_verse(version_code, book, chapter, verse)

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
