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
        for item in data:
            wrong = item.get("wrong_answers")
            if wrong is not None and not isinstance(wrong, list):
                wrong = [wrong]
            db.add(
                QuizQuestion(
                    difficulty_level=item["difficulty_level"],
                    question_type=item["question_type"],
                    question_text=item["question_text"],
                    correct_answer=item["correct_answer"],
                    wrong_answers=wrong,
                    explanation=item.get("explanation"),
                    related_verses=item.get("related_verses"),
                    category=item.get("category"),
                )
            )
        db.commit()
        print(f"Inserted {len(data)} quiz questions from {path}.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
