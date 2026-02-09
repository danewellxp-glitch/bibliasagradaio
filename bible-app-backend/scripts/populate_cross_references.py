#!/usr/bin/env python3
"""Seed ~300 real Bible cross-references (TSK-style) for study API."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base, SessionLocal, engine
from app.models.study import CrossReference

# ---------------------------------------------------------------------------
# Book number constants (matching the app's canonical book IDs)
# ---------------------------------------------------------------------------
GEN = 1; EXO = 2; LEV = 3; NUM = 4; DEU = 5; JOS = 6; RUT = 8
SAM1 = 9; SAM2 = 10; KI1 = 11; KI2 = 12
JOB = 18; PSA = 19; PRO = 20; ECC = 21
ISA = 23; JER = 24; EZK = 26; DAN = 27
HOS = 28; JOE = 29; AMO = 30; MIC = 33; ZEC = 38; MAL = 39
MAT = 40; MRK = 41; LUK = 42; JHN = 43; ACT = 44
ROM = 45; CO1 = 46; CO2 = 47; GAL = 48; EPH = 49; PHP = 50
HEB = 58; JAS = 59; PE1 = 60; JO1 = 62; REV = 66

# ---------------------------------------------------------------------------
# ~300 real cross-reference entries organised by major biblical themes
# ---------------------------------------------------------------------------
SEED = [
    # ===================================================================
    # 1. CREATION  (Genesis <-> John, Psalms, Hebrews, Colossians-like)
    # ===================================================================
    # Gen 1:1 - "In the beginning God created..."
    {"from_book": GEN, "from_chapter": 1, "from_verse": 1, "to_book": JHN, "to_chapter": 1, "to_verse": 1, "relationship_type": "parallel"},
    {"from_book": GEN, "from_chapter": 1, "from_verse": 1, "to_book": PSA, "to_chapter": 33, "to_verse": 6, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 1, "from_verse": 1, "to_book": HEB, "to_chapter": 11, "to_verse": 3, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 1, "from_verse": 1, "to_book": ISA, "to_chapter": 40, "to_verse": 28, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 1, "from_verse": 1, "to_book": REV, "to_chapter": 4, "to_verse": 11, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 1, "from_verse": 1, "to_book": PSA, "to_chapter": 102, "to_verse": 25, "relationship_type": "theme"},
    # Gen 1:2 - Spirit over the waters
    {"from_book": GEN, "from_chapter": 1, "from_verse": 2, "to_book": PSA, "to_chapter": 104, "to_verse": 30, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 1, "from_verse": 2, "to_book": JOB, "to_chapter": 26, "to_verse": 13, "relationship_type": "theme"},
    # Gen 1:3 - "Let there be light"
    {"from_book": GEN, "from_chapter": 1, "from_verse": 3, "to_book": CO2, "to_chapter": 4, "to_verse": 6, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 1, "from_verse": 3, "to_book": JHN, "to_chapter": 1, "to_verse": 5, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 1, "from_verse": 3, "to_book": PSA, "to_chapter": 33, "to_verse": 9, "relationship_type": "parallel"},
    # Gen 1:26-27 - Image of God
    {"from_book": GEN, "from_chapter": 1, "from_verse": 26, "to_book": CO1, "to_chapter": 11, "to_verse": 7, "relationship_type": "quotation"},
    {"from_book": GEN, "from_chapter": 1, "from_verse": 27, "to_book": MAT, "to_chapter": 19, "to_verse": 4, "relationship_type": "quotation"},
    {"from_book": GEN, "from_chapter": 1, "from_verse": 27, "to_book": JAS, "to_chapter": 3, "to_verse": 9, "relationship_type": "allusion"},
    # Gen 2:2-3 - Sabbath rest
    {"from_book": GEN, "from_chapter": 2, "from_verse": 2, "to_book": EXO, "to_chapter": 20, "to_verse": 11, "relationship_type": "quotation"},
    {"from_book": GEN, "from_chapter": 2, "from_verse": 2, "to_book": HEB, "to_chapter": 4, "to_verse": 4, "relationship_type": "quotation"},
    # Gen 2:7 - Man from dust
    {"from_book": GEN, "from_chapter": 2, "from_verse": 7, "to_book": CO1, "to_chapter": 15, "to_verse": 45, "relationship_type": "type_antitype"},
    {"from_book": GEN, "from_chapter": 2, "from_verse": 7, "to_book": JOB, "to_chapter": 33, "to_verse": 4, "relationship_type": "theme"},
    # Gen 2:24 - Marriage
    {"from_book": GEN, "from_chapter": 2, "from_verse": 24, "to_book": MAT, "to_chapter": 19, "to_verse": 5, "relationship_type": "quotation"},
    {"from_book": GEN, "from_chapter": 2, "from_verse": 24, "to_book": EPH, "to_chapter": 5, "to_verse": 31, "relationship_type": "quotation"},
    {"from_book": GEN, "from_chapter": 2, "from_verse": 24, "to_book": MRK, "to_chapter": 10, "to_verse": 7, "relationship_type": "quotation"},

    # ===================================================================
    # 2. THE FALL AND REDEMPTION (Gen 3 <-> Romans, Revelation)
    # ===================================================================
    # Gen 3:1 - Serpent
    {"from_book": GEN, "from_chapter": 3, "from_verse": 1, "to_book": REV, "to_chapter": 12, "to_verse": 9, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 3, "from_verse": 1, "to_book": CO2, "to_chapter": 11, "to_verse": 3, "relationship_type": "allusion"},
    # Gen 3:15 - Protoevangelium
    {"from_book": GEN, "from_chapter": 3, "from_verse": 15, "to_book": ROM, "to_chapter": 16, "to_verse": 20, "relationship_type": "prophecy_fulfillment"},
    {"from_book": GEN, "from_chapter": 3, "from_verse": 15, "to_book": GAL, "to_chapter": 4, "to_verse": 4, "relationship_type": "prophecy_fulfillment"},
    {"from_book": GEN, "from_chapter": 3, "from_verse": 15, "to_book": REV, "to_chapter": 12, "to_verse": 17, "relationship_type": "prophecy_fulfillment"},
    # Gen 3:17-19 - Curse on the ground / death
    {"from_book": GEN, "from_chapter": 3, "from_verse": 17, "to_book": ROM, "to_chapter": 8, "to_verse": 20, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 3, "from_verse": 19, "to_book": ROM, "to_chapter": 5, "to_verse": 12, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 3, "from_verse": 19, "to_book": CO1, "to_chapter": 15, "to_verse": 21, "relationship_type": "theme"},

    # ===================================================================
    # 3. ABRAHAM COVENANT / FAITH (Gen 12-22 <-> Rom, Gal, Heb, Jas)
    # ===================================================================
    # Gen 12:1-3 - Call of Abram, blessing
    {"from_book": GEN, "from_chapter": 12, "from_verse": 1, "to_book": ACT, "to_chapter": 7, "to_verse": 3, "relationship_type": "quotation"},
    {"from_book": GEN, "from_chapter": 12, "from_verse": 3, "to_book": GAL, "to_chapter": 3, "to_verse": 8, "relationship_type": "quotation"},
    {"from_book": GEN, "from_chapter": 12, "from_verse": 3, "to_book": ACT, "to_chapter": 3, "to_verse": 25, "relationship_type": "quotation"},
    # Gen 15:6 - Abram believed -> counted as righteousness
    {"from_book": GEN, "from_chapter": 15, "from_verse": 6, "to_book": ROM, "to_chapter": 4, "to_verse": 3, "relationship_type": "quotation"},
    {"from_book": GEN, "from_chapter": 15, "from_verse": 6, "to_book": GAL, "to_chapter": 3, "to_verse": 6, "relationship_type": "quotation"},
    {"from_book": GEN, "from_chapter": 15, "from_verse": 6, "to_book": JAS, "to_chapter": 2, "to_verse": 23, "relationship_type": "quotation"},
    # Gen 22 - Sacrifice of Isaac / type of Christ
    {"from_book": GEN, "from_chapter": 22, "from_verse": 2, "to_book": JHN, "to_chapter": 3, "to_verse": 16, "relationship_type": "type_antitype"},
    {"from_book": GEN, "from_chapter": 22, "from_verse": 8, "to_book": JHN, "to_chapter": 1, "to_verse": 29, "relationship_type": "type_antitype"},
    {"from_book": GEN, "from_chapter": 22, "from_verse": 12, "to_book": HEB, "to_chapter": 11, "to_verse": 17, "relationship_type": "theme"},
    {"from_book": GEN, "from_chapter": 22, "from_verse": 18, "to_book": GAL, "to_chapter": 3, "to_verse": 16, "relationship_type": "prophecy_fulfillment"},
    # Gen 14:18 - Melchizedek
    {"from_book": GEN, "from_chapter": 14, "from_verse": 18, "to_book": HEB, "to_chapter": 7, "to_verse": 1, "relationship_type": "type_antitype"},
    {"from_book": GEN, "from_chapter": 14, "from_verse": 18, "to_book": PSA, "to_chapter": 110, "to_verse": 4, "relationship_type": "theme"},

    # ===================================================================
    # 4. EXODUS / PASSOVER / LAW  (Exo <-> NT)
    # ===================================================================
    # Exo 3:14 - I AM
    {"from_book": EXO, "from_chapter": 3, "from_verse": 14, "to_book": JHN, "to_chapter": 8, "to_verse": 58, "relationship_type": "theme"},
    {"from_book": EXO, "from_chapter": 3, "from_verse": 14, "to_book": REV, "to_chapter": 1, "to_verse": 8, "relationship_type": "theme"},
    # Exo 12 - Passover lamb
    {"from_book": EXO, "from_chapter": 12, "from_verse": 3, "to_book": CO1, "to_chapter": 5, "to_verse": 7, "relationship_type": "type_antitype"},
    {"from_book": EXO, "from_chapter": 12, "from_verse": 5, "to_book": PE1, "to_chapter": 1, "to_verse": 19, "relationship_type": "type_antitype"},
    {"from_book": EXO, "from_chapter": 12, "from_verse": 13, "to_book": ROM, "to_chapter": 3, "to_verse": 25, "relationship_type": "type_antitype"},
    {"from_book": EXO, "from_chapter": 12, "from_verse": 46, "to_book": JHN, "to_chapter": 19, "to_verse": 36, "relationship_type": "prophecy_fulfillment"},
    # Exo 16 - Manna
    {"from_book": EXO, "from_chapter": 16, "from_verse": 4, "to_book": JHN, "to_chapter": 6, "to_verse": 31, "relationship_type": "type_antitype"},
    {"from_book": EXO, "from_chapter": 16, "from_verse": 4, "to_book": REV, "to_chapter": 2, "to_verse": 17, "relationship_type": "allusion"},
    # Exo 17:6 - Rock at Horeb
    {"from_book": EXO, "from_chapter": 17, "from_verse": 6, "to_book": CO1, "to_chapter": 10, "to_verse": 4, "relationship_type": "type_antitype"},
    # Exo 19:5-6 - Kingdom of priests
    {"from_book": EXO, "from_chapter": 19, "from_verse": 6, "to_book": PE1, "to_chapter": 2, "to_verse": 9, "relationship_type": "quotation"},
    {"from_book": EXO, "from_chapter": 19, "from_verse": 6, "to_book": REV, "to_chapter": 1, "to_verse": 6, "relationship_type": "allusion"},
    # Exo 20 - Ten Commandments
    {"from_book": EXO, "from_chapter": 20, "from_verse": 3, "to_book": MAT, "to_chapter": 4, "to_verse": 10, "relationship_type": "theme"},
    {"from_book": EXO, "from_chapter": 20, "from_verse": 12, "to_book": EPH, "to_chapter": 6, "to_verse": 2, "relationship_type": "quotation"},
    {"from_book": EXO, "from_chapter": 20, "from_verse": 13, "to_book": MAT, "to_chapter": 5, "to_verse": 21, "relationship_type": "quotation"},
    {"from_book": EXO, "from_chapter": 20, "from_verse": 14, "to_book": MAT, "to_chapter": 5, "to_verse": 27, "relationship_type": "quotation"},
    {"from_book": EXO, "from_chapter": 20, "from_verse": 17, "to_book": ROM, "to_chapter": 7, "to_verse": 7, "relationship_type": "quotation"},
    # Exo 24:8 - Blood of the covenant
    {"from_book": EXO, "from_chapter": 24, "from_verse": 8, "to_book": HEB, "to_chapter": 9, "to_verse": 20, "relationship_type": "quotation"},
    {"from_book": EXO, "from_chapter": 24, "from_verse": 8, "to_book": MAT, "to_chapter": 26, "to_verse": 28, "relationship_type": "type_antitype"},
    # Exo 25:40 - Pattern for tabernacle
    {"from_book": EXO, "from_chapter": 25, "from_verse": 40, "to_book": HEB, "to_chapter": 8, "to_verse": 5, "relationship_type": "quotation"},
    # Exo 33:20 - Cannot see God's face
    {"from_book": EXO, "from_chapter": 33, "from_verse": 20, "to_book": JHN, "to_chapter": 1, "to_verse": 18, "relationship_type": "contrast"},
    {"from_book": EXO, "from_chapter": 33, "from_verse": 20, "to_book": JO1, "to_chapter": 4, "to_verse": 12, "relationship_type": "theme"},
    # Exo 34:6 - God merciful and gracious
    {"from_book": EXO, "from_chapter": 34, "from_verse": 6, "to_book": PSA, "to_chapter": 103, "to_verse": 8, "relationship_type": "parallel"},
    {"from_book": EXO, "from_chapter": 34, "from_verse": 6, "to_book": JOE, "to_chapter": 2, "to_verse": 13, "relationship_type": "parallel"},

    # ===================================================================
    # 5. LEVITICUS / ATONEMENT / HOLINESS (Lev <-> Hebrews, 1 Peter)
    # ===================================================================
    # Lev 4:35 - Sin offering
    {"from_book": LEV, "from_chapter": 4, "from_verse": 35, "to_book": HEB, "to_chapter": 10, "to_verse": 12, "relationship_type": "type_antitype"},
    # Lev 11:44 - Be holy
    {"from_book": LEV, "from_chapter": 11, "from_verse": 44, "to_book": PE1, "to_chapter": 1, "to_verse": 16, "relationship_type": "quotation"},
    # Lev 16 - Day of Atonement
    {"from_book": LEV, "from_chapter": 16, "from_verse": 15, "to_book": HEB, "to_chapter": 9, "to_verse": 7, "relationship_type": "type_antitype"},
    {"from_book": LEV, "from_chapter": 16, "from_verse": 15, "to_book": HEB, "to_chapter": 9, "to_verse": 12, "relationship_type": "type_antitype"},
    {"from_book": LEV, "from_chapter": 16, "from_verse": 21, "to_book": JHN, "to_chapter": 1, "to_verse": 29, "relationship_type": "type_antitype"},
    # Lev 17:11 - Life is in the blood
    {"from_book": LEV, "from_chapter": 17, "from_verse": 11, "to_book": HEB, "to_chapter": 9, "to_verse": 22, "relationship_type": "theme"},
    {"from_book": LEV, "from_chapter": 17, "from_verse": 11, "to_book": EPH, "to_chapter": 1, "to_verse": 7, "relationship_type": "theme"},
    # Lev 19:2 - Be holy as I am holy
    {"from_book": LEV, "from_chapter": 19, "from_verse": 2, "to_book": PE1, "to_chapter": 1, "to_verse": 15, "relationship_type": "quotation"},
    # Lev 19:18 - Love your neighbor
    {"from_book": LEV, "from_chapter": 19, "from_verse": 18, "to_book": MAT, "to_chapter": 22, "to_verse": 39, "relationship_type": "quotation"},
    {"from_book": LEV, "from_chapter": 19, "from_verse": 18, "to_book": ROM, "to_chapter": 13, "to_verse": 9, "relationship_type": "quotation"},
    {"from_book": LEV, "from_chapter": 19, "from_verse": 18, "to_book": GAL, "to_chapter": 5, "to_verse": 14, "relationship_type": "quotation"},
    {"from_book": LEV, "from_chapter": 19, "from_verse": 18, "to_book": JAS, "to_chapter": 2, "to_verse": 8, "relationship_type": "quotation"},

    # ===================================================================
    # 6. DEUTERONOMY (Deut quoted by Jesus, NT)
    # ===================================================================
    # Deut 6:4-5 - Shema / greatest commandment
    {"from_book": DEU, "from_chapter": 6, "from_verse": 4, "to_book": MRK, "to_chapter": 12, "to_verse": 29, "relationship_type": "quotation"},
    {"from_book": DEU, "from_chapter": 6, "from_verse": 5, "to_book": MAT, "to_chapter": 22, "to_verse": 37, "relationship_type": "quotation"},
    {"from_book": DEU, "from_chapter": 6, "from_verse": 5, "to_book": LUK, "to_chapter": 10, "to_verse": 27, "relationship_type": "quotation"},
    # Deut 6:13 - Worship God only (Jesus' temptation)
    {"from_book": DEU, "from_chapter": 6, "from_verse": 13, "to_book": MAT, "to_chapter": 4, "to_verse": 10, "relationship_type": "quotation"},
    # Deut 6:16 - Do not test the Lord
    {"from_book": DEU, "from_chapter": 6, "from_verse": 16, "to_book": MAT, "to_chapter": 4, "to_verse": 7, "relationship_type": "quotation"},
    # Deut 8:3 - Man does not live by bread alone
    {"from_book": DEU, "from_chapter": 8, "from_verse": 3, "to_book": MAT, "to_chapter": 4, "to_verse": 4, "relationship_type": "quotation"},
    {"from_book": DEU, "from_chapter": 8, "from_verse": 3, "to_book": LUK, "to_chapter": 4, "to_verse": 4, "relationship_type": "quotation"},
    # Deut 18:15 - Prophet like Moses
    {"from_book": DEU, "from_chapter": 18, "from_verse": 15, "to_book": ACT, "to_chapter": 3, "to_verse": 22, "relationship_type": "prophecy_fulfillment"},
    {"from_book": DEU, "from_chapter": 18, "from_verse": 15, "to_book": ACT, "to_chapter": 7, "to_verse": 37, "relationship_type": "prophecy_fulfillment"},
    {"from_book": DEU, "from_chapter": 18, "from_verse": 15, "to_book": JHN, "to_chapter": 6, "to_verse": 14, "relationship_type": "prophecy_fulfillment"},
    # Deut 21:23 - Cursed is everyone hung on a tree
    {"from_book": DEU, "from_chapter": 21, "from_verse": 23, "to_book": GAL, "to_chapter": 3, "to_verse": 13, "relationship_type": "quotation"},
    # Deut 30:12-14 - The word is near you
    {"from_book": DEU, "from_chapter": 30, "from_verse": 14, "to_book": ROM, "to_chapter": 10, "to_verse": 8, "relationship_type": "quotation"},
    # Deut 32:35 - Vengeance is mine
    {"from_book": DEU, "from_chapter": 32, "from_verse": 35, "to_book": ROM, "to_chapter": 12, "to_verse": 19, "relationship_type": "quotation"},
    {"from_book": DEU, "from_chapter": 32, "from_verse": 35, "to_book": HEB, "to_chapter": 10, "to_verse": 30, "relationship_type": "quotation"},

    # ===================================================================
    # 7. MESSIANIC PROPHECIES  (Isaiah <-> Gospels, Acts, Romans)
    # ===================================================================
    # Isa 7:14 - Virgin shall conceive
    {"from_book": ISA, "from_chapter": 7, "from_verse": 14, "to_book": MAT, "to_chapter": 1, "to_verse": 23, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 7, "from_verse": 14, "to_book": LUK, "to_chapter": 1, "to_verse": 31, "relationship_type": "prophecy_fulfillment"},
    # Isa 9:1-2 - Light in Galilee
    {"from_book": ISA, "from_chapter": 9, "from_verse": 1, "to_book": MAT, "to_chapter": 4, "to_verse": 15, "relationship_type": "prophecy_fulfillment"},
    # Isa 9:6 - Wonderful Counselor
    {"from_book": ISA, "from_chapter": 9, "from_verse": 6, "to_book": LUK, "to_chapter": 2, "to_verse": 11, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 9, "from_verse": 6, "to_book": JHN, "to_chapter": 1, "to_verse": 14, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 9, "from_verse": 6, "to_book": EPH, "to_chapter": 2, "to_verse": 14, "relationship_type": "theme"},
    # Isa 11:1-2 - Branch / Spirit of the Lord
    {"from_book": ISA, "from_chapter": 11, "from_verse": 1, "to_book": MAT, "to_chapter": 2, "to_verse": 23, "relationship_type": "allusion"},
    {"from_book": ISA, "from_chapter": 11, "from_verse": 2, "to_book": LUK, "to_chapter": 4, "to_verse": 18, "relationship_type": "theme"},
    # Isa 28:16 - Cornerstone in Zion
    {"from_book": ISA, "from_chapter": 28, "from_verse": 16, "to_book": ROM, "to_chapter": 9, "to_verse": 33, "relationship_type": "quotation"},
    {"from_book": ISA, "from_chapter": 28, "from_verse": 16, "to_book": PE1, "to_chapter": 2, "to_verse": 6, "relationship_type": "quotation"},
    {"from_book": ISA, "from_chapter": 28, "from_verse": 16, "to_book": EPH, "to_chapter": 2, "to_verse": 20, "relationship_type": "allusion"},
    # Isa 40:3 - Voice in the wilderness
    {"from_book": ISA, "from_chapter": 40, "from_verse": 3, "to_book": MAT, "to_chapter": 3, "to_verse": 3, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 40, "from_verse": 3, "to_book": MRK, "to_chapter": 1, "to_verse": 3, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 40, "from_verse": 3, "to_book": LUK, "to_chapter": 3, "to_verse": 4, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 40, "from_verse": 3, "to_book": JHN, "to_chapter": 1, "to_verse": 23, "relationship_type": "prophecy_fulfillment"},
    # Isa 40:8 - Word of God stands forever
    {"from_book": ISA, "from_chapter": 40, "from_verse": 8, "to_book": PE1, "to_chapter": 1, "to_verse": 25, "relationship_type": "quotation"},
    # Isa 42:1-4 - Servant of the Lord
    {"from_book": ISA, "from_chapter": 42, "from_verse": 1, "to_book": MAT, "to_chapter": 12, "to_verse": 18, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 42, "from_verse": 1, "to_book": MAT, "to_chapter": 3, "to_verse": 17, "relationship_type": "prophecy_fulfillment"},
    # Isa 49:6 - Light to the Gentiles
    {"from_book": ISA, "from_chapter": 49, "from_verse": 6, "to_book": ACT, "to_chapter": 13, "to_verse": 47, "relationship_type": "quotation"},
    {"from_book": ISA, "from_chapter": 49, "from_verse": 6, "to_book": LUK, "to_chapter": 2, "to_verse": 32, "relationship_type": "prophecy_fulfillment"},
    # Isa 52:7 - Beautiful feet / good news
    {"from_book": ISA, "from_chapter": 52, "from_verse": 7, "to_book": ROM, "to_chapter": 10, "to_verse": 15, "relationship_type": "quotation"},
    # Isa 53 - Suffering Servant (the core messianic passage)
    {"from_book": ISA, "from_chapter": 53, "from_verse": 1, "to_book": JHN, "to_chapter": 12, "to_verse": 38, "relationship_type": "quotation"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 1, "to_book": ROM, "to_chapter": 10, "to_verse": 16, "relationship_type": "quotation"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 3, "to_book": JHN, "to_chapter": 1, "to_verse": 11, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 4, "to_book": MAT, "to_chapter": 8, "to_verse": 17, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 5, "to_book": PE1, "to_chapter": 2, "to_verse": 24, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 5, "to_book": ROM, "to_chapter": 4, "to_verse": 25, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 6, "to_book": PE1, "to_chapter": 2, "to_verse": 25, "relationship_type": "allusion"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 7, "to_book": ACT, "to_chapter": 8, "to_verse": 32, "relationship_type": "quotation"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 7, "to_book": JHN, "to_chapter": 1, "to_verse": 29, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 9, "to_book": PE1, "to_chapter": 2, "to_verse": 22, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 12, "to_book": LUK, "to_chapter": 22, "to_verse": 37, "relationship_type": "quotation"},
    {"from_book": ISA, "from_chapter": 53, "from_verse": 12, "to_book": MRK, "to_chapter": 15, "to_verse": 28, "relationship_type": "prophecy_fulfillment"},
    # Isa 55:3 - Everlasting covenant / David
    {"from_book": ISA, "from_chapter": 55, "from_verse": 3, "to_book": ACT, "to_chapter": 13, "to_verse": 34, "relationship_type": "quotation"},
    # Isa 59:20 - Redeemer from Zion
    {"from_book": ISA, "from_chapter": 59, "from_verse": 20, "to_book": ROM, "to_chapter": 11, "to_verse": 26, "relationship_type": "quotation"},
    # Isa 61:1-2 - Spirit of the Lord upon me
    {"from_book": ISA, "from_chapter": 61, "from_verse": 1, "to_book": LUK, "to_chapter": 4, "to_verse": 18, "relationship_type": "quotation"},
    {"from_book": ISA, "from_chapter": 61, "from_verse": 1, "to_book": MAT, "to_chapter": 11, "to_verse": 5, "relationship_type": "allusion"},

    # ===================================================================
    # 8. JEREMIAH / NEW COVENANT (Jer <-> Hebrews, Luke)
    # ===================================================================
    # Jer 31:15 - Rachel weeping
    {"from_book": JER, "from_chapter": 31, "from_verse": 15, "to_book": MAT, "to_chapter": 2, "to_verse": 18, "relationship_type": "prophecy_fulfillment"},
    # Jer 31:31-34 - New covenant
    {"from_book": JER, "from_chapter": 31, "from_verse": 31, "to_book": HEB, "to_chapter": 8, "to_verse": 8, "relationship_type": "quotation"},
    {"from_book": JER, "from_chapter": 31, "from_verse": 33, "to_book": HEB, "to_chapter": 10, "to_verse": 16, "relationship_type": "quotation"},
    {"from_book": JER, "from_chapter": 31, "from_verse": 31, "to_book": LUK, "to_chapter": 22, "to_verse": 20, "relationship_type": "prophecy_fulfillment"},
    {"from_book": JER, "from_chapter": 31, "from_verse": 34, "to_book": HEB, "to_chapter": 8, "to_verse": 12, "relationship_type": "quotation"},

    # ===================================================================
    # 9. EZEKIEL (Ezk <-> Revelation, John)
    # ===================================================================
    # Ezk 34 - God as Shepherd
    {"from_book": EZK, "from_chapter": 34, "from_verse": 11, "to_book": JHN, "to_chapter": 10, "to_verse": 11, "relationship_type": "prophecy_fulfillment"},
    {"from_book": EZK, "from_chapter": 34, "from_verse": 23, "to_book": JHN, "to_chapter": 10, "to_verse": 16, "relationship_type": "prophecy_fulfillment"},
    # Ezk 36:25-27 - New heart, new spirit
    {"from_book": EZK, "from_chapter": 36, "from_verse": 26, "to_book": JHN, "to_chapter": 3, "to_verse": 5, "relationship_type": "theme"},
    {"from_book": EZK, "from_chapter": 36, "from_verse": 27, "to_book": ROM, "to_chapter": 8, "to_verse": 4, "relationship_type": "theme"},
    # Ezk 37 - Valley of dry bones / resurrection
    {"from_book": EZK, "from_chapter": 37, "from_verse": 5, "to_book": ROM, "to_chapter": 8, "to_verse": 11, "relationship_type": "theme"},
    {"from_book": EZK, "from_chapter": 37, "from_verse": 27, "to_book": REV, "to_chapter": 21, "to_verse": 3, "relationship_type": "prophecy_fulfillment"},
    # Ezk 47 - River from the temple
    {"from_book": EZK, "from_chapter": 47, "from_verse": 1, "to_book": REV, "to_chapter": 22, "to_verse": 1, "relationship_type": "parallel"},

    # ===================================================================
    # 10. DANIEL <-> REVELATION (Apocalyptic)
    # ===================================================================
    # Dan 2:34-35 - Stone cut without hands
    {"from_book": DAN, "from_chapter": 2, "from_verse": 34, "to_book": LUK, "to_chapter": 20, "to_verse": 18, "relationship_type": "allusion"},
    # Dan 2:44 - Kingdom that will never be destroyed
    {"from_book": DAN, "from_chapter": 2, "from_verse": 44, "to_book": REV, "to_chapter": 11, "to_verse": 15, "relationship_type": "theme"},
    {"from_book": DAN, "from_chapter": 2, "from_verse": 44, "to_book": LUK, "to_chapter": 1, "to_verse": 33, "relationship_type": "prophecy_fulfillment"},
    # Dan 7:9 - Ancient of Days
    {"from_book": DAN, "from_chapter": 7, "from_verse": 9, "to_book": REV, "to_chapter": 1, "to_verse": 14, "relationship_type": "parallel"},
    # Dan 7:13-14 - Son of Man coming on clouds
    {"from_book": DAN, "from_chapter": 7, "from_verse": 13, "to_book": MAT, "to_chapter": 24, "to_verse": 30, "relationship_type": "prophecy_fulfillment"},
    {"from_book": DAN, "from_chapter": 7, "from_verse": 13, "to_book": MAT, "to_chapter": 26, "to_verse": 64, "relationship_type": "quotation"},
    {"from_book": DAN, "from_chapter": 7, "from_verse": 13, "to_book": MRK, "to_chapter": 14, "to_verse": 62, "relationship_type": "quotation"},
    {"from_book": DAN, "from_chapter": 7, "from_verse": 13, "to_book": REV, "to_chapter": 1, "to_verse": 7, "relationship_type": "prophecy_fulfillment"},
    {"from_book": DAN, "from_chapter": 7, "from_verse": 13, "to_book": REV, "to_chapter": 14, "to_verse": 14, "relationship_type": "allusion"},
    {"from_book": DAN, "from_chapter": 7, "from_verse": 14, "to_book": PHP, "to_chapter": 2, "to_verse": 10, "relationship_type": "theme"},
    # Dan 9:27 - Abomination of desolation
    {"from_book": DAN, "from_chapter": 9, "from_verse": 27, "to_book": MAT, "to_chapter": 24, "to_verse": 15, "relationship_type": "quotation"},
    {"from_book": DAN, "from_chapter": 9, "from_verse": 27, "to_book": MRK, "to_chapter": 13, "to_verse": 14, "relationship_type": "quotation"},
    # Dan 10:5-6 - Glorious figure
    {"from_book": DAN, "from_chapter": 10, "from_verse": 6, "to_book": REV, "to_chapter": 1, "to_verse": 15, "relationship_type": "parallel"},
    # Dan 12:1 - Time of distress / Michael
    {"from_book": DAN, "from_chapter": 12, "from_verse": 1, "to_book": MAT, "to_chapter": 24, "to_verse": 21, "relationship_type": "parallel"},
    {"from_book": DAN, "from_chapter": 12, "from_verse": 1, "to_book": REV, "to_chapter": 12, "to_verse": 7, "relationship_type": "parallel"},
    # Dan 12:2 - Resurrection
    {"from_book": DAN, "from_chapter": 12, "from_verse": 2, "to_book": JHN, "to_chapter": 5, "to_verse": 29, "relationship_type": "theme"},
    {"from_book": DAN, "from_chapter": 12, "from_verse": 2, "to_book": ACT, "to_chapter": 24, "to_verse": 15, "relationship_type": "theme"},

    # ===================================================================
    # 11. PSALMS QUOTED IN NT
    # ===================================================================
    # Psa 2:1-2 - Nations rage against the Lord's Anointed
    {"from_book": PSA, "from_chapter": 2, "from_verse": 1, "to_book": ACT, "to_chapter": 4, "to_verse": 25, "relationship_type": "quotation"},
    # Psa 2:7 - You are my Son
    {"from_book": PSA, "from_chapter": 2, "from_verse": 7, "to_book": ACT, "to_chapter": 13, "to_verse": 33, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 2, "from_verse": 7, "to_book": HEB, "to_chapter": 1, "to_verse": 5, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 2, "from_verse": 7, "to_book": HEB, "to_chapter": 5, "to_verse": 5, "relationship_type": "quotation"},
    # Psa 8:2 - Out of the mouths of babes
    {"from_book": PSA, "from_chapter": 8, "from_verse": 2, "to_book": MAT, "to_chapter": 21, "to_verse": 16, "relationship_type": "quotation"},
    # Psa 8:4-6 - What is man / crowned with glory
    {"from_book": PSA, "from_chapter": 8, "from_verse": 4, "to_book": HEB, "to_chapter": 2, "to_verse": 6, "relationship_type": "quotation"},
    # Psa 16:8-11 - Not abandon to Sheol
    {"from_book": PSA, "from_chapter": 16, "from_verse": 10, "to_book": ACT, "to_chapter": 2, "to_verse": 27, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 16, "from_verse": 10, "to_book": ACT, "to_chapter": 13, "to_verse": 35, "relationship_type": "quotation"},
    # Psa 22 - My God, my God, why have you forsaken me?
    {"from_book": PSA, "from_chapter": 22, "from_verse": 1, "to_book": MAT, "to_chapter": 27, "to_verse": 46, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 22, "from_verse": 1, "to_book": MRK, "to_chapter": 15, "to_verse": 34, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 22, "from_verse": 7, "to_book": MAT, "to_chapter": 27, "to_verse": 39, "relationship_type": "prophecy_fulfillment"},
    {"from_book": PSA, "from_chapter": 22, "from_verse": 8, "to_book": MAT, "to_chapter": 27, "to_verse": 43, "relationship_type": "prophecy_fulfillment"},
    {"from_book": PSA, "from_chapter": 22, "from_verse": 16, "to_book": JHN, "to_chapter": 20, "to_verse": 25, "relationship_type": "prophecy_fulfillment"},
    {"from_book": PSA, "from_chapter": 22, "from_verse": 18, "to_book": JHN, "to_chapter": 19, "to_verse": 24, "relationship_type": "prophecy_fulfillment"},
    {"from_book": PSA, "from_chapter": 22, "from_verse": 18, "to_book": MAT, "to_chapter": 27, "to_verse": 35, "relationship_type": "prophecy_fulfillment"},
    # Psa 23 - The Lord is my shepherd
    {"from_book": PSA, "from_chapter": 23, "from_verse": 1, "to_book": JHN, "to_chapter": 10, "to_verse": 11, "relationship_type": "type_antitype"},
    {"from_book": PSA, "from_chapter": 23, "from_verse": 1, "to_book": REV, "to_chapter": 7, "to_verse": 17, "relationship_type": "allusion"},
    # Psa 31:5 - Into your hands I commit my spirit
    {"from_book": PSA, "from_chapter": 31, "from_verse": 5, "to_book": LUK, "to_chapter": 23, "to_verse": 46, "relationship_type": "quotation"},
    # Psa 34:20 - Not a bone broken
    {"from_book": PSA, "from_chapter": 34, "from_verse": 20, "to_book": JHN, "to_chapter": 19, "to_verse": 36, "relationship_type": "prophecy_fulfillment"},
    # Psa 40:6-8 - Sacrifice you did not desire
    {"from_book": PSA, "from_chapter": 40, "from_verse": 6, "to_book": HEB, "to_chapter": 10, "to_verse": 5, "relationship_type": "quotation"},
    # Psa 41:9 - Betrayal by a friend
    {"from_book": PSA, "from_chapter": 41, "from_verse": 9, "to_book": JHN, "to_chapter": 13, "to_verse": 18, "relationship_type": "prophecy_fulfillment"},
    # Psa 45:6-7 - Throne of God forever
    {"from_book": PSA, "from_chapter": 45, "from_verse": 6, "to_book": HEB, "to_chapter": 1, "to_verse": 8, "relationship_type": "quotation"},
    # Psa 51:4 - Against you only have I sinned
    {"from_book": PSA, "from_chapter": 51, "from_verse": 4, "to_book": ROM, "to_chapter": 3, "to_verse": 4, "relationship_type": "quotation"},
    # Psa 68:18 - Ascended on high
    {"from_book": PSA, "from_chapter": 68, "from_verse": 18, "to_book": EPH, "to_chapter": 4, "to_verse": 8, "relationship_type": "quotation"},
    # Psa 69:9 - Zeal for your house
    {"from_book": PSA, "from_chapter": 69, "from_verse": 9, "to_book": JHN, "to_chapter": 2, "to_verse": 17, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 69, "from_verse": 9, "to_book": ROM, "to_chapter": 15, "to_verse": 3, "relationship_type": "quotation"},
    # Psa 69:21 - Gave me vinegar
    {"from_book": PSA, "from_chapter": 69, "from_verse": 21, "to_book": MAT, "to_chapter": 27, "to_verse": 48, "relationship_type": "prophecy_fulfillment"},
    {"from_book": PSA, "from_chapter": 69, "from_verse": 21, "to_book": JHN, "to_chapter": 19, "to_verse": 29, "relationship_type": "prophecy_fulfillment"},
    # Psa 69:25 & 109:8 - Judas' replacement
    {"from_book": PSA, "from_chapter": 69, "from_verse": 25, "to_book": ACT, "to_chapter": 1, "to_verse": 20, "relationship_type": "quotation"},
    # Psa 78:2 - Open my mouth in parables
    {"from_book": PSA, "from_chapter": 78, "from_verse": 2, "to_book": MAT, "to_chapter": 13, "to_verse": 35, "relationship_type": "prophecy_fulfillment"},
    # Psa 91:11-12 - Angels will guard you (temptation)
    {"from_book": PSA, "from_chapter": 91, "from_verse": 11, "to_book": MAT, "to_chapter": 4, "to_verse": 6, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 91, "from_verse": 11, "to_book": LUK, "to_chapter": 4, "to_verse": 10, "relationship_type": "quotation"},
    # Psa 95:7-11 - Do not harden your hearts
    {"from_book": PSA, "from_chapter": 95, "from_verse": 7, "to_book": HEB, "to_chapter": 3, "to_verse": 7, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 95, "from_verse": 11, "to_book": HEB, "to_chapter": 4, "to_verse": 3, "relationship_type": "quotation"},
    # Psa 102:25-27 - Heavens perish, you remain
    {"from_book": PSA, "from_chapter": 102, "from_verse": 25, "to_book": HEB, "to_chapter": 1, "to_verse": 10, "relationship_type": "quotation"},
    # Psa 110:1 - Sit at my right hand (most quoted OT verse in NT)
    {"from_book": PSA, "from_chapter": 110, "from_verse": 1, "to_book": MAT, "to_chapter": 22, "to_verse": 44, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 110, "from_verse": 1, "to_book": MRK, "to_chapter": 12, "to_verse": 36, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 110, "from_verse": 1, "to_book": ACT, "to_chapter": 2, "to_verse": 34, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 110, "from_verse": 1, "to_book": HEB, "to_chapter": 1, "to_verse": 13, "relationship_type": "quotation"},
    # Psa 110:4 - Priest forever after Melchizedek
    {"from_book": PSA, "from_chapter": 110, "from_verse": 4, "to_book": HEB, "to_chapter": 5, "to_verse": 6, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 110, "from_verse": 4, "to_book": HEB, "to_chapter": 7, "to_verse": 17, "relationship_type": "quotation"},
    # Psa 118:22-23 - Stone the builders rejected
    {"from_book": PSA, "from_chapter": 118, "from_verse": 22, "to_book": MAT, "to_chapter": 21, "to_verse": 42, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 118, "from_verse": 22, "to_book": ACT, "to_chapter": 4, "to_verse": 11, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 118, "from_verse": 22, "to_book": PE1, "to_chapter": 2, "to_verse": 7, "relationship_type": "quotation"},
    # Psa 118:26 - Blessed is he who comes in the name of the Lord
    {"from_book": PSA, "from_chapter": 118, "from_verse": 26, "to_book": MAT, "to_chapter": 21, "to_verse": 9, "relationship_type": "quotation"},
    {"from_book": PSA, "from_chapter": 118, "from_verse": 26, "to_book": MAT, "to_chapter": 23, "to_verse": 39, "relationship_type": "quotation"},

    # ===================================================================
    # 12. PROVERBS <-> JAMES (Wisdom literature)
    # ===================================================================
    # Pro 1:7 - Fear of the Lord
    {"from_book": PRO, "from_chapter": 1, "from_verse": 7, "to_book": JAS, "to_chapter": 1, "to_verse": 5, "relationship_type": "theme"},
    {"from_book": PRO, "from_chapter": 1, "from_verse": 7, "to_book": PSA, "to_chapter": 111, "to_verse": 10, "relationship_type": "parallel"},
    # Pro 3:5-6 - Trust in the Lord
    {"from_book": PRO, "from_chapter": 3, "from_verse": 5, "to_book": JAS, "to_chapter": 4, "to_verse": 10, "relationship_type": "theme"},
    # Pro 3:11-12 - Lord disciplines those he loves
    {"from_book": PRO, "from_chapter": 3, "from_verse": 11, "to_book": HEB, "to_chapter": 12, "to_verse": 5, "relationship_type": "quotation"},
    {"from_book": PRO, "from_chapter": 3, "from_verse": 12, "to_book": REV, "to_chapter": 3, "to_verse": 19, "relationship_type": "allusion"},
    # Pro 3:34 - God opposes the proud, gives grace to the humble
    {"from_book": PRO, "from_chapter": 3, "from_verse": 34, "to_book": JAS, "to_chapter": 4, "to_verse": 6, "relationship_type": "quotation"},
    {"from_book": PRO, "from_chapter": 3, "from_verse": 34, "to_book": PE1, "to_chapter": 5, "to_verse": 5, "relationship_type": "quotation"},
    # Pro 4:23 - Guard your heart
    {"from_book": PRO, "from_chapter": 4, "from_verse": 23, "to_book": MAT, "to_chapter": 15, "to_verse": 18, "relationship_type": "theme"},
    # Pro 10:12 - Love covers all transgressions
    {"from_book": PRO, "from_chapter": 10, "from_verse": 12, "to_book": PE1, "to_chapter": 4, "to_verse": 8, "relationship_type": "allusion"},
    # Pro 11:31 - If the righteous are barely saved
    {"from_book": PRO, "from_chapter": 11, "from_verse": 31, "to_book": PE1, "to_chapter": 4, "to_verse": 18, "relationship_type": "quotation"},
    # Pro 15:1 - A gentle answer turns away wrath
    {"from_book": PRO, "from_chapter": 15, "from_verse": 1, "to_book": JAS, "to_chapter": 1, "to_verse": 19, "relationship_type": "theme"},
    # Pro 16:18 - Pride before a fall
    {"from_book": PRO, "from_chapter": 16, "from_verse": 18, "to_book": JAS, "to_chapter": 4, "to_verse": 6, "relationship_type": "theme"},
    # Pro 17:3 - Refining of the heart
    {"from_book": PRO, "from_chapter": 17, "from_verse": 3, "to_book": PE1, "to_chapter": 1, "to_verse": 7, "relationship_type": "theme"},
    # Pro 25:21-22 - Feed your enemy
    {"from_book": PRO, "from_chapter": 25, "from_verse": 21, "to_book": ROM, "to_chapter": 12, "to_verse": 20, "relationship_type": "quotation"},
    # Pro 26:11 - Dog returns to vomit
    {"from_book": PRO, "from_chapter": 26, "from_verse": 11, "to_book": PE1, "to_chapter": 2, "to_verse": 22, "relationship_type": "quotation"},
    # Pro 27:1 - Do not boast about tomorrow
    {"from_book": PRO, "from_chapter": 27, "from_verse": 1, "to_book": JAS, "to_chapter": 4, "to_verse": 13, "relationship_type": "theme"},

    # ===================================================================
    # 13. HOSEA, JOEL, AMOS, MICAH, ZECHARIAH, MALACHI -> NT
    # ===================================================================
    # Hos 1:10 - Not my people -> my people
    {"from_book": HOS, "from_chapter": 1, "from_verse": 10, "to_book": ROM, "to_chapter": 9, "to_verse": 26, "relationship_type": "quotation"},
    # Hos 2:23 - I will say "You are my people"
    {"from_book": HOS, "from_chapter": 2, "from_verse": 23, "to_book": PE1, "to_chapter": 2, "to_verse": 10, "relationship_type": "allusion"},
    # Hos 6:6 - I desire mercy not sacrifice
    {"from_book": HOS, "from_chapter": 6, "from_verse": 6, "to_book": MAT, "to_chapter": 9, "to_verse": 13, "relationship_type": "quotation"},
    {"from_book": HOS, "from_chapter": 6, "from_verse": 6, "to_book": MAT, "to_chapter": 12, "to_verse": 7, "relationship_type": "quotation"},
    # Hos 11:1 - Out of Egypt I called my son
    {"from_book": HOS, "from_chapter": 11, "from_verse": 1, "to_book": MAT, "to_chapter": 2, "to_verse": 15, "relationship_type": "prophecy_fulfillment"},
    # Hos 13:14 - Death where is your sting
    {"from_book": HOS, "from_chapter": 13, "from_verse": 14, "to_book": CO1, "to_chapter": 15, "to_verse": 55, "relationship_type": "quotation"},
    # Joel 2:28-32 - Pour out my Spirit
    {"from_book": JOE, "from_chapter": 2, "from_verse": 28, "to_book": ACT, "to_chapter": 2, "to_verse": 17, "relationship_type": "prophecy_fulfillment"},
    {"from_book": JOE, "from_chapter": 2, "from_verse": 32, "to_book": ROM, "to_chapter": 10, "to_verse": 13, "relationship_type": "quotation"},
    {"from_book": JOE, "from_chapter": 2, "from_verse": 32, "to_book": ACT, "to_chapter": 2, "to_verse": 21, "relationship_type": "quotation"},
    # Amos 5:25-27 - Tent of Molek (Stephen's speech)
    {"from_book": AMO, "from_chapter": 5, "from_verse": 25, "to_book": ACT, "to_chapter": 7, "to_verse": 42, "relationship_type": "quotation"},
    # Amos 9:11-12 - Rebuild David's fallen tent
    {"from_book": AMO, "from_chapter": 9, "from_verse": 11, "to_book": ACT, "to_chapter": 15, "to_verse": 16, "relationship_type": "quotation"},
    # Mic 5:2 - Bethlehem
    {"from_book": MIC, "from_chapter": 5, "from_verse": 2, "to_book": MAT, "to_chapter": 2, "to_verse": 6, "relationship_type": "prophecy_fulfillment"},
    {"from_book": MIC, "from_chapter": 5, "from_verse": 2, "to_book": JHN, "to_chapter": 7, "to_verse": 42, "relationship_type": "allusion"},
    # Mic 6:8 - Do justice, love mercy
    {"from_book": MIC, "from_chapter": 6, "from_verse": 8, "to_book": MAT, "to_chapter": 23, "to_verse": 23, "relationship_type": "allusion"},
    # Zec 9:9 - King riding on a donkey
    {"from_book": ZEC, "from_chapter": 9, "from_verse": 9, "to_book": MAT, "to_chapter": 21, "to_verse": 5, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ZEC, "from_chapter": 9, "from_verse": 9, "to_book": JHN, "to_chapter": 12, "to_verse": 15, "relationship_type": "prophecy_fulfillment"},
    # Zec 11:12-13 - Thirty pieces of silver
    {"from_book": ZEC, "from_chapter": 11, "from_verse": 12, "to_book": MAT, "to_chapter": 26, "to_verse": 15, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ZEC, "from_chapter": 11, "from_verse": 13, "to_book": MAT, "to_chapter": 27, "to_verse": 9, "relationship_type": "prophecy_fulfillment"},
    # Zec 12:10 - Look on him whom they have pierced
    {"from_book": ZEC, "from_chapter": 12, "from_verse": 10, "to_book": JHN, "to_chapter": 19, "to_verse": 37, "relationship_type": "prophecy_fulfillment"},
    {"from_book": ZEC, "from_chapter": 12, "from_verse": 10, "to_book": REV, "to_chapter": 1, "to_verse": 7, "relationship_type": "prophecy_fulfillment"},
    # Zec 13:7 - Strike the shepherd
    {"from_book": ZEC, "from_chapter": 13, "from_verse": 7, "to_book": MAT, "to_chapter": 26, "to_verse": 31, "relationship_type": "quotation"},
    {"from_book": ZEC, "from_chapter": 13, "from_verse": 7, "to_book": MRK, "to_chapter": 14, "to_verse": 27, "relationship_type": "quotation"},
    # Mal 3:1 - Messenger who prepares the way
    {"from_book": MAL, "from_chapter": 3, "from_verse": 1, "to_book": MAT, "to_chapter": 11, "to_verse": 10, "relationship_type": "prophecy_fulfillment"},
    {"from_book": MAL, "from_chapter": 3, "from_verse": 1, "to_book": MRK, "to_chapter": 1, "to_verse": 2, "relationship_type": "prophecy_fulfillment"},
    {"from_book": MAL, "from_chapter": 3, "from_verse": 1, "to_book": LUK, "to_chapter": 7, "to_verse": 27, "relationship_type": "prophecy_fulfillment"},
    # Mal 4:5 - Elijah before the great day
    {"from_book": MAL, "from_chapter": 4, "from_verse": 5, "to_book": MAT, "to_chapter": 11, "to_verse": 14, "relationship_type": "prophecy_fulfillment"},
    {"from_book": MAL, "from_chapter": 4, "from_verse": 5, "to_book": MAT, "to_chapter": 17, "to_verse": 12, "relationship_type": "prophecy_fulfillment"},
    {"from_book": MAL, "from_chapter": 4, "from_verse": 5, "to_book": LUK, "to_chapter": 1, "to_verse": 17, "relationship_type": "prophecy_fulfillment"},

    # ===================================================================
    # 14. JOHN'S GOSPEL - "I AM" statements & OT roots
    # ===================================================================
    # John 1:1 - In the beginning was the Word
    {"from_book": JHN, "from_chapter": 1, "from_verse": 1, "to_book": GEN, "to_chapter": 1, "to_verse": 1, "relationship_type": "parallel"},
    {"from_book": JHN, "from_chapter": 1, "from_verse": 1, "to_book": JO1, "to_chapter": 1, "to_verse": 1, "relationship_type": "parallel"},
    {"from_book": JHN, "from_chapter": 1, "from_verse": 1, "to_book": REV, "to_chapter": 19, "to_verse": 13, "relationship_type": "theme"},
    # John 1:14 - Word became flesh
    {"from_book": JHN, "from_chapter": 1, "from_verse": 14, "to_book": PHP, "to_chapter": 2, "to_verse": 7, "relationship_type": "parallel"},
    # John 1:29 - Lamb of God
    {"from_book": JHN, "from_chapter": 1, "from_verse": 29, "to_book": ISA, "to_chapter": 53, "to_verse": 7, "relationship_type": "prophecy_fulfillment"},
    {"from_book": JHN, "from_chapter": 1, "from_verse": 29, "to_book": REV, "to_chapter": 5, "to_verse": 6, "relationship_type": "theme"},
    # John 3:14 - As Moses lifted the serpent
    {"from_book": JHN, "from_chapter": 3, "from_verse": 14, "to_book": NUM, "to_chapter": 21, "to_verse": 9, "relationship_type": "type_antitype"},
    # John 3:16 - God so loved the world
    {"from_book": JHN, "from_chapter": 3, "from_verse": 16, "to_book": ROM, "to_chapter": 5, "to_verse": 8, "relationship_type": "parallel"},
    {"from_book": JHN, "from_chapter": 3, "from_verse": 16, "to_book": JO1, "to_chapter": 4, "to_verse": 9, "relationship_type": "parallel"},
    # John 6:35 - I am the bread of life
    {"from_book": JHN, "from_chapter": 6, "from_verse": 35, "to_book": EXO, "to_chapter": 16, "to_verse": 15, "relationship_type": "type_antitype"},
    # John 8:12 - I am the light of the world
    {"from_book": JHN, "from_chapter": 8, "from_verse": 12, "to_book": ISA, "to_chapter": 9, "to_verse": 2, "relationship_type": "prophecy_fulfillment"},
    # John 10:11 - I am the good shepherd
    {"from_book": JHN, "from_chapter": 10, "from_verse": 11, "to_book": PSA, "to_chapter": 23, "to_verse": 1, "relationship_type": "type_antitype"},
    {"from_book": JHN, "from_chapter": 10, "from_verse": 11, "to_book": EZK, "to_chapter": 34, "to_verse": 23, "relationship_type": "prophecy_fulfillment"},
    # John 11:25 - I am the resurrection
    {"from_book": JHN, "from_chapter": 11, "from_verse": 25, "to_book": CO1, "to_chapter": 15, "to_verse": 20, "relationship_type": "theme"},
    # John 14:6 - I am the way, truth, life
    {"from_book": JHN, "from_chapter": 14, "from_verse": 6, "to_book": ACT, "to_chapter": 4, "to_verse": 12, "relationship_type": "parallel"},
    {"from_book": JHN, "from_chapter": 14, "from_verse": 6, "to_book": HEB, "to_chapter": 10, "to_verse": 20, "relationship_type": "theme"},
    # John 15:1 - I am the true vine
    {"from_book": JHN, "from_chapter": 15, "from_verse": 1, "to_book": ISA, "to_chapter": 5, "to_verse": 1, "relationship_type": "contrast"},

    # ===================================================================
    # 15. ROMANS - Law and Grace theology
    # ===================================================================
    # Rom 1:17 - The righteous shall live by faith (Hab 2:4)
    {"from_book": ROM, "from_chapter": 1, "from_verse": 17, "to_book": GAL, "to_chapter": 3, "to_verse": 11, "relationship_type": "parallel"},
    {"from_book": ROM, "from_chapter": 1, "from_verse": 17, "to_book": HEB, "to_chapter": 10, "to_verse": 38, "relationship_type": "parallel"},
    # Rom 3:23 - All have sinned
    {"from_book": ROM, "from_chapter": 3, "from_verse": 23, "to_book": GEN, "to_chapter": 3, "to_verse": 19, "relationship_type": "theme"},
    {"from_book": ROM, "from_chapter": 3, "from_verse": 23, "to_book": PSA, "to_chapter": 14, "to_verse": 3, "relationship_type": "quotation"},
    # Rom 5:12 - Sin through Adam
    {"from_book": ROM, "from_chapter": 5, "from_verse": 12, "to_book": GEN, "to_chapter": 3, "to_verse": 6, "relationship_type": "allusion"},
    {"from_book": ROM, "from_chapter": 5, "from_verse": 12, "to_book": CO1, "to_chapter": 15, "to_verse": 22, "relationship_type": "parallel"},
    # Rom 5:19 - Obedience of one
    {"from_book": ROM, "from_chapter": 5, "from_verse": 19, "to_book": PHP, "to_chapter": 2, "to_verse": 8, "relationship_type": "theme"},
    # Rom 6:23 - Wages of sin is death
    {"from_book": ROM, "from_chapter": 6, "from_verse": 23, "to_book": GEN, "to_chapter": 2, "to_verse": 17, "relationship_type": "theme"},
    # Rom 8:28 - All things work together
    {"from_book": ROM, "from_chapter": 8, "from_verse": 28, "to_book": GEN, "to_chapter": 50, "to_verse": 20, "relationship_type": "theme"},
    # Rom 8:34 - Christ at the right hand
    {"from_book": ROM, "from_chapter": 8, "from_verse": 34, "to_book": PSA, "to_chapter": 110, "to_verse": 1, "relationship_type": "allusion"},
    # Rom 10:9 - Confess with your mouth
    {"from_book": ROM, "from_chapter": 10, "from_verse": 9, "to_book": ACT, "to_chapter": 16, "to_verse": 31, "relationship_type": "parallel"},

    # ===================================================================
    # 16. GALATIANS / EPHESIANS / PHILIPPIANS
    # ===================================================================
    # Gal 2:16 - Justified by faith
    {"from_book": GAL, "from_chapter": 2, "from_verse": 16, "to_book": ROM, "to_chapter": 3, "to_verse": 28, "relationship_type": "parallel"},
    # Gal 3:13 - Christ became a curse for us
    {"from_book": GAL, "from_chapter": 3, "from_verse": 13, "to_book": DEU, "to_chapter": 21, "to_verse": 23, "relationship_type": "quotation"},
    {"from_book": GAL, "from_chapter": 3, "from_verse": 13, "to_book": CO2, "to_chapter": 5, "to_verse": 21, "relationship_type": "parallel"},
    # Gal 5:22-23 - Fruit of the Spirit
    {"from_book": GAL, "from_chapter": 5, "from_verse": 22, "to_book": EPH, "to_chapter": 5, "to_verse": 9, "relationship_type": "parallel"},
    {"from_book": GAL, "from_chapter": 5, "from_verse": 22, "to_book": JHN, "to_chapter": 15, "to_verse": 5, "relationship_type": "theme"},
    # Eph 2:8-9 - By grace through faith
    {"from_book": EPH, "from_chapter": 2, "from_verse": 8, "to_book": ROM, "to_chapter": 3, "to_verse": 24, "relationship_type": "parallel"},
    # Eph 6:10-17 - Armor of God
    {"from_book": EPH, "from_chapter": 6, "from_verse": 14, "to_book": ISA, "to_chapter": 59, "to_verse": 17, "relationship_type": "allusion"},
    # Php 2:6-11 - Christ hymn (kenosis)
    {"from_book": PHP, "from_chapter": 2, "from_verse": 6, "to_book": JHN, "to_chapter": 1, "to_verse": 1, "relationship_type": "theme"},
    {"from_book": PHP, "from_chapter": 2, "from_verse": 7, "to_book": ISA, "to_chapter": 53, "to_verse": 12, "relationship_type": "allusion"},
    {"from_book": PHP, "from_chapter": 2, "from_verse": 10, "to_book": ISA, "to_chapter": 45, "to_verse": 23, "relationship_type": "quotation"},
    {"from_book": PHP, "from_chapter": 2, "from_verse": 10, "to_book": ROM, "to_chapter": 14, "to_verse": 11, "relationship_type": "parallel"},

    # ===================================================================
    # 17. HEBREWS - OT fulfilment / better covenant
    # ===================================================================
    # Heb 1:3 - Radiance of God's glory
    {"from_book": HEB, "from_chapter": 1, "from_verse": 3, "to_book": JHN, "to_chapter": 1, "to_verse": 14, "relationship_type": "parallel"},
    # Heb 4:12 - Word of God is living and active
    {"from_book": HEB, "from_chapter": 4, "from_verse": 12, "to_book": EPH, "to_chapter": 6, "to_verse": 17, "relationship_type": "theme"},
    # Heb 7:25 - He always lives to intercede
    {"from_book": HEB, "from_chapter": 7, "from_verse": 25, "to_book": ROM, "to_chapter": 8, "to_verse": 34, "relationship_type": "parallel"},
    # Heb 9:22 - Without shedding of blood no forgiveness
    {"from_book": HEB, "from_chapter": 9, "from_verse": 22, "to_book": LEV, "to_chapter": 17, "to_verse": 11, "relationship_type": "theme"},
    # Heb 11 - Hall of faith references
    {"from_book": HEB, "from_chapter": 11, "from_verse": 4, "to_book": GEN, "to_chapter": 4, "to_verse": 4, "relationship_type": "allusion"},
    {"from_book": HEB, "from_chapter": 11, "from_verse": 5, "to_book": GEN, "to_chapter": 5, "to_verse": 24, "relationship_type": "allusion"},
    {"from_book": HEB, "from_chapter": 11, "from_verse": 7, "to_book": GEN, "to_chapter": 6, "to_verse": 22, "relationship_type": "allusion"},
    {"from_book": HEB, "from_chapter": 11, "from_verse": 8, "to_book": GEN, "to_chapter": 12, "to_verse": 1, "relationship_type": "allusion"},
    {"from_book": HEB, "from_chapter": 11, "from_verse": 17, "to_book": GEN, "to_chapter": 22, "to_verse": 1, "relationship_type": "allusion"},
    {"from_book": HEB, "from_chapter": 11, "from_verse": 23, "to_book": EXO, "to_chapter": 2, "to_verse": 2, "relationship_type": "allusion"},
    {"from_book": HEB, "from_chapter": 11, "from_verse": 29, "to_book": EXO, "to_chapter": 14, "to_verse": 22, "relationship_type": "allusion"},
    {"from_book": HEB, "from_chapter": 11, "from_verse": 30, "to_book": JOS, "to_chapter": 6, "to_verse": 20, "relationship_type": "allusion"},
    {"from_book": HEB, "from_chapter": 11, "from_verse": 31, "to_book": JOS, "to_chapter": 2, "to_verse": 1, "relationship_type": "allusion"},
    # Heb 12:2 - Author and finisher of faith
    {"from_book": HEB, "from_chapter": 12, "from_verse": 2, "to_book": JHN, "to_chapter": 19, "to_verse": 30, "relationship_type": "allusion"},
    # Heb 13:5 - Never leave you
    {"from_book": HEB, "from_chapter": 13, "from_verse": 5, "to_book": DEU, "to_chapter": 31, "to_verse": 6, "relationship_type": "quotation"},
    {"from_book": HEB, "from_chapter": 13, "from_verse": 5, "to_book": JOS, "to_chapter": 1, "to_verse": 5, "relationship_type": "quotation"},

    # ===================================================================
    # 18. 1 JOHN - Love / Light themes
    # ===================================================================
    {"from_book": JO1, "from_chapter": 1, "from_verse": 5, "to_book": JHN, "to_chapter": 1, "to_verse": 5, "relationship_type": "parallel"},
    {"from_book": JO1, "from_chapter": 2, "from_verse": 2, "to_book": ROM, "to_chapter": 3, "to_verse": 25, "relationship_type": "parallel"},
    {"from_book": JO1, "from_chapter": 3, "from_verse": 2, "to_book": ROM, "to_chapter": 8, "to_verse": 29, "relationship_type": "theme"},
    {"from_book": JO1, "from_chapter": 3, "from_verse": 12, "to_book": GEN, "to_chapter": 4, "to_verse": 8, "relationship_type": "allusion"},
    {"from_book": JO1, "from_chapter": 4, "from_verse": 8, "to_book": JHN, "to_chapter": 3, "to_verse": 16, "relationship_type": "parallel"},
    {"from_book": JO1, "from_chapter": 4, "from_verse": 10, "to_book": ROM, "to_chapter": 5, "to_verse": 8, "relationship_type": "parallel"},

    # ===================================================================
    # 19. REVELATION - Consummation / OT echoes
    # ===================================================================
    # Rev 1:8 - Alpha and Omega
    {"from_book": REV, "from_chapter": 1, "from_verse": 8, "to_book": ISA, "to_chapter": 44, "to_verse": 6, "relationship_type": "theme"},
    # Rev 4:8 - Holy, holy, holy
    {"from_book": REV, "from_chapter": 4, "from_verse": 8, "to_book": ISA, "to_chapter": 6, "to_verse": 3, "relationship_type": "parallel"},
    # Rev 5:5 - Lion of Judah
    {"from_book": REV, "from_chapter": 5, "from_verse": 5, "to_book": GEN, "to_chapter": 49, "to_verse": 9, "relationship_type": "prophecy_fulfillment"},
    # Rev 5:6 - Lamb as though slain
    {"from_book": REV, "from_chapter": 5, "from_verse": 6, "to_book": ISA, "to_chapter": 53, "to_verse": 7, "relationship_type": "allusion"},
    # Rev 7:17 - God will wipe every tear
    {"from_book": REV, "from_chapter": 7, "from_verse": 17, "to_book": ISA, "to_chapter": 25, "to_verse": 8, "relationship_type": "allusion"},
    # Rev 11:15 - Kingdom of the world -> kingdom of our Lord
    {"from_book": REV, "from_chapter": 11, "from_verse": 15, "to_book": DAN, "to_chapter": 2, "to_verse": 44, "relationship_type": "prophecy_fulfillment"},
    # Rev 19:11-16 - Rider on the white horse
    {"from_book": REV, "from_chapter": 19, "from_verse": 15, "to_book": ISA, "to_chapter": 63, "to_verse": 3, "relationship_type": "allusion"},
    {"from_book": REV, "from_chapter": 19, "from_verse": 16, "to_book": DAN, "to_chapter": 7, "to_verse": 14, "relationship_type": "theme"},
    # Rev 20:2 - The ancient serpent
    {"from_book": REV, "from_chapter": 20, "from_verse": 2, "to_book": GEN, "to_chapter": 3, "to_verse": 1, "relationship_type": "theme"},
    # Rev 21:1 - New heaven and new earth
    {"from_book": REV, "from_chapter": 21, "from_verse": 1, "to_book": ISA, "to_chapter": 65, "to_verse": 17, "relationship_type": "prophecy_fulfillment"},
    # Rev 21:3-4 - God dwelling with man
    {"from_book": REV, "from_chapter": 21, "from_verse": 3, "to_book": EZK, "to_chapter": 37, "to_verse": 27, "relationship_type": "prophecy_fulfillment"},
    {"from_book": REV, "from_chapter": 21, "from_verse": 4, "to_book": ISA, "to_chapter": 25, "to_verse": 8, "relationship_type": "prophecy_fulfillment"},
    # Rev 21:23 - No need for sun
    {"from_book": REV, "from_chapter": 21, "from_verse": 23, "to_book": ISA, "to_chapter": 60, "to_verse": 19, "relationship_type": "prophecy_fulfillment"},
    # Rev 22:1-2 - Tree of life / river of life
    {"from_book": REV, "from_chapter": 22, "from_verse": 1, "to_book": EZK, "to_chapter": 47, "to_verse": 1, "relationship_type": "parallel"},
    {"from_book": REV, "from_chapter": 22, "from_verse": 2, "to_book": GEN, "to_chapter": 2, "to_verse": 9, "relationship_type": "theme"},
    {"from_book": REV, "from_chapter": 22, "from_verse": 2, "to_book": EZK, "to_chapter": 47, "to_verse": 12, "relationship_type": "parallel"},
    # Rev 22:13 - Alpha and Omega, the First and the Last
    {"from_book": REV, "from_chapter": 22, "from_verse": 13, "to_book": ISA, "to_chapter": 44, "to_verse": 6, "relationship_type": "parallel"},
    # Rev 22:16 - Root and offspring of David
    {"from_book": REV, "from_chapter": 22, "from_verse": 16, "to_book": ISA, "to_chapter": 11, "to_verse": 1, "relationship_type": "prophecy_fulfillment"},

    # ===================================================================
    # 20. ADDITIONAL CROSS-THEME LINKS (JOB, RUTH, SAMUEL, KINGS, ECC)
    # ===================================================================
    # Job 19:25 - I know my redeemer lives
    {"from_book": JOB, "from_chapter": 19, "from_verse": 25, "to_book": CO1, "to_chapter": 15, "to_verse": 20, "relationship_type": "theme"},
    # Ruth 4:14 - Kinsman redeemer
    {"from_book": RUT, "from_chapter": 4, "from_verse": 14, "to_book": EPH, "to_chapter": 1, "to_verse": 7, "relationship_type": "type_antitype"},
    # 2 Sam 7:12-14 - Davidic covenant
    {"from_book": SAM2, "from_chapter": 7, "from_verse": 12, "to_book": LUK, "to_chapter": 1, "to_verse": 32, "relationship_type": "prophecy_fulfillment"},
    {"from_book": SAM2, "from_chapter": 7, "from_verse": 14, "to_book": HEB, "to_chapter": 1, "to_verse": 5, "relationship_type": "quotation"},
    # 1 Kings 19:18 - 7000 who have not bowed
    {"from_book": KI1, "from_chapter": 19, "from_verse": 18, "to_book": ROM, "to_chapter": 11, "to_verse": 4, "relationship_type": "quotation"},
    # Ecc 12:14 - God will judge every deed
    {"from_book": ECC, "from_chapter": 12, "from_verse": 14, "to_book": ROM, "to_chapter": 2, "to_verse": 16, "relationship_type": "theme"},
    {"from_book": ECC, "from_chapter": 12, "from_verse": 14, "to_book": CO2, "to_chapter": 5, "to_verse": 10, "relationship_type": "theme"},
    # Ecc 3:1 - A time for everything
    {"from_book": ECC, "from_chapter": 3, "from_verse": 1, "to_book": GAL, "to_chapter": 4, "to_verse": 4, "relationship_type": "theme"},
    # 1 Sam 16:7 - God looks at the heart
    {"from_book": SAM1, "from_chapter": 16, "from_verse": 7, "to_book": JAS, "to_chapter": 2, "to_verse": 1, "relationship_type": "theme"},
    # Num 21:9 - Bronze serpent
    {"from_book": NUM, "from_chapter": 21, "from_verse": 9, "to_book": JHN, "to_chapter": 3, "to_verse": 14, "relationship_type": "type_antitype"},
    # Josh 1:5 - I will not leave you
    {"from_book": JOS, "from_chapter": 1, "from_verse": 5, "to_book": HEB, "to_chapter": 13, "to_verse": 5, "relationship_type": "quotation"},
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    inserted = 0
    skipped = 0

    try:
        for i, row in enumerate(SEED):
            # ------ dedup: skip if this exact reference already exists ------
            exists = (
                db.query(CrossReference)
                .filter_by(
                    from_book=row["from_book"],
                    from_chapter=row["from_chapter"],
                    from_verse=row["from_verse"],
                    to_book=row["to_book"],
                    to_chapter=row["to_chapter"],
                    to_verse=row["to_verse"],
                )
                .first()
            )
            if exists:
                skipped += 1
                continue

            db.add(CrossReference(**row))
            inserted += 1

            # ------ batch commit every 50 rows ------
            if inserted % 50 == 0:
                db.commit()
                print(f"  ... committed batch ({inserted} so far)")

        # final commit for remaining rows
        db.commit()
        print(
            f"Done. Inserted {inserted} cross-references "
            f"({skipped} duplicates skipped, {len(SEED)} total in seed)."
        )
    except Exception as exc:
        db.rollback()
        print(f"Error: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
