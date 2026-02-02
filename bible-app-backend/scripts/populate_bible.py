#!/usr/bin/env python3
"""
Populate PostgreSQL with Bible texts (ARA, ARC, ACF, KJV) from JSON or CSV.

Usage:
  From bible-app-backend/:
    python scripts/populate_bible.py --seed-only
    python scripts/populate_bible.py --json data/bible_ara.json
    python scripts/populate_bible.py --json data/ara.json --json data/arc.json
    python scripts/populate_bible.py --csv data/bible.csv

JSON format: list of objects with keys:
  version_code, book_number, book_name, chapter, verse, text

CSV format: header row with version_code, book_number, book_name, chapter, verse, text
"""
import argparse
import csv
import json
import os
import sys

# Ensure app is importable when run as script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session

from app.core.database import Base, SessionLocal, engine
# Import all models so tables are created in correct order
from app.models import *  # noqa: F401, F403
from app.models.bible import BibleText, BibleVersion

BIBLE_VERSIONS = [
    {"code": "NVI", "name": "Nova Versão Internacional", "language": "pt-BR"},
    {"code": "ARC", "name": "Almeida Revista e Corrigida", "language": "pt-BR"},
    {"code": "ACF", "name": "Almeida Corrigida e Fiel", "language": "pt-BR"},
    {"code": "KJV", "name": "King James Version", "language": "en-US"},
]

# 66 books: (number, name, chapters)
BIBLE_BOOKS = [
    (1, "Genesis", 50), (2, "Exodo", 40), (3, "Levitico", 27), (4, "Numeros", 36),
    (5, "Deuteronomio", 34), (6, "Josue", 24), (7, "Juizes", 21), (8, "Rute", 4),
    (9, "1 Samuel", 31), (10, "2 Samuel", 24), (11, "1 Reis", 22), (12, "2 Reis", 25),
    (13, "1 Cronicas", 29), (14, "2 Cronicas", 36), (15, "Esdras", 10), (16, "Neemias", 13),
    (17, "Ester", 10), (18, "Jo", 42), (19, "Salmos", 150), (20, "Proverbios", 31),
    (21, "Eclesiastes", 12), (22, "Canticos", 8), (23, "Isaias", 66), (24, "Jeremias", 52),
    (25, "Lamentacoes", 5), (26, "Ezequiel", 48), (27, "Daniel", 12), (28, "Oseias", 14),
    (29, "Joel", 3), (30, "Amos", 9), (31, "Obadias", 1), (32, "Jonas", 4),
    (33, "Miqueias", 7), (34, "Naum", 3), (35, "Habacuque", 3), (36, "Sofonias", 3),
    (37, "Ageu", 2), (38, "Zacarias", 14), (39, "Malaquias", 4),
    (40, "Mateus", 28), (41, "Marcos", 16), (42, "Lucas", 24), (43, "Joao", 21),
    (44, "Atos", 28), (45, "Romanos", 16), (46, "1 Corintios", 16), (47, "2 Corintios", 13),
    (48, "Galatas", 6), (49, "Efesios", 6), (50, "Filipenses", 4), (51, "Colossenses", 4),
    (52, "1 Tessalonicenses", 5), (53, "2 Tessalonicenses", 3), (54, "1 Timoteo", 6),
    (55, "2 Timoteo", 4), (56, "Tito", 3), (57, "Filemom", 1), (58, "Hebreus", 13),
    (59, "Tiago", 5), (60, "1 Pedro", 5), (61, "2 Pedro", 3), (62, "1 Joao", 5),
    (63, "2 Joao", 1), (64, "3 Joao", 1), (65, "Judas", 1), (66, "Apocalipse", 22),
]

# Minimal seed: Genesis 1:1-31 (ARA) for quick testing
GENESIS_1_ARA = [
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 1, "text": "No principio criou Deus os ceus e a terra."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 2, "text": "A terra, porem, estava sem forma e vazia; havia trevas sobre a face do abismo, e o Espirito de Deus pairava por sobre as aguas."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 3, "text": "Disse Deus: Haja luz. E houve luz."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 4, "text": "E viu Deus que a luz era boa; e fez separacao entre a luz e as trevas."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 5, "text": "Chamou Deus à luz Dia, e às trevas Noite. Houve tarde e manha, o primeiro dia."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 6, "text": "E disse Deus: Haja firmamento no meio das aguas e separacao entre aguas e aguas."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 7, "text": "Fez Deus o firmamento e separacao entre as aguas que estavam debaixo do firmamento e as aguas que estavam sobre o firmamento. E assim se fez."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 8, "text": "E a esse firmamento chamou Deus Ceu. Houve tarde e manha, o segundo dia."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 9, "text": "Disse tambem Deus: Ajuntem-se as aguas debaixo dos ceus num so lugar, e apareca a porcao seca. E assim se fez."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 10, "text": "À porcao seca chamou Deus Terra e ao ajuntamento das aguas Mares. E viu Deus que era bom."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 11, "text": "E disse: Produza a terra relva, ervas que deem semente e arvores frutiferas que deem fruto segundo a sua especie, cuja semente esteja nele sobre a terra. E assim se fez."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 12, "text": "A terra, pois, produziu relva, ervas que davam semente segundo a sua especie e arvores que davam fruto, cuja semente estava nele, conforme a sua especie. E viu Deus que era bom."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 13, "text": "Houve tarde e manha, o terceiro dia."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 14, "text": "Disse Deus: Haja luzeiros no firmamento dos ceus, para fazerem separacao entre o dia e a noite; e sejam eles para sinais, para estacoes, para dias e anos."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 15, "text": "E sejam para luzeiros no firmamento dos ceus para alumiar a terra. E assim se fez."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 16, "text": "Fez Deus os dois grandes luzeiros: o luzeiro maior para governar o dia, e o luzeiro menor para governar a noite; e fez tambem as estrelas."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 17, "text": "E Deus os pos no firmamento dos ceus para alumiar a terra,"},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 18, "text": "para governar o dia e a noite e fazer separacao entre a luz e as trevas. E viu Deus que era bom."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 19, "text": "Houve tarde e manha, o quarto dia."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 20, "text": "Disse Deus: Povoem-se as aguas de enxames de seres viventes; e voem as aves sobre a terra, sob o firmamento dos ceus."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 21, "text": "Criou Deus, pois, os grandes animais marinhos e todos os seres viventes que rastejam, os quais povoavam as aguas, segundo as suas especies; e todas as aves, segundo as suas especies. E viu Deus que era bom."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 22, "text": "E Deus os abencoou, dizendo: Sede fecundos, multiplicai-vos e enchei as aguas dos mares; e, na terra, se multipliquem as aves."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 23, "text": "Houve tarde e manha, o quinto dia."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 24, "text": "Disse Deus: Produza a terra seres viventes, conforme a sua especie: animais domesticos, répteis e animais selváticos, segundo a sua especie. E assim se fez."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 25, "text": "E fez Deus os animais selváticos, segundo a sua especie, e os animais domesticos, segundo a sua especie, e todos os répteis da terra, segundo a sua especie. E viu Deus que era bom."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 26, "text": "E disse Deus: Façamos o homem à nossa imagem, conforme a nossa semelhança; e dominem sobre os peixes do mar, e sobre as aves dos ceus, e sobre os animais domesticos, e sobre toda a terra, e sobre todo réptil que rasteja pela terra."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 27, "text": "Criou Deus, pois, o homem à sua imagem, à imagem de Deus o criou; homem e mulher os criou."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 28, "text": "E Deus os abencoou e lhes disse: Sede fecundos, multiplicai-vos, enchei a terra e sujeitai-a; dominai sobre os peixes do mar, sobre as aves dos ceus e sobre todo animal que rasteja pela terra."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 29, "text": "E disse Deus: Eis que vos dou todas as ervas que dao semente e que estao sobre a face de toda a terra e todas as arvores em que ha fruto que dê semente; ser-vos-ao para alimento."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 30, "text": "E a todos os animais da terra, e a todas as aves dos ceus e a todo ser vivente que rasteja sobre a terra, dou todas as ervas verdes por alimento. E assim se fez."},
    {"version_code": "ARA", "book_number": 1, "book_name": "Genesis", "chapter": 1, "verse": 31, "text": "Viu Deus tudo quanto fizera, e eis que era muito bom. Houve tarde e manha, o sexto dia."},
]


def ensure_tables():
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


def get_or_create_versions(db: Session) -> dict[str, int]:
    """Create version records if missing; return mapping code -> id."""
    code_to_id = {}
    for v in BIBLE_VERSIONS:
        existing = db.query(BibleVersion).filter(BibleVersion.code == v["code"]).first()
        if existing:
            code_to_id[v["code"]] = existing.id
        else:
            version = BibleVersion(
                code=v["code"],
                name=v["name"],
                language=v["language"],
                is_premium=False,
                is_available_offline=True,
            )
            db.add(version)
            db.flush()
            code_to_id[v["code"]] = version.id
    db.commit()
    return code_to_id


def load_json(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        data = [data]
    return data


def load_csv(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["book_number"] = int(row["book_number"])
            row["chapter"] = int(row["chapter"])
            row["verse"] = int(row["verse"])
            rows.append(row)
    return rows


def insert_verses(db: Session, code_to_id: dict[str, int], verses: list[dict], batch_size: int = 2000):
    """Insert verses; verses are dicts with version_code, book_number, book_name, chapter, verse, text."""
    inserted = 0
    for i in range(0, len(verses), batch_size):
        batch = verses[i : i + batch_size]
        for v in batch:
            code = v["version_code"]
            if code not in code_to_id:
                continue
            db.add(
                BibleText(
                    version_id=code_to_id[code],
                    book_number=v["book_number"],
                    book_name=v["book_name"],
                    chapter=v["chapter"],
                    verse=v["verse"],
                    text=v["text"],
                )
            )
        db.commit()
        inserted += len(batch)
        print(f"  Inserted {inserted} verses...")
    return inserted


def main():
    parser = argparse.ArgumentParser(description="Populate Bible texts from JSON/CSV")
    parser.add_argument("--json", action="append", help="Path(s) to JSON file(s)")
    parser.add_argument("--csv", action="append", help="Path(s) to CSV file(s)")
    parser.add_argument("--seed-only", action="store_true", help="Only create versions and insert Genesis 1 (ARA) seed")
    args = parser.parse_args()

    ensure_tables()
    db = SessionLocal()
    try:
        code_to_id = get_or_create_versions(db)
        print("Versions:", code_to_id)

        if args.seed_only:
            n = insert_verses(db, code_to_id, GENESIS_1_ARA)
            print(f"Seed: inserted {n} verses (Genesis 1 ARA).")
            return

        all_verses = []
        if args.json:
            for path in args.json:
                if not os.path.isfile(path):
                    print(f"Warning: {path} not found, skipping.")
                    continue
                data = load_json(path)
                all_verses.extend(data)
                print(f"Loaded {len(data)} verses from {path}")
        if args.csv:
            for path in args.csv:
                if not os.path.isfile(path):
                    print(f"Warning: {path} not found, skipping.")
                    continue
                data = load_csv(path)
                all_verses.extend(data)
                print(f"Loaded {len(data)} verses from CSV {path}")

        if not all_verses and not args.seed_only:
            print("No files given. Use --seed-only to insert Genesis 1 (ARA) or provide --json/--csv.")
            return
        if all_verses:
            total = insert_verses(db, code_to_id, all_verses)
            print(f"Total inserted: {total} verses.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
