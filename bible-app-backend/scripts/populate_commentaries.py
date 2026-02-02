#!/usr/bin/env python3
"""Seed Bible commentaries (e.g. Matthew Henry style) for study API."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base, SessionLocal, engine
from app.models.study import BibleCommentary

# Minimal seed: one commentary on Genesis 1:1
SEED = [
    {
        "author": "Matthew Henry",
        "book_number": 1,
        "chapter": 1,
        "verse_start": 1,
        "verse_end": 1,
        "commentary": "No principio criou Deus os ceus e a terra. A criacao do mundo em seis dias mostra o poder e a gloria de Deus. Tudo foi criado do nada pela palavra do Senhor.",
        "source": "Matthew Henry",
        "language": "pt-BR",
    },
    {
        "author": "Comentario Biblico",
        "book_number": 1,
        "chapter": 1,
        "verse_start": 1,
        "verse_end": 31,
        "commentary": "O capitulo 1 de Genesis descreve a criacao em seis dias: luz, firmamento, terra e mares, luminares, seres viventes, e por fim o homem e a mulher a imagem de Deus.",
        "source": "Resumo",
        "language": "pt-BR",
    },
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for row in SEED:
            db.add(BibleCommentary(**row))
        db.commit()
        print(f"Inserted {len(SEED)} commentary entries.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
