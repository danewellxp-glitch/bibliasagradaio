#!/usr/bin/env python3
"""Seed timeline events for study API."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base, SessionLocal, engine
from app.models.study import TimelineEvent

# Minimal seed: key biblical events
SEED = [
    {"event_name": "Criacao", "description": "Deus cria os ceus e a terra.", "approximate_date": "~4000 BC", "date_start": -4000, "date_end": -4000, "event_type": "creation", "related_books": [1], "related_verses": [["1", "1", "1"]]},
    {"event_name": "Diluvio", "description": "O diluvio de Noe.", "approximate_date": "~2348 BC", "date_start": -2348, "date_end": -2348, "event_type": "flood", "related_books": [6, 7], "related_verses": None},
    {"event_name": "Exodo", "description": "Israel sai do Egito.", "approximate_date": "~1446 BC", "date_start": -1446, "date_end": -1446, "event_type": "exodus", "related_books": [2], "related_verses": None},
    {"event_name": "Nascimento de Jesus", "description": "Jesus nasce em Belem.", "approximate_date": "~4 BC", "date_start": -4, "date_end": -4, "event_type": "birth", "related_books": [40, 42, 43], "related_verses": None},
    {"event_name": "Ministerio de Jesus", "description": "Ministerio publico de Jesus.", "approximate_date": "27-30 AD", "date_start": 27, "date_end": 30, "event_type": "ministry", "related_books": [40, 41, 42, 43], "related_verses": None},
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for row in SEED:
            db.add(TimelineEvent(**row))
        db.commit()
        print(f"Inserted {len(SEED)} timeline events.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
