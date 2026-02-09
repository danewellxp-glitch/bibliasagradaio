"""Populate lexicon_entries and word_occurrences with Strong's Concordance data."""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import Base, SessionLocal, engine
from app.models.study import LexiconEntry, WordOccurrence

# Book number constants
GEN, EXO, LEV, NUM, DEU = 1, 2, 3, 4, 5
JOS, JDG, RUT = 6, 7, 8
SAM1, SAM2, KI1, KI2 = 9, 10, 11, 12
CHR1, CHR2, EZR, NEH, EST = 13, 14, 15, 16, 17
JOB, PSA, PRO, ECC, SNG = 18, 19, 20, 21, 22
ISA, JER, LAM, EZK, DAN = 23, 24, 25, 26, 27
HOS, JOL, AMO, OBA, JNA = 28, 29, 30, 31, 32
MIC, NAH, HAB, ZEP, HAG, ZEC, MAL = 33, 34, 35, 36, 37, 38, 39
MAT, MRK, LUK, JHN, ACT = 40, 41, 42, 43, 44
ROM, CO1, CO2, GAL, EPH = 45, 46, 47, 48, 49
PHP, COL, TH1, TH2 = 50, 51, 52, 53
TI1, TI2, TIT, PHM = 54, 55, 56, 57
HEB, JAS, PE1, PE2 = 58, 59, 60, 61
JO1, JO2, JO3, JDE, REV = 62, 63, 64, 65, 66

# fmt: off
HEBREW_ENTRIES = [
    # (strong_number, original_word, transliteration, pronunciation, basic_meaning, extended_definition, usage_count, first_occurrence, occurrences)
    ("H1", "אָב", "ab", "awb", "pai, father", "Pai, ancestral, chefe de familia. Usado para relacoes familiares e para Deus como Pai.", 1180, "GEN.2.24",
     [(GEN, 2, 24), (GEN, 17, 4), (EXO, 20, 12), (PSA, 68, 5), (ISA, 9, 6)]),
    ("H120", "אָדָם", "adam", "aw-dawm", "homem, humanidade", "Ser humano, humanidade. Usado como nome proprio (Adao) e genericamente para a raca humana.", 552, "GEN.1.26",
     [(GEN, 1, 26), (GEN, 2, 7), (GEN, 5, 2), (PSA, 8, 4), (ECC, 7, 20)]),
    ("H136", "אֲדֹנָי", "Adonai", "ad-o-noy", "Senhor, meu Senhor", "Titulo de respeito e reverencia para Deus. Substituto oral para YHWH na leitura judaica.", 434, "GEN.15.2",
     [(GEN, 15, 2), (EXO, 4, 10), (PSA, 110, 1), (ISA, 6, 1), (DAN, 9, 4)]),
    ("H157", "אָהַב", "ahab", "aw-hab", "amar", "Amar, ter afeto por. Usado tanto para amor humano quanto divino.", 208, "GEN.22.2",
     [(GEN, 22, 2), (DEU, 6, 5), (PSA, 18, 1), (PRO, 8, 17), (HOS, 3, 1)]),
    ("H430", "אֱלֹהִים", "Elohim", "el-o-heem", "Deus, deuses", "Forma plural de El. Nome principal para Deus no AT, indicando majestade e plenitude divina.", 2606, "GEN.1.1",
     [(GEN, 1, 1), (GEN, 1, 26), (EXO, 20, 2), (PSA, 19, 1), (ISA, 45, 5)]),
    ("H410", "אֵל", "El", "ale", "Deus, poderoso", "Deus, o poderoso. Forma singular indicando forca e poder divino.", 242, "GEN.14.18",
     [(GEN, 14, 18), (NUM, 23, 22), (PSA, 22, 1), (ISA, 9, 6), (DAN, 11, 36)]),
    ("H539", "אָמַן", "aman", "aw-man", "crer, confiar", "Acreditar, ter fe, confiar. Raiz de 'amen' e 'emunah' (fidelidade).", 108, "GEN.15.6",
     [(GEN, 15, 6), (EXO, 14, 31), (NUM, 14, 11), (ISA, 7, 9), (HAB, 2, 4)]),
    ("H559", "אָמַר", "amar", "aw-mar", "dizer, falar", "Dizer, declarar, falar. Um dos verbos mais comuns no AT.", 5308, "GEN.1.3",
     [(GEN, 1, 3), (GEN, 3, 1), (EXO, 3, 14), (ISA, 6, 8), (JER, 1, 5)]),
    ("H571", "אֱמֶת", "emet", "eh-meth", "verdade, fidelidade", "Verdade, firmeza, fidelidade. Descreve a natureza confiavel de Deus e Sua palavra.", 127, "GEN.24.27",
     [(GEN, 24, 27), (EXO, 34, 6), (PSA, 25, 5), (PSA, 119, 160), (ZEC, 8, 16)]),
    ("H776", "אֶרֶץ", "erets", "eh-rets", "terra, pais", "Terra, solo, pais, territorio. Usada para a terra fisica e para a Terra Prometida.", 2504, "GEN.1.1",
     [(GEN, 1, 1), (GEN, 12, 1), (EXO, 3, 8), (DEU, 8, 7), (ISA, 65, 17)]),
    ("H1254", "בָּרָא", "bara", "baw-raw", "criar", "Criar do nada, produzir algo novo. Usado exclusivamente para a atividade criadora de Deus.", 54, "GEN.1.1",
     [(GEN, 1, 1), (GEN, 1, 21), (GEN, 1, 27), (ISA, 43, 1), (ISA, 65, 17)]),
    ("H1285", "בְּרִית", "berith", "ber-eeth", "alianca, pacto", "Alianca, pacto, acordo. Conceito central da teologia biblica: alianca entre Deus e o povo.", 284, "GEN.6.18",
     [(GEN, 6, 18), (GEN, 15, 18), (EXO, 19, 5), (DEU, 7, 9), (JER, 31, 31)]),
    ("H1696", "דָּבָר", "dabar", "daw-bar", "falar, palavra", "Falar, declarar; como substantivo: palavra, coisa, assunto.", 1142, "GEN.8.15",
     [(GEN, 8, 15), (EXO, 20, 1), (DEU, 5, 22), (PSA, 33, 6), (ISA, 55, 11)]),
    ("H1697", "דָּבָר", "dabar", "daw-bawr", "palavra, coisa", "Palavra, assunto, coisa. A Palavra de Deus como agente ativo de criacao e revelacao.", 1441, "GEN.11.1",
     [(GEN, 11, 1), (DEU, 8, 3), (PSA, 33, 4), (PSA, 119, 105), (ISA, 40, 8)]),
    ("H1980", "הָלַךְ", "halak", "haw-lak", "andar, caminhar", "Andar, caminhar, ir. Metafora para conduta de vida e seguir a Deus.", 1554, "GEN.2.14",
     [(GEN, 5, 22), (GEN, 6, 9), (DEU, 10, 12), (PSA, 1, 1), (MIC, 6, 8)]),
    ("H2398", "חָטָא", "chata", "khaw-taw", "pecar, errar", "Pecar, errar o alvo, falhar. Conceito central de pecado como desvio do padrao divino.", 238, "GEN.20.6",
     [(GEN, 20, 6), (EXO, 32, 30), (PSA, 51, 4), (ISA, 1, 18), (DAN, 9, 5)]),
    ("H2580", "חֵן", "chen", "khane", "graca, favor", "Graca, favor, benevolencia. Favor imerecido de Deus para com as pessoas.", 69, "GEN.6.8",
     [(GEN, 6, 8), (EXO, 33, 13), (PRO, 3, 34), (PSA, 84, 11), (ZEC, 12, 10)]),
    ("H2617", "חֶסֶד", "chesed", "kheh-sed", "amor leal, misericordia", "Amor leal, bondade, misericordia. Amor fiel de Deus baseado em Sua alianca.", 248, "GEN.19.19",
     [(GEN, 19, 19), (EXO, 34, 6), (PSA, 23, 6), (PSA, 136, 1), (LAM, 3, 22)]),
    ("H3045", "יָדַע", "yada", "yaw-dah", "conhecer, saber", "Conhecer intimamente, experimentar, reconhecer. Inclui conhecimento relacional.", 947, "GEN.3.5",
     [(GEN, 3, 5), (GEN, 4, 1), (EXO, 6, 7), (PSA, 46, 10), (JER, 31, 34)]),
    ("H3068", "יְהוָה", "YHWH", "yah-weh", "SENHOR, Javé", "O nome proprio de Deus revelado a Moises. Significa 'Eu Sou o que Sou'. Nome mais sagrado.", 6519, "GEN.2.4",
     [(GEN, 2, 4), (EXO, 3, 14), (EXO, 6, 3), (PSA, 23, 1), (ISA, 42, 8)]),
    ("H3444", "יְשׁוּעָה", "yeshuah", "yesh-oo-aw", "salvacao", "Salvacao, livramento, vitoria. Raiz do nome Yeshua (Jesus).", 78, "GEN.49.18",
     [(GEN, 49, 18), (EXO, 14, 13), (PSA, 3, 8), (PSA, 27, 1), (ISA, 12, 2)]),
    ("H3467", "יָשַׁע", "yasha", "yaw-shah", "salvar, livrar", "Salvar, resgatar, livrar. Deus como o unico verdadeiro Salvador.", 205, "EXO.14.30",
     [(EXO, 14, 30), (JDG, 2, 16), (PSA, 18, 3), (ISA, 43, 11), (ISA, 45, 22)]),
    ("H3722", "כָּפַר", "kaphar", "kaw-far", "expiar, cobrir", "Expiar, fazer expiacao, cobrir pecado. Base do sistema sacrificial e do Yom Kippur.", 102, "GEN.32.20",
     [(GEN, 32, 20), (LEV, 16, 30), (LEV, 17, 11), (PSA, 65, 3), (DAN, 9, 24)]),
    ("H3820", "לֵב", "leb", "labe", "coracao", "Coracao, mente, interior. Centro da vontade, emocoes e pensamentos do ser humano.", 598, "GEN.6.5",
     [(GEN, 6, 5), (DEU, 6, 5), (PSA, 51, 10), (PRO, 4, 23), (JER, 17, 9)]),
    ("H4428", "מֶלֶךְ", "melek", "meh-lek", "rei", "Rei, governante. Titulo usado para reis humanos e para Deus como Rei soberano.", 2523, "GEN.14.1",
     [(GEN, 14, 18), (SAM1, 8, 5), (PSA, 47, 7), (ISA, 6, 5), (DAN, 2, 37)]),
    ("H4941", "מִשְׁפָּט", "mishpat", "mish-pawt", "justica, juizo", "Justica, julgamento, ordenanca, direito. Padrao divino de justica e retidao.", 421, "GEN.18.19",
     [(GEN, 18, 25), (DEU, 16, 18), (PSA, 89, 14), (ISA, 1, 17), (MIC, 6, 8)]),
    ("H5315", "נֶפֶשׁ", "nephesh", "neh-fesh", "alma, vida, ser", "Alma, ser vivo, pessoa, vida interior. Totalidade do ser humano.", 754, "GEN.1.20",
     [(GEN, 1, 20), (GEN, 2, 7), (DEU, 6, 5), (PSA, 23, 3), (PSA, 42, 1)]),
    ("H5414", "נָתַן", "natan", "naw-than", "dar, conceder", "Dar, conceder, entregar, colocar. Um dos verbos mais versáteis do hebraico.", 2014, "GEN.1.17",
     [(GEN, 1, 17), (GEN, 12, 7), (EXO, 31, 18), (DEU, 30, 19), (ISA, 9, 6)]),
    ("H5545", "סָלַח", "salach", "saw-lakh", "perdoar", "Perdoar, absolver. Usado exclusivamente para o perdao divino.", 46, "EXO.34.9",
     [(EXO, 34, 9), (NUM, 14, 19), (KI1, 8, 36), (PSA, 103, 3), (JER, 31, 34)]),
    ("H6440", "פָּנִים", "panim", "paw-neem", "face, presenca", "Face, presenca, superficie. Buscar a face de Deus = buscar Sua presenca.", 2109, "GEN.1.2",
     [(GEN, 1, 2), (GEN, 32, 30), (EXO, 33, 14), (NUM, 6, 25), (PSA, 27, 8)]),
    ("H6662", "צַדִּיק", "tsaddiq", "tsad-deek", "justo, reto", "Justo, inocente, reto. Pessoa que vive conforme os padroes de Deus.", 206, "GEN.6.9",
     [(GEN, 6, 9), (GEN, 18, 23), (PSA, 1, 6), (PRO, 10, 25), (HAB, 2, 4)]),
    ("H6666", "צְדָקָה", "tsedaqah", "tsed-aw-kaw", "justica, retidao", "Justica, retidao, equidade. Atributo de Deus e padrao para Seu povo.", 157, "GEN.15.6",
     [(GEN, 15, 6), (DEU, 6, 25), (PSA, 24, 5), (ISA, 46, 13), (DAN, 9, 7)]),
    ("H6918", "קָדוֹשׁ", "qadosh", "kaw-doshe", "santo, sagrado", "Santo, separado, consagrado. Atributo primario de Deus: completamente puro e separado.", 116, "EXO.3.5",
     [(EXO, 3, 5), (LEV, 19, 2), (PSA, 99, 9), (ISA, 6, 3), (ISA, 57, 15)]),
    ("H7200", "רָאָה", "ra'ah", "raw-aw", "ver, olhar", "Ver, observar, perceber, considerar. Tanto visao fisica quanto percepcao espiritual.", 1311, "GEN.1.4",
     [(GEN, 1, 4), (GEN, 22, 14), (EXO, 3, 4), (PSA, 34, 8), (ISA, 6, 1)]),
    ("H7225", "רֵאשִׁית", "reshit", "ray-sheeth", "principio, inicio", "Principio, primicia, comeco. Primeira palavra da Biblia hebraica.", 51, "GEN.1.1",
     [(GEN, 1, 1), (DEU, 18, 4), (PRO, 1, 7), (PRO, 8, 22), (JER, 2, 3)]),
    ("H7307", "רוּחַ", "ruach", "roo-akh", "espirito, vento, sopro", "Espirito, vento, sopro, mente. O Espirito de Deus como forca criadora e vivificante.", 378, "GEN.1.2",
     [(GEN, 1, 2), (GEN, 6, 3), (NUM, 11, 25), (PSA, 51, 11), (EZK, 37, 9)]),
    ("H7355", "רָחַם", "racham", "raw-kham", "ter compaixao", "Ter misericordia, compaixao. Amor terno de Deus como o de uma mae por seu filho.", 47, "EXO.33.19",
     [(EXO, 33, 19), (DEU, 30, 3), (PSA, 103, 13), (ISA, 49, 15), (HOS, 2, 23)]),
    ("H7965", "שָׁלוֹם", "shalom", "shaw-lome", "paz, integridade", "Paz, completude, bem-estar, integridade. Muito mais que ausencia de conflito.", 236, "GEN.15.15",
     [(GEN, 15, 15), (NUM, 6, 26), (PSA, 29, 11), (ISA, 9, 6), (ISA, 53, 5)]),
    ("H8064", "שָׁמַיִם", "shamayim", "shaw-mah-yim", "ceus", "Ceus, firmamento, morada de Deus. Dual indicando a vastidao celeste.", 420, "GEN.1.1",
     [(GEN, 1, 1), (GEN, 1, 8), (DEU, 10, 14), (PSA, 19, 1), (ISA, 66, 1)]),
    ("H8085", "שָׁמַע", "shama", "shaw-mah", "ouvir, escutar", "Ouvir, escutar, obedecer. 'Shema' - 'Ouve, o Israel' (Dt 6:4).", 1159, "GEN.3.8",
     [(GEN, 3, 8), (DEU, 6, 4), (SAM1, 3, 10), (PSA, 34, 17), (ISA, 55, 3)]),
    ("H8104", "שָׁמַר", "shamar", "shaw-mar", "guardar, vigiar", "Guardar, observar, proteger, manter. Guardar os mandamentos de Deus.", 468, "GEN.2.15",
     [(GEN, 2, 15), (GEN, 28, 15), (EXO, 20, 6), (PSA, 121, 7), (PRO, 4, 23)]),
    ("H8451", "תּוֹרָה", "torah", "to-raw", "lei, instrucao", "Lei, ensinamento, instrucao divina. Mais que regras: orientacao de Deus para a vida.", 219, "GEN.26.5",
     [(GEN, 26, 5), (EXO, 24, 12), (DEU, 31, 9), (PSA, 1, 2), (PSA, 119, 97)]),
    ("H2416", "חַי", "chay", "khah-ee", "vivo, vida", "Vivo, vivente, vida. Deus como o Deus vivo; arvore da vida.", 501, "GEN.2.7",
     [(GEN, 2, 7), (GEN, 2, 9), (DEU, 30, 19), (PSA, 36, 9), (JER, 10, 10)]),
    ("H3519", "כָּבוֹד", "kabod", "kaw-bode", "gloria, honra", "Gloria, esplendor, honra, peso. A manifestacao visivel da presenca de Deus.", 200, "EXO.16.10",
     [(EXO, 16, 10), (EXO, 33, 18), (PSA, 19, 1), (ISA, 6, 3), (EZK, 1, 28)]),
    ("H4899", "מָשִׁיחַ", "mashiach", "maw-shee-akh", "ungido, messias", "Ungido, messias. Aquele escolhido por Deus com proposito especial.", 39, "LEV.4.3",
     [(LEV, 4, 3), (SAM1, 2, 10), (SAM2, 23, 1), (PSA, 2, 2), (DAN, 9, 25)]),
    ("H5769", "עוֹלָם", "olam", "o-lawm", "eternidade, para sempre", "Eternidade, tempo antigo, para sempre. Conceito de duracao sem fim.", 439, "GEN.3.22",
     [(GEN, 3, 22), (GEN, 21, 33), (PSA, 90, 2), (PSA, 103, 17), (ISA, 40, 28)]),
    ("H7462", "רָעָה", "ra'ah", "raw-aw", "pastorear, apascentar", "Pastorear, cuidar do rebanho. Deus como Pastor de Israel.", 167, "GEN.29.7",
     [(GEN, 29, 7), (GEN, 48, 15), (PSA, 23, 1), (ISA, 40, 11), (EZK, 34, 23)]),
    ("H3478", "יִשְׂרָאֵל", "Yisrael", "yis-raw-ale", "Israel", "Israel - 'aquele que luta com Deus'. Nome dado a Jaco e ao povo escolhido.", 2514, "GEN.32.28",
     [(GEN, 32, 28), (EXO, 4, 22), (DEU, 6, 4), (PSA, 14, 7), (ISA, 49, 3)]),
]

GREEK_ENTRIES = [
    ("G25", "ἀγαπάω", "agapao", "ag-ap-ah-o", "amar", "Amar com amor incondicional, escolher amar. Amor divino em acao.", 143, "MAT.5.44",
     [(MAT, 5, 44), (JHN, 3, 16), (JHN, 13, 34), (ROM, 8, 28), (JO1, 4, 8)]),
    ("G26", "ἀγάπη", "agape", "ag-ah-pay", "amor", "Amor incondicional, amor de Deus. O tipo mais elevado de amor no NT.", 116, "MAT.24.12",
     [(JHN, 15, 13), (ROM, 5, 8), (CO1, 13, 13), (EPH, 2, 4), (JO1, 4, 16)]),
    ("G40", "ἅγιος", "hagios", "hag-ee-os", "santo", "Santo, sagrado, separado para Deus. Descreve Deus, Seu Espirito e Seu povo.", 233, "MAT.1.18",
     [(MAT, 1, 18), (MAT, 28, 19), (ACT, 2, 4), (ROM, 1, 7), (PE1, 1, 16)]),
    ("G191", "ἀκούω", "akouo", "ak-oo-o", "ouvir", "Ouvir, escutar, entender, obedecer. Raiz da palavra 'acustica'.", 428, "MAT.2.3",
     [(MAT, 7, 24), (MRK, 4, 9), (JHN, 10, 27), (ROM, 10, 17), (REV, 2, 7)]),
    ("G225", "ἀλήθεια", "aletheia", "al-ay-thi-a", "verdade", "Verdade, realidade, sinceridade. Jesus como 'o caminho, a verdade e a vida'.", 109, "MAT.22.16",
     [(JHN, 1, 14), (JHN, 8, 32), (JHN, 14, 6), (JHN, 17, 17), (EPH, 4, 15)]),
    ("G266", "ἁμαρτία", "hamartia", "ham-ar-tee-ah", "pecado", "Pecado, errar o alvo. Desvio do proposito divino para a vida humana.", 173, "MAT.1.21",
     [(MAT, 1, 21), (JHN, 1, 29), (ROM, 3, 23), (ROM, 6, 23), (HEB, 9, 26)]),
    ("G386", "ἀνάστασις", "anastasis", "an-as-tas-is", "ressurreicao", "Ressurreicao, levantar-se dos mortos. Doutrina central do cristianismo.", 42, "MAT.22.23",
     [(MAT, 22, 30), (JHN, 11, 25), (ACT, 2, 31), (ROM, 6, 5), (CO1, 15, 42)]),
    ("G908", "βάπτισμα", "baptisma", "bap-tis-mah", "batismo", "Batismo, imersao. Rito de iniciacao e identificacao com Cristo.", 22, "MAT.3.7",
     [(MAT, 3, 7), (MAT, 28, 19), (ROM, 6, 4), (GAL, 3, 27), (EPH, 4, 5)]),
    ("G932", "βασιλεία", "basileia", "bas-il-i-ah", "reino", "Reino, reinado, dominio. O Reino de Deus como tema central de Jesus.", 162, "MAT.3.2",
     [(MAT, 3, 2), (MAT, 6, 33), (MRK, 1, 15), (LUK, 17, 21), (JHN, 18, 36)]),
    ("G991", "βλέπω", "blepo", "blep-o", "ver, olhar", "Ver, perceber, tomar cuidado. Visao tanto fisica quanto espiritual.", 133, "MAT.5.28",
     [(MAT, 5, 28), (MAT, 7, 3), (MRK, 8, 24), (CO2, 4, 18), (HEB, 2, 9)]),
    ("G1097", "γινώσκω", "ginosko", "ghin-oce-ko", "conhecer", "Conhecer por experiencia, entender, reconhecer. Conhecimento relacional.", 222, "MAT.1.25",
     [(MAT, 7, 23), (JHN, 8, 32), (JHN, 10, 14), (JHN, 17, 3), (PHP, 3, 10)]),
    ("G1189", "δέομαι", "deomai", "deh-om-ahee", "rogar, suplicar", "Suplicar, rogar, orar com urgencia.", 22, "MAT.9.38",
     [(MAT, 9, 38), (LUK, 22, 32), (ACT, 4, 31), (GAL, 4, 12), (TH1, 3, 10)]),
    ("G1325", "δίδωμι", "didomi", "did-o-mee", "dar", "Dar, conceder, entregar. Deus como o doador supremo de toda boa dadiva.", 413, "MAT.4.9",
     [(MAT, 7, 7), (JHN, 3, 16), (JHN, 10, 28), (ACT, 20, 35), (JAS, 1, 5)]),
    ("G1342", "δίκαιος", "dikaios", "dik-ah-yos", "justo", "Justo, reto, correto. Pessoa aprovada diante de Deus.", 79, "MAT.1.19",
     [(MAT, 1, 19), (MAT, 5, 45), (ROM, 3, 10), (ROM, 5, 19), (PE1, 3, 18)]),
    ("G1343", "δικαιοσύνη", "dikaiosune", "dik-ah-yos-oo-nay", "justica, retidao", "Justica, retidao de Deus. Justica imputada pela fe em Cristo.", 92, "MAT.3.15",
     [(MAT, 5, 6), (MAT, 6, 33), (ROM, 1, 17), (ROM, 3, 22), (PHP, 3, 9)]),
    ("G1411", "δύναμις", "dunamis", "doo-nam-is", "poder, milagre", "Poder, forca, capacidade, milagre. Poder de Deus operando no mundo.", 120, "MAT.6.13",
     [(MAT, 22, 29), (ACT, 1, 8), (ROM, 1, 16), (CO1, 1, 18), (EPH, 1, 19)]),
    ("G1515", "εἰρήνη", "eirene", "i-ray-nay", "paz", "Paz, harmonia, tranquilidade. Paz com Deus e paz interior.", 92, "MAT.10.13",
     [(LUK, 2, 14), (JHN, 14, 27), (ROM, 5, 1), (EPH, 2, 14), (PHP, 4, 7)]),
    ("G1577", "ἐκκλησία", "ekklesia", "ek-klay-see-ah", "igreja, assembleia", "Assembleia, congregacao, igreja. Comunidade dos chamados por Deus.", 114, "MAT.16.18",
     [(MAT, 16, 18), (ACT, 2, 47), (CO1, 12, 28), (EPH, 1, 22), (COL, 1, 18)]),
    ("G1680", "ἐλπίς", "elpis", "el-pis", "esperanca", "Esperanca, expectativa confiante. Esperanca baseada nas promessas de Deus.", 53, "ACT.2.26",
     [(ROM, 5, 5), (ROM, 8, 24), (CO1, 13, 13), (EPH, 1, 18), (HEB, 6, 19)]),
    ("G1849", "ἐξουσία", "exousia", "ex-oo-see-ah", "autoridade, poder", "Autoridade, poder, direito, jurisdicao. Autoridade delegada por Deus.", 102, "MAT.7.29",
     [(MAT, 28, 18), (JHN, 1, 12), (ROM, 13, 1), (EPH, 1, 21), (COL, 1, 16)]),
    ("G2064", "ἔρχομαι", "erchomai", "er-khom-ahee", "vir, chegar", "Vir, chegar, aparecer. Usado para a vinda de Cristo.", 636, "MAT.2.2",
     [(MAT, 11, 28), (JHN, 1, 11), (JHN, 6, 37), (JHN, 14, 3), (REV, 22, 20)]),
    ("G2098", "εὐαγγέλιον", "euaggelion", "yoo-ang-ghel-ee-on", "evangelho, boa nova", "Boa noticia, evangelho. A mensagem de salvacao em Jesus Cristo.", 76, "MAT.4.23",
     [(MAT, 4, 23), (MRK, 1, 1), (ROM, 1, 16), (CO1, 15, 1), (GAL, 1, 7)]),
    ("G2222", "ζωή", "zoe", "dzo-ay", "vida", "Vida, especialmente vida eterna. Vida abundante em Cristo.", 135, "MAT.7.14",
     [(JHN, 1, 4), (JHN, 3, 16), (JHN, 10, 10), (JHN, 14, 6), (ROM, 6, 23)]),
    ("G2288", "θάνατος", "thanatos", "than-at-os", "morte", "Morte, tanto fisica quanto espiritual. Separacao de Deus.", 120, "MAT.4.16",
     [(ROM, 5, 12), (ROM, 6, 23), (CO1, 15, 26), (PHP, 2, 8), (REV, 21, 4)]),
    ("G2316", "θεός", "theos", "theh-os", "Deus", "Deus, divindade. O Deus verdadeiro e unico.", 1317, "MAT.1.23",
     [(MAT, 1, 23), (JHN, 1, 1), (JHN, 3, 16), (ROM, 8, 28), (HEB, 11, 6)]),
    ("G2424", "Ἰησοῦς", "Iesous", "ee-ay-sooce", "Jesus", "Jesus - forma grega de Yeshua. 'O Senhor salva'.", 917, "MAT.1.1",
     [(MAT, 1, 1), (MAT, 1, 21), (LUK, 2, 21), (JHN, 1, 17), (ACT, 4, 12)]),
    ("G2588", "καρδία", "kardia", "kar-dee-ah", "coracao", "Coracao, centro do ser interior. Sede dos pensamentos e emocoes.", 156, "MAT.5.8",
     [(MAT, 5, 8), (MAT, 22, 37), (ROM, 10, 9), (EPH, 3, 17), (HEB, 4, 12)]),
    ("G2784", "κηρύσσω", "kerusso", "kay-roos-so", "pregar, proclamar", "Pregar, proclamar como arauto. Anunciar a mensagem do evangelho.", 61, "MAT.3.1",
     [(MAT, 4, 17), (MRK, 1, 14), (ACT, 28, 31), (ROM, 10, 14), (TI2, 4, 2)]),
    ("G2889", "κόσμος", "kosmos", "kos-mos", "mundo", "Mundo, universo, humanidade. O sistema mundial em oposicao a Deus.", 186, "MAT.4.8",
     [(JHN, 1, 10), (JHN, 3, 16), (JHN, 16, 33), (ROM, 12, 2), (JO1, 2, 15)]),
    ("G2962", "κύριος", "kurios", "koo-ree-os", "Senhor", "Senhor, mestre, dono. Titulo de Jesus indicando Sua divindade.", 717, "MAT.1.20",
     [(MAT, 7, 21), (ACT, 2, 36), (ROM, 10, 9), (CO1, 12, 3), (PHP, 2, 11)]),
    ("G3004", "λέγω", "lego", "leg-o", "dizer, falar", "Dizer, falar, declarar. Comunicar uma mensagem.", 1343, "MAT.1.20",
     [(MAT, 5, 22), (MAT, 16, 15), (JHN, 1, 1), (JHN, 14, 6), (REV, 22, 17)]),
    ("G3056", "λόγος", "logos", "log-os", "palavra, verbo", "Palavra, razao, discurso. Jesus como o Verbo (Logos) encarnado.", 330, "MAT.7.24",
     [(JHN, 1, 1), (JHN, 1, 14), (ACT, 6, 7), (HEB, 4, 12), (REV, 19, 13)]),
    ("G3107", "μακάριος", "makarios", "mak-ar-ee-os", "bem-aventurado", "Feliz, abençoado, bem-aventurado. Estado de bencao divina.", 50, "MAT.5.3",
     [(MAT, 5, 3), (LUK, 1, 45), (JHN, 20, 29), (ROM, 4, 7), (REV, 1, 3)]),
    ("G3341", "μετάνοια", "metanoia", "met-an-oy-ah", "arrependimento", "Mudanca de mente, arrependimento. Transformacao radical de pensamento.", 24, "MAT.3.8",
     [(MAT, 3, 8), (MRK, 1, 4), (LUK, 15, 7), (ACT, 2, 38), (PE2, 3, 9)]),
    ("G3551", "νόμος", "nomos", "nom-os", "lei", "Lei, principio, Torah. A lei de Moises e a lei moral de Deus.", 194, "MAT.5.17",
     [(MAT, 5, 17), (JHN, 1, 17), (ROM, 3, 21), (ROM, 7, 7), (GAL, 3, 24)]),
    ("G3962", "πατήρ", "pater", "pat-ayr", "pai", "Pai, ancestral. Deus como Pai de Jesus e dos crentes.", 413, "MAT.2.22",
     [(MAT, 6, 9), (JHN, 1, 14), (JHN, 14, 9), (ROM, 8, 15), (EPH, 4, 6)]),
    ("G4100", "πιστεύω", "pisteuo", "pist-yoo-o", "crer, confiar", "Crer, ter fe, confiar. Ato de confiar em Deus e em Cristo.", 241, "MAT.8.13",
     [(JHN, 1, 12), (JHN, 3, 16), (JHN, 11, 25), (ACT, 16, 31), (ROM, 10, 9)]),
    ("G4102", "πίστις", "pistis", "pis-tis", "fe, confianca", "Fe, confianca, fidelidade. Confianca em Deus e em Suas promessas.", 244, "MAT.8.10",
     [(MAT, 17, 20), (ROM, 1, 17), (GAL, 2, 20), (EPH, 2, 8), (HEB, 11, 1)]),
    ("G4151", "πνεῦμα", "pneuma", "pnyoo-mah", "espirito", "Espirito, vento, sopro. O Espirito Santo de Deus.", 379, "MAT.1.18",
     [(MAT, 3, 16), (JHN, 3, 8), (JHN, 14, 26), (ACT, 2, 4), (ROM, 8, 16)]),
    ("G4160", "ποιέω", "poieo", "poy-eh-o", "fazer, criar", "Fazer, produzir, criar, agir. Realizar a vontade de Deus.", 568, "MAT.1.24",
     [(MAT, 7, 21), (JHN, 2, 5), (JHN, 15, 5), (ROM, 7, 15), (JAS, 1, 22)]),
    ("G4336", "προσεύχομαι", "proseuchomai", "pros-yoo-khom-ahee", "orar", "Orar, fazer oracoes a Deus. Comunicacao reverente com Deus.", 85, "MAT.5.44",
     [(MAT, 6, 9), (MAT, 26, 39), (MRK, 1, 35), (LUK, 18, 1), (TH1, 5, 17)]),
    ("G4561", "σάρξ", "sarx", "sarx", "carne", "Carne, corpo, natureza humana. Natureza pecaminosa em contraste com o Espirito.", 147, "MAT.16.17",
     [(JHN, 1, 14), (ROM, 7, 18), (ROM, 8, 4), (GAL, 5, 17), (JO1, 4, 2)]),
    ("G4716", "σταυρός", "stauros", "stow-ros", "cruz", "Cruz, poste de execucao. Instrumento de morte de Cristo e simbolo da fe.", 27, "MAT.10.38",
     [(MAT, 16, 24), (CO1, 1, 17), (GAL, 6, 14), (EPH, 2, 16), (COL, 1, 20)]),
    ("G4982", "σώζω", "sozo", "sode-zo", "salvar", "Salvar, resgatar, curar, preservar. Salvacao espiritual e fisica.", 106, "MAT.1.21",
     [(MAT, 1, 21), (JHN, 3, 17), (ACT, 2, 21), (ROM, 10, 9), (EPH, 2, 8)]),
    ("G5207", "υἱός", "huios", "hwee-os", "filho", "Filho, descendente. Jesus como o Filho de Deus.", 377, "MAT.1.1",
     [(MAT, 3, 17), (JHN, 1, 12), (JHN, 3, 16), (ROM, 8, 14), (GAL, 4, 4)]),
    ("G5485", "χάρις", "charis", "khar-ece", "graca", "Graca, favor imerecido, bondade divina. Base da salvacao.", 155, "LUK.2.40",
     [(JHN, 1, 14), (ACT, 15, 11), (ROM, 3, 24), (EPH, 2, 8), (TIT, 2, 11)]),
    ("G5547", "Χριστός", "Christos", "khris-tos", "Cristo, ungido", "Cristo, o Ungido. Titulo messianico de Jesus, equivalente grego de Mashiach.", 529, "MAT.1.1",
     [(MAT, 1, 1), (MAT, 16, 16), (ACT, 2, 36), (ROM, 5, 8), (GAL, 2, 20)]),
    ("G5590", "ψυχή", "psyche", "psoo-khay", "alma, vida", "Alma, vida, pessoa, ser interior. Parte imaterial do ser humano.", 103, "MAT.2.20",
     [(MAT, 10, 28), (MAT, 16, 26), (MRK, 8, 36), (JHN, 10, 11), (HEB, 4, 12)]),
]
# fmt: on


def populate():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    inserted_entries = 0
    inserted_occs = 0
    skipped = 0

    all_entries = HEBREW_ENTRIES + GREEK_ENTRIES

    try:
        for i, (strong, original, translit, pronun, meaning, definition, count, first, occurrences) in enumerate(all_entries):
            existing = db.query(LexiconEntry).filter_by(strong_number=strong).first()
            if existing:
                skipped += 1
                continue

            lang = "hebrew" if strong.startswith("H") else "greek"
            entry = LexiconEntry(
                strong_number=strong,
                language=lang,
                original_word=original,
                transliteration=translit,
                pronunciation=pronun,
                basic_meaning=meaning,
                extended_definition=definition,
                usage_count=count,
                first_occurrence=first,
            )
            db.add(entry)
            db.flush()  # get ID
            inserted_entries += 1

            for book, chap, verse in occurrences:
                occ = WordOccurrence(
                    lexicon_entry_id=entry.id,
                    book_number=book,
                    chapter=chap,
                    verse=verse,
                )
                db.add(occ)
                inserted_occs += 1

            if inserted_entries % 50 == 0:
                db.commit()
                print(f"  ... committed batch ({inserted_entries} entries so far)")

        db.commit()
        print(
            f"Done. Inserted {inserted_entries} lexicon entries + {inserted_occs} occurrences "
            f"({skipped} duplicates skipped, {len(all_entries)} total in seed)."
        )
    except Exception as exc:
        db.rollback()
        print(f"Error: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate()
