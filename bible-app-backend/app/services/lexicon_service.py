from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.study import LexiconEntry, WordOccurrence


class LexiconService:
    def __init__(self, db: Session):
        self.db = db

    def get_lexicon_entry(self, strong_number: str) -> LexiconEntry | None:
        return (
            self.db.query(LexiconEntry)
            .filter(LexiconEntry.strong_number == strong_number.upper())
            .first()
        )

    def search_lexicon(self, query: str, limit: int = 20) -> list[LexiconEntry]:
        pattern = f"%{query}%"
        return (
            self.db.query(LexiconEntry)
            .filter(
                or_(
                    LexiconEntry.original_word.ilike(pattern),
                    LexiconEntry.transliteration.ilike(pattern),
                    LexiconEntry.basic_meaning.ilike(pattern),
                    LexiconEntry.strong_number.ilike(pattern),
                )
            )
            .limit(limit)
            .all()
        )

    def get_word_occurrences(
        self, strong_number: str, limit: int = 50
    ) -> list[WordOccurrence]:
        entry = self.get_lexicon_entry(strong_number)
        if entry is None:
            return []
        return (
            self.db.query(WordOccurrence)
            .filter(WordOccurrence.lexicon_entry_id == entry.id)
            .order_by(
                WordOccurrence.book_number,
                WordOccurrence.chapter,
                WordOccurrence.verse,
            )
            .limit(limit)
            .all()
        )
