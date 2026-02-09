from sqlalchemy.orm import Session

from app.models.study import (
    BibleCommentary,
    BibleMap,
    CrossReference,
    TimelineEvent,
)


class StudyService:
    def __init__(self, db: Session):
        self.db = db

    def get_commentaries(
        self,
        book_number: int,
        chapter: int | None = None,
        verse: int | None = None,
        limit: int = 20,
    ):
        q = self.db.query(BibleCommentary).filter(
            BibleCommentary.book_number == book_number
        )
        if chapter is not None:
            q = q.filter(BibleCommentary.chapter == chapter)
        if verse is not None:
            q = q.filter(
                BibleCommentary.verse_start <= verse,
                BibleCommentary.verse_end >= verse,
            )
        return q.order_by(BibleCommentary.chapter, BibleCommentary.verse_start).limit(limit).all()

    def get_cross_references(
        self,
        book_number: int,
        chapter: int,
        verse: int,
        limit: int = 50,
    ):
        return (
            self.db.query(CrossReference)
            .filter(
                CrossReference.from_book == book_number,
                CrossReference.from_chapter == chapter,
                CrossReference.from_verse == verse,
            )
            .limit(limit)
            .all()
        )

    def get_timeline_events(self, limit: int = 100):
        return (
            self.db.query(TimelineEvent)
            .order_by(TimelineEvent.date_start.asc().nulls_last())
            .limit(limit)
            .all()
        )

    def get_maps(self, period: str | None = None, limit: int = 50):
        q = self.db.query(BibleMap)
        if period:
            q = q.filter(BibleMap.period == period)
        return q.limit(limit).all()

    def get_verse_context(
        self,
        book_number: int,
        chapter: int,
        verse: int,
    ) -> dict:
        commentaries = self.get_commentaries(book_number, chapter, verse, limit=10)
        cross_refs = self.get_cross_references(book_number, chapter, verse, limit=20)
        timeline = (
            self.db.query(TimelineEvent)
            .filter(TimelineEvent.related_books.contains([book_number]))
            .order_by(TimelineEvent.date_start.asc().nulls_last())
            .limit(10)
            .all()
        )
        return {
            "commentaries": commentaries,
            "cross_references": cross_refs,
            "timeline_events": timeline,
        }
