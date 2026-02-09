#!/usr/bin/env python3
"""Populate quiz_questions from data/quiz_questions.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base, SessionLocal, engine
from app.models.quiz import QuizQuestion

DEFAULT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "quiz_questions.json",
)


def main():
    path = os.environ.get("QUIZ_JSON", DEFAULT_PATH)
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Dedup: skip if question_text already exists (evita erro ao re-executar)
        existing_texts = {r.question_text for r in db.query(QuizQuestion.question_text).all()}
        skipped = 0
        for item in data:
            qt = item.get("question_text")
            if qt and qt in existing_texts:
                skipped += 1
                continue
            wrong = item.get("wrong_answers")
            if wrong is not None and not isinstance(wrong, list):
                wrong = [wrong]
            q = QuizQuestion(
                    difficulty_level=item["difficulty_level"],
                    question_type=item["question_type"],
                    question_text=item["question_text"],
                    correct_answer=item["correct_answer"],
                    wrong_answers=wrong,
                    explanation=item.get("explanation"),
                    related_verses=item.get("related_verses"),
                    category=item.get("category"),
                )
            db.add(q)
            if qt:
                existing_texts.add(qt)
        db.commit()
        print(f"Inserted {len(data) - skipped} quiz questions from {path} ({skipped} duplicates skipped).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
