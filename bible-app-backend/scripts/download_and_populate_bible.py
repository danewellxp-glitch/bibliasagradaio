#!/usr/bin/env python3
"""
Download Bible texts from GitHub and populate PostgreSQL database.

Downloads ACF, ARC, ARA (Portuguese) and KJV (English) from open-source repositories
and inserts all ~124,000 verses into the database.

Usage (from bible-app-backend folder):
  docker exec -it bibliasagradaio-api-1 python scripts/download_and_populate_bible.py

Or run directly if you have Python environment set up:
  python scripts/download_and_populate_bible.py
"""
import json
import os
import sys
import urllib.request
import urllib.error
from typing import Any

# Ensure app is importable when run as script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import Base, SessionLocal, engine
from app.models import *  # noqa: F401, F403
from app.models.bible import BibleText, BibleVersion

# GitHub raw URLs for Bible JSONs
BIBLE_SOURCES = {
    "ACF": "https://raw.githubusercontent.com/MaatheusGois/bible/main/versions/pt-br/acf.json",
    "ARC": "https://raw.githubusercontent.com/MaatheusGois/bible/main/versions/pt-br/arc.json",
    "NVI": "https://raw.githubusercontent.com/MaatheusGois/bible/main/versions/pt-br/nvi.json",
    "KJV": "https://raw.githubusercontent.com/MaatheusGois/bible/main/versions/en/kjv.json",
}

# Alternative KJV source if main fails
KJV_ALTERNATIVE = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json"

# Version metadata
BIBLE_VERSIONS = {
    "NVI": {"name": "Nova Versão Internacional", "language": "pt-BR"},
    "ARC": {"name": "Almeida Revista e Corrigida", "language": "pt-BR"},
    "ACF": {"name": "Almeida Corrigida e Fiel", "language": "pt-BR"},
    "KJV": {"name": "King James Version", "language": "en-US"},
}

# Book ID to number mapping (GitHub JSON uses abbreviations like "gn", "ex", etc.)
# These are the IDs used in the MaatheusGois/bible repo
BOOK_ID_TO_NUMBER = {
    # Old Testament
    "gn": 1, "ge": 1, "gen": 1,
    "ex": 2, "exo": 2,
    "lv": 3, "le": 3, "lev": 3,
    "nm": 4, "nu": 4, "num": 4,
    "dt": 5, "de": 5, "deu": 5,
    "js": 6, "jos": 6, "josh": 6,
    "jz": 7, "jdg": 7, "jud": 7,
    "rt": 8, "ru": 8, "rut": 8, "ruth": 8,
    "1sm": 9, "1sa": 9,
    "2sm": 10, "2sa": 10,
    "1rs": 11, "1ki": 11, "1kgs": 11,
    "2rs": 12, "2ki": 12, "2kgs": 12,
    "1cr": 13, "1ch": 13, "1chr": 13,
    "2cr": 14, "2ch": 14, "2chr": 14,
    "ed": 15, "ezr": 15, "ezra": 15,
    "ne": 16, "neh": 16,
    "et": 17, "est": 17, "esth": 17,
    "jó": 18, "job": 18,
    "sl": 19, "ps": 19, "psa": 19, "psalm": 19, "psalms": 19,
    "pv": 20, "pr": 20, "pro": 20, "prov": 20,
    "ec": 21, "ecc": 21, "eccl": 21,
    "ct": 22, "so": 22, "sng": 22, "song": 22, "sos": 22,
    "is": 23, "isa": 23,
    "jr": 24, "je": 24, "jer": 24,
    "lm": 25, "la": 25, "lam": 25,
    "ez": 26, "eze": 26, "ezek": 26,
    "dn": 27, "da": 27, "dan": 27,
    "os": 28, "ho": 28, "hos": 28,
    "jl": 29, "joe": 29, "joel": 29,
    "am": 30, "amo": 30, "amos": 30,
    "ob": 31, "oba": 31, "obad": 31,
    "jn": 32, "jon": 32, "jonah": 32,
    "mq": 33, "mi": 33, "mic": 33,
    "na": 34, "nah": 34,
    "hc": 35, "hab": 35,
    "sf": 36, "zep": 36, "zeph": 36,
    "ag": 37, "hag": 37,
    "zc": 38, "zec": 38, "zech": 38,
    "ml": 39, "mal": 39,
    # New Testament
    "mt": 40, "mat": 40, "matt": 40,
    "mc": 41, "mr": 41, "mk": 41, "mar": 41, "mark": 41,
    "lc": 42, "lu": 42, "lk": 42, "luk": 42, "luke": 42,
    "jo": 43, "joa": 43, "joh": 43, "john": 43,
    "at": 44, "ac": 44, "act": 44, "acts": 44,
    "rm": 45, "ro": 45, "rom": 45,
    "1co": 46, "1cor": 46,
    "2co": 47, "2cor": 47,
    "gl": 48, "ga": 48, "gal": 48,
    "ef": 49, "eph": 49,
    "fp": 50, "php": 50, "phi": 50, "phil": 50,
    "cl": 51, "col": 51,
    "1ts": 52, "1th": 52, "1thess": 52,
    "2ts": 53, "2th": 53, "2thess": 53,
    "1tm": 54, "1ti": 54, "1tim": 54,
    "2tm": 55, "2ti": 55, "2tim": 55,
    "tt": 56, "tit": 56, "titus": 56,
    "fm": 57, "phm": 57, "phlm": 57,
    "hb": 58, "he": 58, "heb": 58,
    "tg": 59, "jas": 59, "jam": 59, "james": 59,
    "1pe": 60, "1pt": 60, "1pet": 60,
    "2pe": 61, "2pt": 61, "2pet": 61,
    "1jo": 62, "1jn": 62, "1john": 62,
    "2jo": 63, "2jn": 63, "2john": 63,
    "3jo": 64, "3jn": 64, "3john": 64,
    "jd": 65, "jude": 65,
    "ap": 66, "re": 66, "rev": 66, "revelation": 66,
}

# Book names in Portuguese (for display)
BOOK_NAMES_PT = {
    1: "Gênesis", 2: "Êxodo", 3: "Levítico", 4: "Números", 5: "Deuteronômio",
    6: "Josué", 7: "Juízes", 8: "Rute", 9: "1 Samuel", 10: "2 Samuel",
    11: "1 Reis", 12: "2 Reis", 13: "1 Crônicas", 14: "2 Crônicas", 15: "Esdras",
    16: "Neemias", 17: "Ester", 18: "Jó", 19: "Salmos", 20: "Provérbios",
    21: "Eclesiastes", 22: "Cânticos", 23: "Isaías", 24: "Jeremias", 25: "Lamentações",
    26: "Ezequiel", 27: "Daniel", 28: "Oséias", 29: "Joel", 30: "Amós",
    31: "Obadias", 32: "Jonas", 33: "Miquéias", 34: "Naum", 35: "Habacuque",
    36: "Sofonias", 37: "Ageu", 38: "Zacarias", 39: "Malaquias",
    40: "Mateus", 41: "Marcos", 42: "Lucas", 43: "João", 44: "Atos",
    45: "Romanos", 46: "1 Coríntios", 47: "2 Coríntios", 48: "Gálatas", 49: "Efésios",
    50: "Filipenses", 51: "Colossenses", 52: "1 Tessalonicenses", 53: "2 Tessalonicenses",
    54: "1 Timóteo", 55: "2 Timóteo", 56: "Tito", 57: "Filemom", 58: "Hebreus",
    59: "Tiago", 60: "1 Pedro", 61: "2 Pedro", 62: "1 João", 63: "2 João",
    64: "3 João", 65: "Judas", 66: "Apocalipse",
}

# Book names in English (for KJV)
BOOK_NAMES_EN = {
    1: "Genesis", 2: "Exodus", 3: "Leviticus", 4: "Numbers", 5: "Deuteronomy",
    6: "Joshua", 7: "Judges", 8: "Ruth", 9: "1 Samuel", 10: "2 Samuel",
    11: "1 Kings", 12: "2 Kings", 13: "1 Chronicles", 14: "2 Chronicles", 15: "Ezra",
    16: "Nehemiah", 17: "Esther", 18: "Job", 19: "Psalms", 20: "Proverbs",
    21: "Ecclesiastes", 22: "Song of Solomon", 23: "Isaiah", 24: "Jeremiah", 25: "Lamentations",
    26: "Ezekiel", 27: "Daniel", 28: "Hosea", 29: "Joel", 30: "Amos",
    31: "Obadiah", 32: "Jonah", 33: "Micah", 34: "Nahum", 35: "Habakkuk",
    36: "Zephaniah", 37: "Haggai", 38: "Zechariah", 39: "Malachi",
    40: "Matthew", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts",
    45: "Romans", 46: "1 Corinthians", 47: "2 Corinthians", 48: "Galatians", 49: "Ephesians",
    50: "Philippians", 51: "Colossians", 52: "1 Thessalonians", 53: "2 Thessalonians",
    54: "1 Timothy", 55: "2 Timothy", 56: "Titus", 57: "Philemon", 58: "Hebrews",
    59: "James", 60: "1 Peter", 61: "2 Peter", 62: "1 John", 63: "2 John",
    64: "3 John", 65: "Jude", 66: "Revelation",
}


def download_json(url: str) -> Any:
    """Download JSON from URL."""
    print(f"  Downloading from {url}...")
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (BibleApp/1.0)"}
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read().decode("utf-8-sig")  # Handle BOM
            return json.loads(data)
    except urllib.error.URLError as e:
        print(f"  Error downloading: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"  Error parsing JSON: {e}")
        return None


def parse_github_bible(data: list[dict], version_code: str) -> list[dict]:
    """
    Parse GitHub Bible JSON format:
    [
      {"id": "gn", "name": "Gênesis", "chapters": [[v1, v2, ...], [v1, v2, ...], ...]},
      ...
    ]
    
    Returns flat list of verses:
    [
      {"version_code": "ACF", "book_number": 1, "book_name": "Gênesis", "chapter": 1, "verse": 1, "text": "..."},
      ...
    ]
    """
    verses = []
    is_english = version_code == "KJV"
    book_names = BOOK_NAMES_EN if is_english else BOOK_NAMES_PT
    
    for book_idx, book in enumerate(data):
        book_id = book.get("id", "").lower()
        book_name_from_json = book.get("name", "")
        chapters = book.get("chapters", [])
        
        # Try to get book number from ID mapping
        book_number = BOOK_ID_TO_NUMBER.get(book_id)
        
        # If not found, try by position (0-indexed)
        if book_number is None:
            book_number = book_idx + 1
            if book_number > 66:
                print(f"    Warning: Skipping unknown book: {book_id} ({book_name_from_json})")
                continue
        
        # Get proper book name
        book_name = book_names.get(book_number, book_name_from_json)
        
        for chapter_idx, chapter_verses in enumerate(chapters):
            chapter_number = chapter_idx + 1
            
            for verse_idx, verse_text in enumerate(chapter_verses):
                verse_number = verse_idx + 1
                
                if not verse_text or not isinstance(verse_text, str):
                    continue
                
                verses.append({
                    "version_code": version_code,
                    "book_number": book_number,
                    "book_name": book_name,
                    "chapter": chapter_number,
                    "verse": verse_number,
                    "text": verse_text.strip(),
                })
    
    return verses


def ensure_tables():
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


def get_or_create_versions(db: Session) -> dict[str, int]:
    """Create version records if missing; return mapping code -> id."""
    code_to_id = {}
    for code, meta in BIBLE_VERSIONS.items():
        existing = db.query(BibleVersion).filter(BibleVersion.code == code).first()
        if existing:
            code_to_id[code] = existing.id
        else:
            version = BibleVersion(
                code=code,
                name=meta["name"],
                language=meta["language"],
                is_premium=False,
                is_available_offline=True,
            )
            db.add(version)
            db.flush()
            code_to_id[code] = version.id
    db.commit()
    return code_to_id


def clear_existing_verses(db: Session, version_id: int):
    """Delete all existing verses for a version (to allow re-running)."""
    deleted = db.query(BibleText).filter(BibleText.version_id == version_id).delete()
    db.commit()
    return deleted


def deduplicate_verses(verses: list[dict]) -> list[dict]:
    """Remove duplicate verses (keep first occurrence)."""
    seen = set()
    unique = []
    duplicates = 0
    for v in verses:
        key = (v["book_number"], v["chapter"], v["verse"])
        if key not in seen:
            seen.add(key)
            unique.append(v)
        else:
            duplicates += 1
    if duplicates > 0:
        print(f"   Removed {duplicates} duplicate verses")
    return unique


def insert_verses_batch(db: Session, verses: list[dict], version_id: int, batch_size: int = 2000):
    """Insert verses in batches using raw SQL with ON CONFLICT DO NOTHING."""
    # Deduplicate first
    verses = deduplicate_verses(verses)
    total = len(verses)
    inserted = 0
    
    for i in range(0, total, batch_size):
        batch = verses[i:i + batch_size]
        
        # Build values for raw SQL insert
        values = []
        params = {}
        for j, v in enumerate(batch):
            values.append(f"(:vid{j}, :bn{j}, :bname{j}, :ch{j}, :vs{j}, :txt{j})")
            params[f"vid{j}"] = version_id
            params[f"bn{j}"] = v["book_number"]
            params[f"bname{j}"] = v["book_name"]
            params[f"ch{j}"] = v["chapter"]
            params[f"vs{j}"] = v["verse"]
            params[f"txt{j}"] = v["text"]
        
        sql = f"""
            INSERT INTO bible_texts (version_id, book_number, book_name, chapter, verse, text)
            VALUES {', '.join(values)}
            ON CONFLICT (version_id, book_number, chapter, verse) DO NOTHING
        """
        
        db.execute(text(sql), params)
        db.commit()
        
        inserted += len(batch)
        print(f"    Inserted {inserted}/{total} verses...")
    
    return inserted


def get_verse_count(db: Session, version_id: int) -> int:
    """Get count of verses for a version."""
    return db.query(BibleText).filter(BibleText.version_id == version_id).count()


def main():
    print("=" * 60)
    print("Bible Download and Population Script")
    print("=" * 60)
    
    # Ensure tables exist
    print("\n1. Creating database tables...")
    ensure_tables()
    print("   Tables ready.")
    
    db = SessionLocal()
    try:
        # Create/get versions
        print("\n2. Setting up Bible versions...")
        code_to_id = get_or_create_versions(db)
        for code, vid in code_to_id.items():
            print(f"   {code}: version_id={vid}")
        
        # Download and process each version
        print("\n3. Downloading and importing Bible texts...")
        
        for version_code, url in BIBLE_SOURCES.items():
            print(f"\n--- Processing {version_code} ---")
            
            # Check existing verses
            version_id = code_to_id[version_code]
            existing_count = get_verse_count(db, version_id)
            
            if existing_count > 1000:
                print(f"   {version_code} already has {existing_count} verses. Skipping.")
                print(f"   (Delete existing verses first if you want to re-import)")
                continue
            
            # Clear any partial data
            if existing_count > 0:
                print(f"   Clearing {existing_count} existing verses...")
                clear_existing_verses(db, version_id)
            
            # Download
            data = download_json(url)
            
            # Try alternative source for KJV if main fails
            if data is None and version_code == "KJV":
                print("   Trying alternative KJV source...")
                data = download_json(KJV_ALTERNATIVE)
            
            if data is None:
                print(f"   ERROR: Could not download {version_code}. Skipping.")
                continue
            
            # Parse
            print(f"   Parsing {version_code} data...")
            verses = parse_github_bible(data, version_code)
            print(f"   Found {len(verses)} verses in {version_code}")
            
            if not verses:
                print(f"   WARNING: No verses found for {version_code}")
                continue
            
            # Insert
            print(f"   Inserting {version_code} verses into database...")
            inserted = insert_verses_batch(db, verses, version_id)
            print(f"   SUCCESS: Inserted {inserted} verses for {version_code}")
        
        # Final summary
        print("\n" + "=" * 60)
        print("FINAL SUMMARY")
        print("=" * 60)
        
        total_verses = 0
        for code, version_id in code_to_id.items():
            count = get_verse_count(db, version_id)
            total_verses += count
            print(f"  {code}: {count:,} verses")
        
        print(f"\n  TOTAL: {total_verses:,} verses in database")
        print("=" * 60)
        
    finally:
        db.close()


if __name__ == "__main__":
    main()
