#!/usr/bin/env python3
"""Seed cross-references (e.g. TSK style) for study API."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base, SessionLocal, engine
from app.models.study import CrossReference

# Minimal seed: cross-refs from Genesis 1:1 and John 1:1
SEED = [
    {"from_book": 1, "from_chapter": 1, "from_verse": 1, "to_book": 43, "to_chapter": 1, "to_verse": 1, "relationship_type": "parallel"},
    {"from_book": 1, "from_chapter": 1, "from_verse": 1, "to_book": 19, "to_chapter": 33, "to_verse": 6, "relationship_type": "theme"},
    {"from_book": 43, "from_chapter": 1, "from_verse": 1, "to_book": 1, "to_chapter": 1, "to_verse": 1, "relationship_type": "parallel"},
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for row in SEED:
            db.add(CrossReference(**row))
        db.commit()
        print(f"Inserted {len(SEED)} cross-reference entries.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
