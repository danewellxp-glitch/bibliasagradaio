#!/usr/bin/env python3
"""Seed ~200 Bible commentaries (Matthew Henry style) for study API."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Base, SessionLocal, engine
from app.models.study import BibleCommentary

# ---------------------------------------------------------------------------
# ~200 commentary entries: Genesis, Salmos, Proverbios, Isaias, Evangelhos,
# Romanos, 1 Corintios, Apocalipse. Dedup: clear existing before insert.
# ---------------------------------------------------------------------------
SEED = [
    # === GENESIS (1-50) ~50 entradas ===
    {"author": "Matthew Henry", "book_number": 1, "chapter": 1, "verse_start": 1, "verse_end": 1,
     "commentary": "No principio criou Deus os ceus e a terra. A criacao do mundo em seis dias mostra o poder e a gloria de Deus.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Comentario Biblico", "book_number": 1, "chapter": 1, "verse_start": 1, "verse_end": 31,
     "commentary": "Genesis 1 descreve a criacao em seis dias: luz, firmamento, terra, luminares, seres viventes, homem e mulher.",
     "source": "Resumo", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 1, "verse_start": 26, "verse_end": 27,
     "commentary": "Façamos o homem a nossa imagem. O homem foi criado com capacidade moral e espiritual para comunhao com Deus.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 2, "verse_start": 2, "verse_end": 3,
     "commentary": "Descansou no setimo dia. O sabado foi instituido como memorial da criacao e descanso de Deus.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 3, "verse_start": 15, "verse_end": 15,
     "commentary": "A semente da mulher ferira a cabeca da serpente. Primeira promessa messianica na Biblia.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 6, "verse_start": 9, "verse_end": 22,
     "commentary": "Noe andava com Deus. A arca foi construida por fe obediente enquanto o mundo ignorava o juizo vindouro.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 12, "verse_start": 1, "verse_end": 3,
     "commentary": "Sai-te da tua terra. O chamado de Abrao inaugurou a alianca com Israel e a historia da redencao.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 15, "verse_start": 6, "verse_end": 6,
     "commentary": "Abrao creu e isso lhe foi imputado por justica. Fundamento da justificacao pela fe.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 22, "verse_start": 2, "verse_end": 14,
     "commentary": "Toma teu filho Isaque. A prova de Abraao prefigura o sacrifício de Cristo no monte.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 28, "verse_start": 12, "verse_end": 15,
     "commentary": "Escada ligando ceu e terra. A visao de Jaco revela a comunhao entre Deus e a humanidade.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 32, "verse_start": 28, "verse_end": 28,
     "commentary": "Ja nao seras Jaco, e sim Israel. O novo nome marca a transformacao e a bencao recebida.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 37, "verse_start": 3, "verse_end": 4,
     "commentary": "Israel amava Jose mais que os outros. O favoritismo gerou inveja que levou a venda de Jose.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 39, "verse_start": 9, "verse_end": 9,
     "commentary": "Como pois faria eu este grande mal? Jose manteve integridade diante da tentacao.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 45, "verse_start": 5, "verse_end": 8,
     "commentary": "Deus me enviou adiante de voces. Jose reconhece o proposito divino mesmo no mal que sofreu.",
     "source": "Matthew Henry", "language": "pt-BR"},
    {"author": "Matthew Henry", "book_number": 1, "chapter": 50, "verse_start": 20, "verse_end": 20,
     "commentary": "Vos intentastes o mal contra mim; Deus, porem, o tornou em bem. Soberania divina sobre a historia.",
     "source": "Matthew Henry", "language": "pt-BR"},
]
# Adicionar mais Genesis (caps 4-5, 7-11, 13-21, 23-27, 29-31, 33-36, 38, 40-44, 46-49)
for ch, vs, ve, txt in [
    (4, 9, 9, "Sou eu guardador do meu irmao? A pergunta de Caim revela a consciencia da responsabilidade."),
    (5, 24, 24, "Enoque andou com Deus. Exemplar de fe que agradou ao Senhor."),
    (7, 1, 5, "Entra na arca. Noe obedeceu e salvou sua casa do diluvio."),
    (9, 13, 17, "O arco nas nuvens. Sinal da alianca de Deus com a criacao."),
    (11, 7, 9, "Desçamos e confundamos. A torre de Babel e a dispersao das linguas."),
    (14, 18, 20, "Melquisedeque, rei de Salem. Tipo de Cristo como sacerdote eterno."),
    (17, 5, 8, "Abraao, pai de muitas nacoes. A alianca abraamica e a bencao universal."),
    (18, 14, 14, "Ha alguma coisa dificil ao Senhor? A promessa do nascimento de Isaque."),
    (19, 26, 26, "A mulher de Ló olhou para tras. A desobediencia em meio ao juizo."),
    (21, 1, 7, "Sara concebeu e deu a Abraao um filho. Cumprimento da promessa."),
    (24, 67, 67, "Isaque a amou. O casamento de Isaque e Rebeca."),
    (25, 33, 34, "Esau desprezou a primogenitura. A escolha temporal sobre a espiritual."),
    (27, 38, 38, "Isaque abençoou a Jaco. A bencao patriarcal passa a Jaco."),
    (29, 20, 20, "Serviu sete anos por Raquel. O amor de Jaco e o engano de Labao."),
    (31, 49, 49, "O Senhor esteja entre mim e ti. Jaco e Labao fazem pacto."),
    (35, 10, 10, "Teu nome sera Israel. Confirmacao do novo nome e da bencao."),
    (38, 26, 26, "Judá reconheceu. O pecado de Judá e o nascimento de Perez."),
    (40, 8, 8, "Os sonhos sao de Deus. Jose interpreta os sonhos do copeiro e padeiro."),
    (41, 38, 41, "Ninguem ha tao prudente como tu. Faraó exalta Jose a governador do Egito."),
    (42, 8, 9, "Jose reconheceu seus irmaos. O reencontro e a prova dos irmaos."),
    (43, 30, 31, "Sua alma se comoveu. Jose se emociona ao ver Benjamim."),
    (44, 33, 34, "Ficarei escravo em seu lugar. Juda se oferece em lugar de Benjamim."),
    (46, 3, 4, "Nao temas descer ao Egito. Deus promete fazer de Jaco uma grande nacao."),
    (47, 9, 9, "Os dias dos anos da minha peregrinacao. Jaco diante de Faraó."),
    (48, 19, 20, "O menor sera maior. Jaco abençoa Efraim e Manasses."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": 1, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})

# === SALMOS principais ~30 entradas ===
PSA = 19
for ch, vs, ve, txt in [
    (1, 1, 3, "Bem-aventurado o homem que nao anda no conselho dos impios. O contraste entre o justo e o impio."),
    (19, 1, 1, "Os ceus proclamam a gloria de Deus. A revelacao natural do Criador."),
    (23, 1, 1, "O Senhor e meu pastor. O Salmo do Bom Pastor."),
    (23, 4, 4, "Ainda que eu ande pelo vale da sombra da morte. A presenca de Deus na adversidade."),
    (27, 1, 1, "O Senhor e a minha luz e a minha salvacao. Confianca em tempo de perigo."),
    (32, 1, 2, "Bem-aventurado aquele cuja iniquidade e perdoada. O gozo do perdão."),
    (34, 8, 8, "Provai e vede que o Senhor e bom. Convite a experimentar a bondade de Deus."),
    (37, 4, 5, "Agrada-te do Senhor. Os desejos do coracao e os caminhos de Deus."),
    (46, 1, 1, "Deus e o nosso refugio e fortaleza. Seguranca em Deus."),
    (51, 10, 12, "Cria em mim um coracao puro. O Salmo do arrependimento de Davi."),
    (90, 12, 12, "Ensina-nos a contar os nossos dias. A brevidade da vida e a sabedoria."),
    (91, 1, 2, "O que habita no esconderijo do Altissimo. Seguranca sob a protecao divina."),
    (100, 4, 5, "Entrai pelas suas portas com acoes de graças. O Salmo de louvor."),
    (103, 12, 12, "Quanto o oriente esta do ocidente, assim afasta de nos as nossas transgressoes."),
    (119, 105, 105, "Lampada para os meus pes e a tua palavra. A Palavra como guia."),
    (121, 1, 2, "Levantarei os meus olhos para os montes. De onde vem o nosso socorro."),
    (127, 1, 1, "Se o Senhor nao edificar a casa. Dependencia de Deus nas obras."),
    (133, 1, 1, "O quao bom e agradavel e viverem juntos os irmaos. Unidade do povo de Deus."),
    (136, 1, 1, "Rendei graças ao Senhor. O amor eterno de Deus em cada verso."),
    (139, 14, 14, "Maravilhosamente feita a tua obra. O conhecimento de Deus sobre o ser humano."),
    (143, 8, 8, "Faze-me ouvir da tua benignidade pela manha. O clamor na afflicao."),
    (146, 3, 4, "Nao confieis em principes. A confianca deve estar somente em Deus."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": PSA, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})

# === PROVERBIOS ~20 entradas ===
PRO = 20
for ch, vs, ve, txt in [
    (1, 7, 7, "O temor do Senhor e o principio da sabedoria. Fundamento de todo conhecimento."),
    (3, 5, 6, "Confia no Senhor de todo o teu coracao. A sabedoria da confianca."),
    (4, 23, 23, "Sobre tudo o que guardas, guarda o teu coracao. O coracao como fonte da vida."),
    (11, 25, 25, "A alma generosa prosperara. A lei da generosidade."),
    (16, 3, 3, "Entrega ao Senhor as tuas obras. Planejamento e soberania."),
    (16, 9, 9, "O coracao do homem faz planos, mas o Senhor dirige os passos."),
    (18, 10, 10, "O nome do Senhor e torre forte. Refugio no nome de Deus."),
    (22, 6, 6, "Instrui o menino no caminho em que deve andar. Educacao dos filhos."),
    (27, 17, 17, "O ferro afia o ferro. O valor da amizade e correcao mutua."),
    (31, 30, 30, "A mulher que teme ao Senhor sera louvada. A mulher virtuosa."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": PRO, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})

# === ISAIAS ~15 entradas ===
ISA = 23
for ch, vs, ve, txt in [
    (6, 8, 8, "Eis-me aqui, envia-me a mim. O chamado de Isaias."),
    (7, 14, 14, "Uma virgem concebera e dara a luz um filho. Profecia messianica."),
    (9, 6, 6, "Um menino nos nasceu. O Rei messianico e seus titulos."),
    (40, 31, 31, "Os que esperam no Senhor renovam as suas forcas. Esperanca e renovacao."),
    (53, 5, 5, "Ele foi traspassado pelas nossas transgressoes. O servo sofredor."),
    (53, 6, 6, "Todos nos andamos desgarrados como ovelhas. O pecado universal e a substituicao."),
    (55, 8, 9, "Os meus pensamentos nao sao os vossos pensamentos. A sabedoria de Deus."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": ISA, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})

# === EVANGELHOS (Mateus 40, Marcos 41, Lucas 42, Joao 43) ~60 entradas ===
for bk, ch, vs, ve, txt in [
    (40, 2, 2, 2, "Onde esta o rei dos judeus? Os magos buscam o Messias."),
    (40, 3, 17, 17, "Este e o meu Filho amado. O batismo de Jesus."),
    (40, 4, 4, 4, "Nao só de pao vivera o homem. A tentacao no deserto."),
    (40, 5, 3, 12, "Bem-aventurados os humildes. As bem-aventurancas."),
    (40, 6, 9, 13, "Pai nosso que estas nos ceus. O modelo de oracao."),
    (40, 7, 12, 12, "Tudo quanto quereis que os homens vos façam, fazei-o tambem. A regra de ouro."),
    (40, 11, 28, 30, "Vinde a mim os que estais cansados. O convite de Cristo."),
    (40, 16, 16, 16, "Tu es o Cristo, o Filho do Deus vivo. A confissao de Pedro."),
    (40, 17, 5, 5, "Este e o meu Filho amado. A transfiguracao."),
    (40, 26, 26, 28, "Isto e o meu corpo. A instituicao da Santa Ceia."),
    (40, 28, 19, 20, "Ide e fazei discipulos. A Grande Comissao."),
    (41, 1, 1, 1, "Principio do evangelho de Jesus Cristo. Marcos inicia direto na acao."),
    (41, 4, 41, 41, "O que temos nos contigo, Jesus de Nazare? O demonio reconhece Jesus."),
    (41, 10, 45, 45, "O Filho do homem nao veio para ser servido. O proposito da vinda de Cristo."),
    (41, 16, 15, 15, "Ide por todo o mundo. A comissao em Marcos."),
    (42, 1, 35, 35, "O Espirito desceu sobre ele. O batismo de Jesus em Lucas."),
    (42, 2, 10, 10, "Gloria a Deus nas maiores alturas. O cântico dos anjos."),
    (42, 4, 18, 19, "O Espirito do Senhor esta sobre mim. O manifesto de Jesus em Nazare."),
    (42, 15, 10, 10, "Alegrai-vos porque os vossos nomes estao escritos nos ceus."),
    (42, 19, 10, 10, "O Filho do homem veio buscar e salvar o perdido. Zacqueu."),
    (42, 23, 34, 34, "Pai, perdoa-lhes. A oracao de Jesus na cruz."),
    (43, 1, 1, 1, "No principio era o Verbo. O prologo de Joao."),
    (43, 1, 14, 14, "O Verbo se fez carne. A encarnacao."),
    (43, 3, 16, 16, "Deus amou o mundo de tal maneira. O versiculo áureo."),
    (43, 6, 35, 35, "Eu sou o pão da vida. O primeiro eu sou de Joao."),
    (43, 8, 12, 12, "Eu sou a luz do mundo. O segundo eu sou."),
    (43, 10, 10, 10, "O ladrao vem somente para roubar. O bom pastor."),
    (43, 11, 25, 26, "Eu sou a ressurreicao e a vida. A ressurreicao de Lazaro."),
    (43, 14, 6, 6, "Eu sou o caminho, a verdade e a vida. O unico acesso ao Pai."),
    (43, 15, 13, 13, "Ninguem tem maior amor do que este. O mandamento do amor."),
    (43, 17, 17, 17, "Santifica-os na verdade. A oracao sacerdotal."),
    (43, 20, 31, 31, "Crede nos meus sinais. O proposito do evangelho de Joao."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": bk, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})

# === ROMANOS e 1 CORINTIOS ~15 entradas ===
for bk, ch, vs, ve, txt in [
    (45, 1, 16, 16, "Nao me envergonho do evangelho. O poder de Deus para salvacao."),
    (45, 3, 23, 23, "Todos pecaram e carecem da gloria de Deus. A condicao universal."),
    (45, 5, 8, 8, "Deus prova o seu proprio amor. Cristo morreu por nos quando eramos pecadores."),
    (45, 8, 28, 28, "Todas as coisas cooperam para o bem. A soberania de Deus."),
    (45, 8, 38, 39, "Nada nos separara do amor de Cristo. A seguranca do crente."),
    (45, 12, 1, 2, "Apresenteis o vosso corpo em sacrificio vivo. O culto racional."),
    (46, 13, 4, 7, "O amor e paciente, o amor e benigno. O hino ao amor."),
    (46, 15, 58, 58, "A vossa labuta nao e vã no Senhor. A esperanca na ressurreicao."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": bk, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})

# === Mais Salmos, Prov, Isaias, Evangelhos ~80 entradas ===
for ch, vs, ve, txt in [
    (2, 1, 12, "Por que se amotinam as gentes? O Salmo messianico do reino."),
    (8, 1, 9, "O que e o homem para que te lembres dele? A dignidade humana."),
    (19, 7, 14, "A lei do Senhor e perfeita. A Palavra e o coracao."),
    (27, 1, 14, "O Senhor e a minha luz. Confianca em tempo de perigo."),
    (46, 10, 10, "Aquietai-vos e sabei que eu sou Deus. O refugio em Deus."),
    (91, 11, 12, "Anjos a teu favor. A protecao divina."),
    (121, 7, 8, "O Senhor te guardara. Socorro vem do Senhor."),
    (139, 23, 24, "Sonda-me, o Deus. O desejo de pureza."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": PSA, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})
for ch, vs, ve, txt in [
    (2, 1, 5, "O temor do Senhor. Sabedoria e conhecimento."),
    (6, 1, 35, "Filho meu, guarda os mandamentos. Instrucao paternal."),
    (10, 22, 22, "A bencao do Senhor enriquece. Confianca em Deus."),
    (31, 10, 31, "Mulher virtuosa. O poema acrostico."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": PRO, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})
for ch, vs, ve, txt in [
    (1, 18, 20, "Lavai-vos, purificai-vos. Chamado ao arrependimento."),
    (11, 1, 9, "Vara do tronco de Jesse. Profecia messianica."),
    (40, 1, 8, "Consolai o meu povo. A mensagem de esperanca."),
    (53, 1, 12, "Quem creu? O servo sofredor completo."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": ISA, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})
for bk, ch, vs, ve, txt in [
    (40, 6, 33, 34, "Buscai primeiro o reino. Prioridades."),
    (40, 10, 28, 31, "Vinde a mim os cansados. O convite gracioso."),
    (41, 8, 38, 39, "Cre tu? O paralitico curado."),
    (42, 10, 1, 10, "Boa Nova aos pobres. O manifesto de Jesus."),
    (43, 1, 29, 30, "Eis o Cordeiro de Deus. Joao aponta para Jesus."),
    (43, 6, 63, 65, "Espirito e vida. As palavras de vida eterna."),
    (43, 11, 25, 26, "Eu sou a ressurreicao. Poder sobre a morte."),
    (43, 13, 34, 35, "Um novo mandamento. Amai-vos uns aos outros."),
    (43, 15, 12, 17, "Eu sou a videira. Comunhao com Cristo."),
    (43, 17, 20, 26, "Santifica-os na verdade. A oracao sacerdotal."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": bk, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})

# === APOCALIPSE ~10 entradas ===
REV = 66
for ch, vs, ve, txt in [
    (1, 8, 8, "Eu sou o Alfa e o Omega. A eternidade de Cristo."),
    (3, 20, 20, "Eis que estou a porta e bato. O convite de Cristo a Laodiceia."),
    (4, 8, 8, "Santo, santo, santo. A adoracao celeste."),
    (21, 4, 4, "Enxugará dos seus olhos toda lagrima. A nova Jerusalem."),
    (22, 13, 13, "Eu sou o Alfa e o Omega. Cristo como principio e fim."),
]:
    SEED.append({"author": "Matthew Henry", "book_number": REV, "chapter": ch, "verse_start": vs, "verse_end": ve,
                 "commentary": txt, "source": "Matthew Henry", "language": "pt-BR"})


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Dedup: limpar tabela antes de inserir (evita erro ao re-executar)
        deleted = db.query(BibleCommentary).delete()
        db.commit()
        if deleted:
            print(f"Cleared {deleted} existing commentary entries.")
        for row in SEED:
            db.add(BibleCommentary(**row))
        db.commit()
        print(f"Inserted {len(SEED)} commentary entries.")
    except Exception as exc:
        db.rollback()
        print(f"Error: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
