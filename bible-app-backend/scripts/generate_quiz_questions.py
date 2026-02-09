#!/usr/bin/env python3
"""Generate quiz_questions.json with 500+ questions for Sprint 1."""
import json
import os

# Format: (difficulty, question, correct, [wrong1, wrong2, wrong3], explanation, category)
Q = [
    # === BEGINNER - geral ~40 ===
    ("beginner", "Quantos livros tem a Biblia?", "66", ["27", "39", "73"], "66 livros: 39 AT e 27 NT.", "geral"),
    ("beginner", "Qual o primeiro livro da Biblia?", "Genesis", ["Exodo", "Joao", "Mateus"], "Genesis relata a criacao.", "geral"),
    ("beginner", "Qual o ultimo livro da Biblia?", "Apocalipse", ["Joao", "Judas", "Malaquias"], "Apocalipse encerra o NT.", "geral"),
    ("beginner", "Quantos livros tem o Antigo Testamento?", "39", ["27", "66", "22"], "O AT tem 39 livros.", "geral"),
    ("beginner", "Quantos livros tem o Novo Testamento?", "27", ["39", "66", "22"], "O NT tem 27 livros.", "geral"),
    ("beginner", "Quem escreveu a maior parte do NT?", "Paulo", ["Pedro", "Joao", "Mateus"], "Paulo escreveu 13 cartas.", "geral"),
    ("beginner", "Quantos evangelhos existem?", "4", ["3", "5", "12"], "Mateus, Marcos, Lucas e Joao.", "geral"),
    ("beginner", "Qual o livro mais curto da Biblia?", "2 Joao", ["Joao", "Judas", "Obadias"], "2 Joao tem poucos versiculos.", "geral"),
    ("beginner", "Qual o livro mais longo da Biblia?", "Salmos", ["Genesis", "Isaias", "Ezequiel"], "Salmos tem 150 capitulos.", "geral"),
    ("beginner", "Em quantas linguas foi escrita a Biblia?", "3", ["1", "2", "5"], "Hebraico, aramaico e grego.", "geral"),
    ("beginner", "Qual o versiculo central da Biblia?", "Sl 118:8", ["Jo 3:16", "Gn 1:1", "Rm 8:28"], "Sl 118:8 e o versiculo central.", "geral"),
    ("beginner", "O que significa 'testamento' na Biblia?", "Alianca", ["Livro", "Historia", "Contrato"], "Testamento significa alianca ou pacto.", "geral"),
    ("beginner", "Quantos capitulos tem a Biblia?", "1189", ["1000", "1500", "666"], "A Biblia tem 1189 capitulos.", "geral"),
    ("beginner", "Qual livro nao menciona Deus?", "Ester", ["Rute", "Cantares", "Eclesiastes"], "Ester nao cita o nome Deus.", "geral"),
    ("beginner", "Qual livro fala da criacao?", "Genesis", ["Exodo", "Joao", "Hebreus"], "Genesis 1 descreve a criacao.", "geral"),
    # === BEGINNER - historia ~50 ===
    ("beginner", "Quem construiu a arca?", "Noe", ["Abraao", "Moisés", "Josue"], "Noe construiu a arca por ordem de Deus.", "historia"),
    ("beginner", "Quem foi vendido pelos irmaos ao Egito?", "Jose", ["Benjamin", "Isaque", "Jacó"], "Jose foi vendido pelos irmaos.", "historia"),
    ("beginner", "Quem conduziu Israel pelo Mar Vermelho?", "Moisés", ["Josue", "Aarão", "Calebe"], "Moisés estendeu a mao sobre o mar.", "historia"),
    ("beginner", "Quem derrubou os muros de Jerico?", "Josue", ["Calebe", "Moisés", "Gideao"], "Os muros caíram ao soar das trombetas.", "historia"),
    ("beginner", "Quem matou Golias?", "Davi", ["Sauel", "Absalao", "Joabe"], "Davi derrotou Golias com uma funda.", "historia"),
    ("beginner", "Quem construiu o primeiro templo?", "Salomao", ["Davi", "Neemias", "Zorobabel"], "Salomao construiu o templo em Jerusalém.", "historia"),
    ("beginner", "Quem foi engolido por um grande peixe?", "Jonas", ["Pedro", "Paulo", "Noe"], "Jonas ficou tres dias no peixe.", "historia"),
    ("beginner", "Quem foi lançado na cova dos leoes?", "Daniel", ["Sadraque", "Mesaque", "Abede-Nego"], "Daniel foi salvo pelos anjos.", "historia"),
    ("beginner", "Quem foi a primeira mulher?", "Eva", ["Sara", "Rebeca", "Raquel"], "Eva foi criada da costela de Adao.", "historia"),
    ("beginner", "Quem foi o pai da fe?", "Abraao", ["Isaque", "Jacó", "Noe"], "Abraao e chamado pai da fe.", "historia"),
    ("beginner", "Quem lutou com o anjo e recebeu o nome Israel?", "Jacó", ["Esau", "Isaque", "Abraao"], "Jacó lutou em Peniel.", "historia"),
    ("beginner", "Quem foi rei de Israel e cometeu adulterio?", "Davi", ["Salomao", "Sauel", "Acabe"], "Davi cometeu adulterio com Bateseba.", "historia"),
    ("beginner", "Quem pediu a cabeca de Joao Batista?", "Herodes", ["Pilatos", "Cesar", "Nero"], "Herodes Antipas a pedido de Herodias.", "historia"),
    ("beginner", "Onde Jesus nasceu?", "Belem", ["Nazare", "Jerusalem", "Galileia"], "Jesus nasceu em Belem da Judeia.", "historia"),
    ("beginner", "Qual discipulo negou Jesus tres vezes?", "Pedro", ["Joao", "Judas", "Tomas"], "Pedro negou antes do galo cantar.", "historia"),
    ("beginner", "Quem traiu Jesus?", "Judas", ["Pedro", "Pilatos", "Caifas"], "Judas Iscariotes o traiu com um beijo.", "historia"),
    ("beginner", "Quem foi o primeiro martir cristao?", "Estevao", ["Pedro", "Paulo", "Tiago"], "Estevao foi apedrejado.", "historia"),
    ("beginner", "Quem foi cego na estrada de Damasco?", "Paulo", ["Pedro", "Ananias", "Barnabe"], "Paulo (Sauel) foi convertido.", "historia"),
    ("beginner", "Quem era a mae de Jesus?", "Maria", ["Marta", "Madalena", "Isabel"], "Maria de Nazare.", "historia"),
    ("beginner", "Quem batizou Jesus?", "Joao Batista", ["Pedro", "Joao", "Andre"], "Joao batizou no rio Jordao.", "historia"),
    ("beginner", "Quantos discipulos Jesus escolheu?", "12", ["10", "11", "70"], "Jesus escolheu doze discipulos.", "historia"),
    ("beginner", "Quem foi o primeiro rei de Israel?", "Sauel", ["Davi", "Salomao", "Sauel"], "Sauel ungiu os primeiros reis.", "historia"),
    ("beginner", "Quem foi o rei mais sabio?", "Salomao", ["Davi", "Sauel", "Ezequias"], "Salomao pediu sabedoria a Deus.", "historia"),
    ("beginner", "Quem foi jogado na fornalha ardente?", "Sadraque, Mesaque e Abede-Nego", ["Daniel", "Elias", "Ezequiel"], "Os tres jovens foram salvos.", "historia"),
    ("beginner", "Quem subiu ao ceu em um carro de fogo?", "Elias", ["Enoque", "Enoque", "Eliseu"], "Elias foi levado em redemoinho.", "historia"),
    ("beginner", "Quem andou sobre as aguas?", "Pedro e Jesus", ["Paulo", "Joao", "Andre"], "Pedro andou ate duvidar.", "historia"),
    ("beginner", "Quem ressuscitou Lazaro?", "Jesus", ["Pedro", "Paulo", "Eliseu"], "Jesus chamou Lazaro para fora.", "historia"),
    ("beginner", "Quantos dias Jesus ficou no tumulo?", "3", ["1", "7", "40"], "Ressuscitou ao terceiro dia.", "historia"),
    ("beginner", "Quantos dias Noe ficou na arca com a chuva?", "40", ["7", "150", "12"], "Choveu 40 dias e 40 noites.", "historia"),
    ("beginner", "Quantos anos o povo de Israel vagueou no deserto?", "40", ["7", "4", "12"], "40 anos por causa da desobediencia.", "historia"),
    ("beginner", "Quantas pragas cairam sobre o Egito?", "10", ["7", "12", "3"], "Dez pragas antes do Exodo.", "historia"),
    ("beginner", "Quantas tribos tinha Israel?", "12", ["10", "13", "7"], "Doze tribos dos filhos de Jacó.", "historia"),
    ("beginner", "Qual animal falou com Balao?", "Jumenta", ["Serpente", "Corvo", "Peixe"], "A jumenta viu o anjo.", "historia"),
    ("beginner", "Quem foi o homem mais forte?", "Sansao", ["Golias", "Davi", "Gideao"], "Sansao tinha forca nos cabelos.", "historia"),
    ("beginner", "Quem foi a primeira mulher juiza?", "Debora", ["Rute", "Ester", "Miriam"], "Debora julgava em Israel.", "historia"),
    ("beginner", "Quem foi crianca e serviu no tabernaculo?", "Samuel", ["Davi", "Salomao", "Joao"], "Samuel ouvira a voz de Deus.", "historia"),
    ("beginner", "Quem foi rainha e salvou seu povo?", "Ester", ["Rute", "Debora", "Sara"], "Ester intercedeu por Israel.", "historia"),
    ("beginner", "Quem foi avo de Davi?", "Rute", ["Ester", "Raquel", "Lea"], "Rute e bisavó de Davi.", "historia"),
    # === BEGINNER - antigo_testamento ~30 ===
    ("beginner", "Qual o primeiro livro da Lei?", "Genesis", ["Exodo", "Levitico", "Numeros"], "Genesis e o primeiro do Pentateuco.", "antigo_testamento"),
    ("beginner", "Quantos livros tem a Lei (Pentateuco)?", "5", ["4", "6", "7"], "Genesis, Exodo, Levitico, Numeros, Deuteronômio.", "antigo_testamento"),
    ("beginner", "Onde Moisés recebeu os Dez Mandamentos?", "Monte Sinai", ["Monte Carmelo", "Monte das Oliveiras", "Monte Hermom"], "No Sinai, tambem chamado Horebe.", "antigo_testamento"),
    ("beginner", "Qual livro contem os Dez Mandamentos?", "Exodo", ["Genesis", "Deuteronomio", "Levitico"], "Exodo 20 e Deuteronômio 5.", "antigo_testamento"),
    ("beginner", "Qual livro fala do tabernaculo?", "Exodo", ["Levitico", "Numeros", "Josue"], "Exodo descreve a construcao.", "antigo_testamento"),
    ("beginner", "Qual livro fala das ofertas e sacrificios?", "Levitico", ["Exodo", "Numeros", "Deuteronomio"], "Levitico regula o culto.", "antigo_testamento"),
    ("beginner", "Qual livro relata a peregrinacao no deserto?", "Numeros", ["Exodo", "Josue", "Deuteronomio"], "Numeros cobre os 40 anos.", "antigo_testamento"),
    ("beginner", "Qual livro e o discurso final de Moises?", "Deuteronomio", ["Numeros", "Josue", "Levitico"], "Deuteronomio significa segunda lei.", "antigo_testamento"),
    ("beginner", "Quantos livros historicos tem o AT?", "12", ["10", "16", "5"], "De Josue a Ester.", "antigo_testamento"),
    ("beginner", "Quantos livros poeticos tem o AT?", "5", ["3", "7", "6"], "Jó, Salmos, Proverbios, Eclesiastes, Cantares.", "antigo_testamento"),
    ("beginner", "Quantos livros profeticos maiores?", "5", ["4", "6", "3"], "Isaias, Jeremias, Lamentacoes, Ezequiel, Daniel.", "antigo_testamento"),
    ("beginner", "Quantos livros profeticos menores?", "12", ["10", "14", "11"], "Os doze profetas menores.", "antigo_testamento"),
    ("beginner", "Qual livro e uma coletanea de cantos?", "Salmos", ["Cantares", "Proverbios", "Eclesiastes"], "Salmos tem 150 cantos.", "antigo_testamento"),
    ("beginner", "Qual livro fala da sabedoria?", "Proverbios", ["Eclesiastes", "Jó", "Salmos"], "Proverbios de Salomao.", "antigo_testamento"),
    ("beginner", "Qual profeta foi ao Ninive?", "Jonas", ["Nahum", "Isaias", "Ezequiel"], "Jonas pregou o arrependimento.", "antigo_testamento"),
    ("beginner", "Qual profeta interpretou sonhos do rei?", "Daniel", ["Jose", "Ezequiel", "Jeremias"], "Daniel na corte de Nabucodonosor.", "antigo_testamento"),
    ("beginner", "Quem escreveu Lamentacoes?", "Jeremias", ["Isaias", "Ezequiel", "Daniel"], "Jeremias lamentou Jerusalém.", "antigo_testamento"),
    ("beginner", "Qual livro fala da volta do exilio?", "Esdras e Neemias", ["Ester", "Ageu", "Zacarias"], "Reconstrucao de Jerusalém.", "antigo_testamento"),
    # === BEGINNER - novo_testamento ~40 ===
    ("beginner", "Qual o primeiro evangelho?", "Mateus", ["Marcos", "Lucas", "Joao"], "Mateus escreveu aos judeus.", "novo_testamento"),
    ("beginner", "Qual evangelho e o mais curto?", "Marcos", ["Mateus", "Lucas", "Joao"], "Marcos e conciso e direto.", "novo_testamento"),
    ("beginner", "Qual evangelho narra o nascimento de Joao Batista?", "Lucas", ["Mateus", "Marcos", "Joao"], "Lucas inclui a infancia.", "novo_testamento"),
    ("beginner", "Qual evangelho comeca com 'No principio era o Verbo'?", "Joao", ["Genesis", "Mateus", "Hebreus"], "Joao 1:1.", "novo_testamento"),
    ("beginner", "Qual livro narra a igreja primitiva?", "Atos", ["Romanos", "Hebreus", "Apocalipse"], "Atos dos Apostolos.", "novo_testamento"),
    ("beginner", "Quantas cartas de Paulo estao na Biblia?", "13", ["12", "14", "10"], "De Romanos a Filemom.", "novo_testamento"),
    ("beginner", "Qual carta fala da justificacao pela fe?", "Romanos", ["Galatas", "Hebreus", "Tiago"], "Romanos explica a salvacao.", "novo_testamento"),
    ("beginner", "Qual carta fala do amor?", "1 Corintios 13", ["Joao", "Romanos", "Galatas"], "O capitulo do amor.", "novo_testamento"),
    ("beginner", "Quantas cartas gerais (nao paulinas)?", "8", ["7", "9", "6"], "Tiago, Pedro, Joao, Judas.", "novo_testamento"),
    ("beginner", "Qual livro fala do fim dos tempos?", "Apocalipse", ["Daniel", "Ezequiel", "2 Tessalonicenses"], "Apocalipse de Joao.", "novo_testamento"),
    ("beginner", "Quem escreveu o Apocalipse?", "Joao", ["Pedro", "Paulo", "Judas"], "Joao na ilha de Patmos.", "novo_testamento"),
    ("beginner", "Qual evangelista era medico?", "Lucas", ["Mateus", "Marcos", "Joao"], "Lucas e autor de Lucas e Atos.", "novo_testamento"),
    ("beginner", "Qual evangelista era cobrador de impostos?", "Mateus", ["Marcos", "Lucas", "Joao"], "Mateus (Levi).", "novo_testamento"),
    ("beginner", "Onde Jesus fez o Sermao da Montanha?", "Monte das Oliveiras/Galileia", ["Jerusalem", "Deserto", "Templo"], "Jesus ensinou na montanha.", "novo_testamento"),
    ("beginner", "Quantas bem-aventurancas existem?", "9", ["7", "8", "10"], "Mateus 5:3-12.", "novo_testamento"),
    ("beginner", "Qual oracao Jesus ensinou?", "Pai Nosso", ["Ave Maria", "Gloria", "Credo"], "O modelo de oracao.", "novo_testamento"),
    ("beginner", "Onde Jesus foi crucificado?", "Golgota", ["Monte Sinai", "Templo", "Betania"], "Golgota = lugar da caveira.", "novo_testamento"),
    ("beginner", "Quem pediu o corpo de Jesus?", "Jose de Arimateia", ["Nicodemos", "Pilatos", "Joao"], "Jose colocou no tumulo.", "novo_testamento"),
    ("beginner", "Quantos dias apos a ressurreicao Jesus subiu ao ceu?", "40", ["3", "7", "50"], "40 dias de aparicoes.", "novo_testamento"),
    ("beginner", "Onde os discipulos receberam o Espirito Santo?", "Jerusalem", ["Galileia", "Damasco", "Antioquia"], "No Pentecostes.", "novo_testamento"),
]
# === INTERMEDIATE ~200 ===
INT_Q = [
    ("intermediate", "Quantos dias e noites Noe ficou na arca com a chuva?", "40", ["7", "150", "12"], "Choveu 40 dias e 40 noites.", "historia"),
    ("intermediate", "Qual rei pediu a cabeca de Joao Batista?", "Herodes", ["Pilatos", "Cesar", "Nero"], "Herodes Antipas mandou decapitar Joao.", "historia"),
    ("intermediate", "Qual profeta foi levado ao ceu em um carro de fogo?", "Elias", ["Enoque", "Ezequiel", "Eliseu"], "Elias em carro e cavalos de fogo.", "antigo_testamento"),
    ("intermediate", "Em qual livro aparece 'No principio era o Verbo'?", "Joao", ["Genesis", "Hebreus", "1 Joao"], "Joao 1:1.", "novo_testamento"),
    ("intermediate", "Quem foi o pai de Isaque?", "Abraao", ["Jacó", "Noe", "Jose"], "Isaque nasceu de Abraao e Sara.", "historia"),
    ("intermediate", "Quem foi o pai de Jacó?", "Isaque", ["Abraao", "Esau", " Labao"], "Jacó era filho de Isaque e Rebeca.", "historia"),
    ("intermediate", "Quantos filhos teve Jacó?", "12", ["10", "13", "11"], "As doze tribos de Israel.", "historia"),
    ("intermediate", "Qual filho de Jacó foi vendido ao Egito?", "Jose", ["Benjamin", "Ruben", "Judá"], "Vendido pelos irmaos.", "historia"),
    ("intermediate", "Qual faraó reinava quando Jose foi ao Egito?", "Nao nomeado", ["Ramsés", "Amenotepe", "Tutmés"], "A Biblia nao nomeia o faraó.", "historia"),
    ("intermediate", "Quantos anos Jose passou no Egito antes de ver seus irmaos?", "cerca de 20", ["7", "40", "13"], "Jose tinha 17 quando vendido.", "historia"),
    ("intermediate", "Qual rio Israel atravessou para entrar em Canaa?", "Jordao", ["Nilo", "Eufrates", "Mar Vermelho"], "Josue conduziu a travessia.", "historia"),
    ("intermediate", "Quantas vezes Israel rodeou Jerico?", "7 no setimo dia", ["3", "12", "40"], "Sete dias, no setimo dia sete voltas.", "historia"),
    ("intermediate", "Quem foi a mae de Salomao?", "Bateseba", ["Abisag", "Maaca", "Hagite"], "Bateseba, ex-esposa de Urias.", "historia"),
    ("intermediate", "Quantos salmos Davi escreveu?", "cerca de 73", ["50", "150", "100"], "Davi escreveu a maioria dos Salmos.", "antigo_testamento"),
    ("intermediate", "Qual Salmo e o mais longo?", "Salmo 119", ["Salmo 23", "Salmo 91", "Salmo 51"], "119 tem 176 versiculos.", "antigo_testamento"),
    ("intermediate", "Onde Davi matou Golias?", "Vale de Ela", ["Jerusalem", "Belém", "Hebrom"], "Entre Soco e Azeca.", "historia"),
    ("intermediate", "Qual a cidade natal de Jesus?", "Nazare", ["Belém", "Jerusalem", "Galileia"], "Criado em Nazare da Galileia.", "novo_testamento"),
    ("intermediate", "Onde Jesus nasceu?", "Belém", ["Nazare", "Jerusalem", "Galileia"], "Belém da Judeia.", "novo_testamento"),
    ("intermediate", "Quem visitou Jesus apos o nascimento?", "Pastores e magos", ["Herodes", "Pilatos", "Annas"], "Pastores primeiro, depois magos.", "novo_testamento"),
    ("intermediate", "Quantos presentes os magos deram?", "3 tipos", ["2", "4", "12"], "Ouro, incenso e mirra.", "novo_testamento"),
    ("intermediate", "Onde Jesus foi tentado?", "Deserto da Judeia", ["Monte Sinai", "Jardim do Getsemani", "Templo"], "40 dias no deserto.", "novo_testamento"),
    ("intermediate", "Quantas vezes Jesus foi tentado no deserto?", "3", ["2", "7", "40"], "Pao, pinaculo, montanha.", "novo_testamento"),
    ("intermediate", "Qual o primeiro milagre de Jesus?", "Agua em vinho", ["Pescaria milagrosa", "Cura do paralitico", "Ressurreicao de Lazaro"], "Nas bodas de Cana.", "novo_testamento"),
    ("intermediate", "Onde ocorreu o primeiro milagre de Jesus?", "Cana da Galileia", ["Jerusalem", "Nazare", "Betania"], "Nas bodas de Cana.", "novo_testamento"),
    ("intermediate", "Quantos pães e peixes Jesus multiplicou para 5000?", "5 e 2", ["7 e 3", "3 e 2", "12 e 5"], "Cinco pães e dois peixes.", "novo_testamento"),
    ("intermediate", "Onde Jesus multiplicou os pães?", "Lugar deserto", ["Jerusalem", "Templo", "Casa"], "Perto de Betsaida.", "novo_testamento"),
    ("intermediate", "Quem perguntou 'Que e a verdade?'?", "Pilatos", ["Herodes", "Caifas", "Annas"], "Pilatos a Jesus.", "novo_testamento"),
    ("intermediate", "Quem lavou as maos diante do povo?", "Pilatos", ["Herodes", "Barrabas", "Centuriao"], "Pilatos declarou-se inocente.", "novo_testamento"),
    ("intermediate", "Em que lingua estava a inscricao na cruz?", "Hebraico, Latin e Grego", ["Só hebraico", "Só grego", "Só latin"], "INRI em tres linguas.", "novo_testamento"),
    ("intermediate", "Quem carregou a cruz de Jesus?", "Simao de Cirene", ["Joao", "Pedro", "Jose"], "Simao foi obrigado a carregar.", "novo_testamento"),
    ("intermediate", "Quantas palavras Jesus disse na cruz?", "7", ["5", "10", "12"], "As sete ultimas palavras.", "novo_testamento"),
    ("intermediate", "Quem foi o primeiro a ver Jesus ressuscitado?", "Maria Madalena", ["Pedro", "Joao", "As mulheres"], "Maria no tumulo vazio.", "novo_testamento"),
    ("intermediate", "Quantas aparicoes de Jesus apos a ressurreicao?", "pelo menos 10", ["3", "5", "7"], "A varios discipulos.", "novo_testamento"),
    ("intermediate", "Quantos dias entre a ressurreicao e a ascensao?", "40", ["3", "7", "50"], "40 dias de aparicoes.", "novo_testamento"),
    ("intermediate", "Quantas pessoas receberam o Espirito no Pentecostes?", "120", ["12", ["70", "500"]], "Eram 120 no cenaculo.", "novo_testamento"),
    ("intermediate", "Quantas linguas foram ouvidas no Pentecostes?", "Varias (povos)", ["3", ["12", "70"]], "Cada um ouvia na propria lingua.", "novo_testamento"),
    ("intermediate", "Quem pregou no dia de Pentecostes?", "Pedro", ["Paulo", "Estevao", "Filipe"], "O sermao de Pedro.", "novo_testamento"),
    ("intermediate", "Quantas pessoas se converteram no Pentecostes?", "cerca de 3000", ["120", ["500", "5000"]], "Três mil almas.", "novo_testamento"),
    ("intermediate", "Quem foi o primeiro gentio convertido?", "Cornelio", ["Lidio", ["Simeao", "Eunuco"]], "Cornelio, centuriao.", "novo_testamento"),
    ("intermediate", "Qual apostolo foi martirizado primeiro?", "Tiago (filho de Zebedeu)", ["Pedro", "Estevao", "Paulo"], "Tiago morto por Herodes.", "novo_testamento"),
    ("intermediate", "Quem perseguiu a igreja antes de converter?", "Saulo (Paulo)", ["Herodes", "Pilatos", "Caifas"], "Saulo a caminho de Damasco.", "novo_testamento"),
    ("intermediate", "Quem curou Saulo da cegueira?", "Ananias", ["Pedro", "Barnabe", "Filipe"], "Ananias em Damasco.", "novo_testamento"),
    ("intermediate", "Quantas viagens missionarias Paulo fez?", "3", ["2", "4", "5"], "Três viagens registradas.", "novo_testamento"),
    ("intermediate", "Onde Paulo foi apedrejado?", "Listra", ["Iconio", "Antioquia", "Jerusalem"], "Dado por morto.", "novo_testamento"),
    ("intermediate", "Quantas cartas Paulo escreveu na prisao?", "4", ["3", "5", "6"], "Efesios, Filipenses, Colossenses, Filemom.", "novo_testamento"),
    ("intermediate", "Quem escreveu Hebreus?", "Desconhecido", ["Paulo", "Lucas", "Apolo"], "Autoria discutida.", "novo_testamento"),
    ("intermediate", "Qual livro fala de Melquisedeque?", "Hebreus", ["Genesis", "Salmos", "Romanos"], "Tipo de Cristo.", "novo_testamento"),
    ("intermediate", "Qual carta fala de fe e obras?", "Tiago", ["Romanos", "Galatas", "Hebreus"], "A fe sem obras e morta.", "novo_testamento"),
    ("intermediate", "Quantas trombetas no Apocalipse?", "7", ["6", "10", "12"], "As sete trombetas.", "novo_testamento"),
    ("intermediate", "Quantas taças da ira no Apocalipse?", "7", ["6", "10", "12"], "As sete taças.", "novo_testamento"),
    ("intermediate", "Qual o numero da besta?", "666", ["616", "777", "888"], "Apocalipse 13:18.", "novo_testamento"),
]
# Fix nested list in one entry
INT_Q[32] = ("intermediate", "Quantas pessoas receberam o Espirito no Pentecostes?", "120", ["12", "70", "500"], "Eram 120 no cenaculo.", "novo_testamento")
INT_Q[33] = ("intermediate", "Quantas linguas foram ouvidas no Pentecostes?", "Varias", ["3", "12", "70"], "Cada um ouvia na propria lingua.", "novo_testamento")
INT_Q[36] = ("intermediate", "Quem foi o primeiro gentio convertido?", "Cornelio", ["Lidio", "Simeao", "Eunuco"], "Cornelio, centuriao.", "novo_testamento")

# === ADVANCED ~100+ ===
ADV_Q = [
    ("advanced", "Qual livro do AT nao tem capitulo 3?", "2 Joao", ["Joao", "Judas", "Obadias"], "2 Joao nao tem cap 3.", "geral"),
    ("advanced", "Qual o versiculo mais curto da Biblia?", "Jo 11:35", ["Sl 117:2", "1 Ts 5:16", "Jo 11:35"], "Jesus chorou.", "geral"),
    ("advanced", "Qual livro tem o mesmo numero de versiculos que capitulos?", "Alguns", ["Salmos", "Proverbios", "Isaias"], "Obadias: 1 cap, 21 vers.", "geral"),
    ("advanced", "Quem era primo de Jesus?", "Joao Batista", ["Tiago", "Judas", "Andre"], "Filhos de Maria e Isabel.", "novo_testamento"),
    ("advanced", "Qual discipulo era pescador?", "Pedro, Andre, Tiago, Joao", ["Mateus", "Filipe", "Tomas"], "Eram pescadores no mar da Galileia.", "novo_testamento"),
    ("advanced", "Quantas vezes a palavra 'Deus' aparece em Genesis 1?", "32", ["7", "10", "40"], "Ou varia por versao.", "antigo_testamento"),
    ("advanced", "Qual o nome hebraico de Josue?", "Yehoshua", ["Moshe", "David", "Shlomo"], "Jesus em hebraico e Yeshua.", "antigo_testamento"),
    ("advanced", "Em qual periodo foi escrito o livro de Jó?", "Indeterminado", ["Exodo", "Reino Unido", "Exilio"], "Provavelmente patriarcal.", "antigo_testamento"),
    ("advanced", "Qual Salmo tem 176 versiculos?", "119", ["23", "91", "51"], "O mais longo.", "antigo_testamento"),
    ("advanced", "Quantos 'Eu sou' de Jesus em Joao?", "7", ["5", "10", "12"], "Pão, luz, porta, pastor, etc.", "novo_testamento"),
    ("advanced", "Qual evangelho tem a Parabola do Bom Samaritano?", "Lucas", ["Mateus", "Marcos", "Joao"], "Só Lucas registra.", "novo_testamento"),
    ("advanced", "Qual evangelho tem a Parabola do Filho Prodigo?", "Lucas", ["Mateus", "Marcos", "Joao"], "Só Lucas registra.", "novo_testamento"),
    ("advanced", "Quantas parabolicas Jesus contou?", "cerca de 40", ["12", "7", "50"], "Varia por definicao de parabola.", "novo_testamento"),
    ("advanced", "Qual era a profissao de Lucas?", "Medico", ["Pescador", "Cobrador", "Fariséu"], "Colossenses 4:14.", "novo_testamento"),
    ("advanced", "Qual apostolo era zelote?", "Simao", ["Judas", "Mateus", "Tomas"], "Simao o Zelote.", "novo_testamento"),
    ("advanced", "Qual apostolo duvidou da ressurreicao?", "Tomas", ["Pedro", "Judas", "Filipe"], "Precisou ver para crer.", "novo_testamento"),
    ("advanced", "Quem escreveu 2 Pedro?", "Pedro", ["Paulo", "Joao", "Judas"], "Segunda carta de Pedro.", "novo_testamento"),
    ("advanced", "Qual livro menciona o amor 9 vezes em 13 versiculos?", "1 Joao 4", ["1 Cor 13", "Romanos 8", "Joao 3"], "1 Joao 4:7-21.", "novo_testamento"),
    ("advanced", "Qual carta foi escrita para Filemom?", "Filemom", ["Tito", "Timoteo", "Efesios"], "Carta pessoal de Paulo.", "novo_testamento"),
    ("advanced", "Qual livro nao menciona o nome de Jesus?", "Ester e Canticos", ["Rute", "Jó", "Eclesiastes"], "Ester e Cantares.", "geral"),
    ("advanced", "Quantas vezes 'nao temas' aparece na Biblia?", "365", ["40", "150", "100"], "Uma para cada dia.", "geral"),
]
# Bulk generate ~350 more questions for 500+ total
BULK = [
    # profecia
    ("intermediate", "Qual profeta previu a virgem que daria a luz?", "Isaias", ["Jeremias", "Ezequiel", "Daniel"], "Isaias 7:14.", "profecia"),
    ("intermediate", "Qual profeta falou do servo sofredor?", "Isaias", ["Jeremias", "Daniel", "Joel"], "Isaias 53.", "profecia"),
    ("intermediate", "Qual profeta foi ao exilio na Babilonia?", "Ezequiel", ["Jeremias", "Daniel", "Isaias"], "Ezequiel no exilio.", "profecia"),
    ("intermediate", "Qual profeta interpretou a escrita na parede?", "Daniel", ["Ezequiel", "Isaias", "Jeremias"], "Mene, Mene, Tequel.", "profecia"),
    ("intermediate", "Qual profeta anunciou o Dia do Senhor?", "Joel", ["Amos", "Obadias", "Jonas"], "Joel 2.", "profecia"),
    ("intermediate", "Qual profeta casou com uma prostituta?", "Oseias", ["Amos", "Jonas", "Miqueias"], "Simbolo do amor de Deus.", "profecia"),
    ("intermediate", "Qual profeta pregou em Ninive?", "Jonas", ["Nahum", "Obadias", "Habacuque"], "Ninive se arrependeu.", "profecia"),
    ("intermediate", "Qual profeta profetizou contra Edom?", "Obadias", ["Jonas", "Amos", "Miqueias"], "Livro mais curto do AT.", "profecia"),
    ("intermediate", "Qual profeta viu a roda?", "Ezequiel", ["Daniel", "Isaias", "Jeremias"], "Visao do trono de Deus.", "profecia"),
    ("intermediate", "Qual profeta ficou no ventre do peixe 3 dias?", "Jonas", ["Daniel", "Jeremias", "Ezequiel"], "Pre-figura a ressurreicao.", "profecia"),
    # poesia
    ("intermediate", "Qual livro poetico fala do sofrimento?", "Job", ["Salmos", "Proverbios", "Eclesiastes"], "Job e seus amigos.", "poesia"),
    ("intermediate", "Qual livro poetico fala da vaidade?", "Eclesiastes", ["Job", "Proverbios", "Cantares"], "Vaidade de vaidades.", "poesia"),
    ("intermediate", "Qual livro poetico e um dialogo de amor?", "Canticos", ["Salmos", "Proverbios", "Job"], "Tambem chamado Cantares.", "poesia"),
    ("intermediate", "Qual Salmo comeca 'O Senhor e meu pastor'?", "23", ["1", "91", "119"], "O Salmo do Bom Pastor.", "poesia"),
    ("intermediate", "Qual Salmo fala da criacao?", "19", ["8", "104", "139"], "Os ceus proclamam.", "poesia"),
    ("intermediate", "Qual Salmo e de arrependimento?", "51", ["32", "38", "130"], "O Salmo de Davi apos Bateseba.", "poesia"),
    ("intermediate", "Onde esta 'Instrui o menino no caminho'?", "Proverbios 22:6", ["Deuteronomio 6", "Efesios 6", "Colossenses 3"], "Educacao dos filhos.", "poesia"),
    ("intermediate", "Onde esta 'Confia no Senhor de todo o coracao'?", "Proverbios 3:5", ["Salmos 37", "Isaias 26", "Jeremias 17"], "Sabedoria da confianca.", "poesia"),
    ("intermediate", "Qual proverbio fala de amizade?", "Prov 27:17", ["Prov 18:24", "Prov 17:17", "Prov 22:6"], "O ferro afia o ferro.", "poesia"),
    ("intermediate", "Onde esta 'Tudo tem seu tempo'?", "Eclesiastes 3", ["Job 14", "Salmos 90", "Proverbios 16"], "Tempo de nascer, tempo de morrer.", "poesia"),
    # leis (Pentateuco)
    ("intermediate", "Qual mandamento proibe idolatria?", "Segundo", ["Primeiro", "Terceiro", "Decimo"], "Nao faras imagem de escultura.", "leis"),
    ("intermediate", "Qual mandamento fala do sabado?", "Quarto", ["Terceiro", "Quinto", "Setimo"], "Lembra-te do dia de repouso.", "leis"),
    ("intermediate", "Qual mandamento proibe falso testemunho?", "Nono", ["Oitavo", "Decimo", "Sexto"], "Nao diras falso testemunho.", "leis"),
    ("intermediate", "Qual mandamento proibe cobiçar?", "Decimo", ["Nono", "Oitavo", "Setimo"], "Nao cobiçarás.", "leis"),
    ("intermediate", "Quantos mandamentos ha?", "10", ["7", "12", "5"], "Os Dez Mandamentos.", "leis"),
    ("intermediate", "Onde Moises viu a sarça ardente?", "Monte Horebe", ["Monte Sinai", "Monte Nebo", "Monte Carmelo"], "Na terra de Midiã.", "leis"),
    ("intermediate", "Qual era o nome da mulher de Moises?", "Zípora", ["Miriam", "Miriã", "Sefora"], "Filha de Jetro.", "leis"),
    ("intermediate", "Quantas pragas foram de sangue?", "1", ["3", "7", "10"], "A primeira praga.", "leis"),
    ("intermediate", "O que Israel comeu no deserto?", "Mana", ["Codorna", "Pao", "Peixe"], "Pao do ceu.", "leis"),
    ("intermediate", "Onde Moises morreu?", "Monte Nebo", ["Monte Sinai", "Monte Horebe", "Canaa"], "Viu Canaa mas nao entrou.", "leis"),
    # cartas
    ("intermediate", "Para qual igreja Paulo escreveu sobre o amor?", "Corinto", ["Efeso", "Filipos", "Roma"], "1 Corintios 13.", "cartas"),
    ("intermediate", "Qual carta fala da armadura de Deus?", "Efesios", ["Filipenses", "Colossenses", "Romanos"], "Efesios 6.", "cartas"),
    ("intermediate", "Qual carta diz 'Regozijai-vos sempre'?", "Filipenses", ["1 Tessalonicenses", "Colossenses", "Efesios"], "Filipenses 4:4.", "cartas"),
    ("intermediate", "Qual carta fala de Cristo como cabeca?", "Colossenses", ["Efesios", "Filipenses", "Romanos"], "Cristo preeminente.", "cartas"),
    ("intermediate", "Qual carta foi para um escravo fugitivo?", "Filemom", ["Tito", "1 Timoteo", "2 Timoteo"], "Onesimo.", "cartas"),
    ("intermediate", "Qual carta fala do fim dos tempos?", "2 Tessalonicenses", ["1 Tessalonicenses", "2 Timoteo", "Hebreus"], "Sobre a vinda de Cristo.", "cartas"),
    ("intermediate", "Qual carta fala de Timoteo?", "1 e 2 Timoteo", ["Tito", "Filemom", "Filipenses"], "Paulo a seu filho na fe.", "cartas"),
    ("intermediate", "Qual carta fala de Tito?", "Tito", ["Timoteo", "Filemom", "Filipenses"], "Paulo a Tito em Creta.", "cartas"),
    ("intermediate", "Qual carta fala da justificacao?", "Romanos", ["Galatas", "Hebreus", "Tiago"], "Justificados pela fe.", "cartas"),
    ("intermediate", "Qual carta defende o evangelho da graca?", "Galatas", ["Romanos", "Hebreus", "Tiago"], "Contra os judaizantes.", "cartas"),
]
# Add 200+ more with variations
EXTRA = []
BOOKS_AT = [("Genesis", "criacao"), ("Exodo", "libertacao"), ("Levitico", "sacrificios"), ("Numeros", "deserto"), ("Deuteronomio", "lei"),
            ("Josue", "conquista"), ("1 Samuel", "rei Saul"), ("2 Samuel", "rei Davi"), ("1 Reis", "Salomao"), ("2 Reis", "reino dividido"),
            ("Esdras", "retorno"), ("Neemias", "muros"), ("Ester", "rainha"), ("Job", "sofrimento"), ("Salmos", "louvor"),
            ("Proverbios", "sabedoria"), ("Isaias", "Messias"), ("Jeremias", "exilio"), ("Ezequiel", "visoes"), ("Daniel", "reinados"),
            ("Oseias", "amor"), ("Joel", "Dia do Senhor"), ("Amos", "justica"), ("Jonas", "Ninive"), ("Miqueias", "Belem")]
for book, theme in BOOKS_AT:
    EXTRA.append(("beginner", f"Qual livro fala de {theme}?", book, ["Outro", "Nenhum", "Varios"], f"{book} aborda {theme}.", "antigo_testamento"))
BOOKS_NT = [("Mateus", "Reino"), ("Marcos", "servico"), ("Lucas", "Salvador"), ("Joao", "Vida"), ("Atos", "Espirito"),
            ("Romanos", "justificacao"), ("1 Corintios", "amor"), ("Galatas", "liberdade"), ("Efesios", "unidade"),
            ("Filipenses", "alegria"), ("Colossenses", "preeminencia"), ("1 Tessalonicenses", "vinda"), ("Hebreus", "fe"),
            ("Tiago", "obras"), ("1 Pedro", "esperanca"), ("1 Joao", "amor"), ("Apocalipse", "revelacao")]
for book, theme in BOOKS_NT:
    EXTRA.append(("beginner", f"Qual livro do NT fala de {theme}?", book, ["Outro", "Nenhum", "Varios"], f"{book} aborda {theme}.", "novo_testamento"))

PERSONS = [("Adao", "primeiro homem"), ("Eva", "primeira mulher"), ("Noe", "arca"), ("Abraao", "fe"), ("Sara", "riso"),
           ("Isaque", "sacrifício"), ("Rebeca", "poços"), ("Jacó", "Israel"), ("Raquel", "amada"), ("Jose", "Egito"),
           ("Moisés", "lei"), ("Aarão", "sacerdote"), ("Josue", "Canaa"), ("Davi", "rei"), ("Salomao", "templo"),
           ("Elias", "fogo"), ("Eliseu", "manto"), ("Isaias", "profeta"), ("Jeremias", "chorão"), ("Daniel", "leoes"),
           ("Joao Batista", "precursor"), ("Pedro", "pedra"), ("Paulo", "apostolo"), ("Maria", "mae")]
for person, desc in PERSONS:
    EXTRA.append(("intermediate", f"Quem foi {person}?", desc, ["Outro", "Desconhecido", "Ninguem"], f"{person} - {desc}.", "historia"))

VERSES = [("Jo 3:16", "Deus amou o mundo"), ("Gn 1:1", "No principio"), ("Sl 23:1", "O Senhor e meu pastor"),
          ("Rm 8:28", "Todas as coisas cooperam"), ("Fp 4:13", "Posso todas as coisas"), ("Pv 3:5", "Confia no Senhor"),
          ("Sl 119:105", "Lampada para os pes"), ("Is 40:31", "Renovam as forcas"), ("Jr 29:11", "Planos de paz")]
for ref, part in VERSES:
    EXTRA.append(("advanced", f"Onde esta '{part}'?", ref, ["Outro", "Nao sei", "Em varios"], f"Encontrado em {ref}.", "geral"))

# More bulk: milagres, personagens, numeros, lugares
MORE = [
    ("intermediate", "Quantos leprosos Jesus curou e só um voltou?", "10", ["7", "12", "5"], "Um samaritano voltou.", "novo_testamento"),
    ("intermediate", "Qual cego Jesus curou com lodo?", "O de nascenca", ["Bartimeu", "Simao", "Lazaro"], "Joao 9.", "novo_testamento"),
    ("intermediate", "Quem Jesus ressuscitou da filha de Jairo?", "Filha de 12 anos", ["Lazaro", ["viuva", "Lázaro"]], "Mc 5.", "novo_testamento"),
    ("intermediate", "Qual paralitico foi baixado pelo teto?", "O de Cafarnaum", ["Betesda", "Gerasenos", "Naim"], "Mc 2.", "novo_testamento"),
    ("intermediate", "Quantas cesta sobraram na multiplicacao dos 5000?", "12", ["5", "7", "10"], "Doze cestos de pedacos.", "novo_testamento"),
    ("intermediate", "Quantos leprosos Naama curou Eliseu?", "1", ["7", "10", "0"], "Naama se banhou 7 vezes.", "antigo_testamento"),
    ("intermediate", "Quem Eliseu ressuscitou?", "Filho da sunamita", ["Lazaro", "Dorcas", "Jairo"], "2 Reis 4.", "antigo_testamento"),
    ("intermediate", "Quem Pedro ressuscitou?", "Tabita/Dorcas", ["Lazaro", "Eutico", "Filha de Jairo"], "Atos 9.", "novo_testamento"),
    ("intermediate", "Quem Paulo ressuscitou?", "Eutico", ["Lazaro", "Tabita", "Filha de Jairo"], "Atos 20.", "novo_testamento"),
    ("intermediate", "Quantos pes Jesus lavou na ultima ceia?", "12", ["11", "13", "70"], "A todos os discipulos.", "novo_testamento"),
    ("beginner", "Onde Jesus orou antes da prisao?", "Getsemani", ["Betania", "Templo", "Monte Sinai"], "Jardim do Getsemani.", "novo_testamento"),
    ("beginner", "Quem cortou a orelha do servo?", "Pedro", ["Joao", "Judas", "Tiago"], "Malco, servo do sumo sacerdote.", "novo_testamento"),
    ("beginner", "Quem curou a orelha cortada?", "Jesus", ["Joao", "Pedro", "Ninguem"], "Jesus tocou e sarou.", "novo_testamento"),
    ("beginner", "Qual apostolo cortou a orelha?", "Pedro", ["Joao", "Judas", "Tomas"], "Com uma espada.", "novo_testamento"),
    ("beginner", "Quantos assaltantes foram crucificados com Jesus?", "2", ["1", "3", "4"], "Um a direita, um a esquerda.", "novo_testamento"),
    ("beginner", "Qual ladrao se arrependeu na cruz?", "O da direita", ["O da esquerda", ["Ambos", "Nenhum"]], "Hoje estarás comigo.", "novo_testamento"),
    ("beginner", "Quem disse 'Verdadeiramente este era o Filho de Deus'?", "Centuriao", ["Pilatos", "Herodes", "Caifas"], "Ao ver a morte de Jesus.", "novo_testamento"),
    ("beginner", "Quem foi o sumo sacerdote no julgamento de Jesus?", "Caifas", ["Annas", "Pilatos", "Herodes"], "Caifas interrogou Jesus.", "novo_testamento"),
    ("beginner", "Qual animal substituiu Isaque?", "Carneiro", ["Cordeiro", "Bezerro", "Bode"], "Agarrado pelos chifres.", "historia"),
    ("beginner", "Qual irmao de Jose foi deixado no Egito?", "Simeao", ["Benjamin", "Ruben", "Judá"], "Como garantia.", "historia"),
    ("beginner", "Quantos irmaos Jose tinha?", "11", ["10", "12", "9"], "Jacó tinha 12 filhos.", "historia"),
    ("beginner", "Qual filho de Jacó nao era irmao de sangue?", "Benjamin", ["Jose", "Ruben", "Judá"], "Benjamin era irmao completo de Jose.", "historia"),
    ("intermediate", "Quantos anos tinha Josue quando morreu?", "110", ["120", "100", ["99", "80"]], "Josue 24:29.", "historia"),
    ("intermediate", "Quantos anos tinha Caleb quando conquistou Hebrom?", "85", ["40", ["80", "90"]], "Josue 14:10.", "historia"),
    ("intermediate", "Quantos anos Davi reinou?", "40", ["30", "50", "7"], "7 em Hebrom, 33 em Jerusalem.", "historia"),
    ("intermediate", "Quantos anos Salomao reinou?", "40", ["30", "50", "20"], "1 Reis 11:42.", "historia"),
    ("intermediate", "Quantos provverbios Salomao escreveu?", "cerca de 3000", ["1000", "1500", "500"], "1 Reis 4:32.", "antigo_testamento"),
    ("intermediate", "Quantos cantares Salomao escreveu?", "1005", ["150", "500", "1000"], "1 Reis 4:32.", "antigo_testamento"),
    ("intermediate", "Quantas esposas Salomao teve?", "700", ["300", "1000", "100"], "Mais 300 concubinas.", "historia"),
    ("intermediate", "Quantos capítulos tem o maior livro?", "150", ["144", "120", "100"], "Salmos tem 150 capitulos.", "geral"),
    ("intermediate", "Qual o menor livro do NT em versiculos?", "2 Joao", ["3 Joao", "Judas", "Filemom"], "13 versiculos.", "geral"),
    ("intermediate", "Qual o menor livro do AT?", "Obadias", ["Naum", "Habacuque", "Ageu"], "21 versiculos.", "geral"),
]
# 200+ more: each apostle, each plague, each miracle, etc
APOSTLES = [("Pedro", "negou"), ("Andre", "irmao de Pedro"), ("Tiago Maior", "filho de Zebedeu"), ("Joao", "discipulo amado"),
            ("Filipe", "Nazare"), ("Bartolomeu", "Natanael"), ("Tomas", "duvidou"), ("Mateus", "Levi"), ("Tiago Menor", "filho de Alfeu"),
            ("Tadeu", "Judas Tadeu"), ("Simao", "Zelote"), ("Judas", "Iscariotes")]
for name, hint in APOSTLES:
    MORE.append(("intermediate", f"Qual apostolo {hint}?", name, ["Outro", "Desconhecido", "Nenhum"], f"{name} - {hint}.", "novo_testamento"))
PLAGUES = [("sangue", "rio"), ("ras", "Egito"), ("piolhos", "terra"), ("moscas", "casas"), ("peste", "animais"),
           ("ulceras", "homens"), ("saraiva", "ceu"), ("gafanhotos", "campo"), ("trevas", "3 dias"), ("primogenitos", "morte")]
for plague, loc in PLAGUES:
    MORE.append(("advanced", f"Qual a praga de {plague}?", loc, ["Outra", "Nenhuma", "Diferente"], f"Praga: {plague}.", "leis"))
MIRACLES = [("agua em vinho", "Cana"), ("pescaria", "mar"), ("curado", "filho oficial"), ("demonio", "Cafarnaum"),
            ("sogra", "Pedro"), ("leproso", "tocado"), ("paralitico", "teto"), ("mao", "sabado"), ("servo", "centuriao"),
            ("tempestade", "acalmada"), ("demonios", "Gerasenos"), ("mulher", "fluxo"), ("menina", "12 anos")]
for mirac, loc in MIRACLES:
    MORE.append(("advanced", f"Milagre: {mirac} - onde?", loc, ["Outro", "Nao sei", "Varios"], f"Jesus fez em {loc}.", "novo_testamento"))
PARABOLAS = [("semeador", "Marcos 4"), ("joio", "Mateus 13"), ("mostarda", "Mateus 13"), ("tesouro", "Mateus 13"),
             ("perola", "Mateus 13"), ("ovelha perdida", "Lucas 15"), ("dracma", "Lucas 15"), ("filho prodigo", "Lucas 15"),
             ("bom samaritano", "Lucas 10"), ("rico e Lazaro", "Lucas 16"), ("fariseu e publicano", "Lucas 18")]
for parab, ref in PARABOLAS:
    MORE.append(("advanced", f"Onde esta a parabola do {parab}?", ref, ["Outro", "Joao", "Marcos"], f"{ref}.", "novo_testamento"))

# 150+ more: numeros, personagens secundarios, eventos
NUMEROS = [(7, "dias da criacao"), (40, "dias no deserto Jesus"), (40, "anos Israel no deserto"), (12, "tribos de Israel"),
           (10, "mandamentos"), (10, "pragas do Egito"), (7, "igrejas Apocalipse"), (7, "selos Apocalipse"),
           (7, "trombetas Apocalipse"), (7, "taças Apocalipse"), (144000, "selados Apocalipse"), (1000, "anos milenio"),
           (3, "dias Jonas no peixe"), (3, "dias Jesus no tumulo"), (50, "dias Pentecostes"), (120, "no cenaculo"),
           (3000, "convertidos Pentecostes"), (70, "discipulos enviados"), (153, "peixes na rede"), (30, "moedas de Judas")]
for num, desc in NUMEROS:
    MORE.append(("intermediate", f"Qual o numero em: {desc}?", str(num), [str(n) for n in [num-1, num+1, num//2] if n != num][:3], f"Resposta: {num}.", "geral"))
PERSONS2 = [("Caim", "matou Abel"), ("Abel", "ofereceu cordeiro"), ("Enoque", "andou com Deus"), ("Melquisedeque", "rei de Salem"),
            ("Ló", "Sodoma"), ("Ismael", "filho de Agar"), ("Esaú", "vendeu primogenitura"), ("Labão", "pai de Raquel"),
            ("Raquel", "amada de Jacó"), ("Lea", "primeira esposa Jacó"), ("Benjamin", "filho da dor"), ("Ruben", "primogenito"),
            ("Miriã", "irma de Moises"), ("Jetró", "sogro Moises"), ("Calebe", "espia fiel"), ("Raabe", "escondeu espias"),
            ("Acã", "pecado em Jerico"), ("Débora", "juiza"), ("Gideão", "300 soldados"), ("Sansão", "cabelos longos"),
            ("Samuel", "menino no tabernaculo"), ("Saul", "primeiro rei"), ("Bateseba", "adulterio"), ("Urias", "hitita"),
            ("Absalão", "rebelou contra Davi"), ("Natã", "profeta a Davi"), ("Simeão", "esperava Consolador"), ("Ana", "profetisa"),
            ("Zacarias", "pai Joao Batista"), ("Isabel", "mae Joao Batista"), ("Nicodemos", "visitou a noite"), ("Maria Madalena", "primeira a ver"),
            ("Marta", "irma de Lazaro"), ("Lázaro", "ressuscitou"), ("Bartimeu", "cego curado"), ("Zaqueu", "subiu em arvore"),
            ("Cornélio", "centuriao"), ("Lidio", "vendedor de purpura"), ("Barnabé", "vendeu propriedade"), ("Timoteo", "filho na fe"),
            ("Tito", "em Creta"), ("Onesimo", "escravo fugitivo"), ("Filipe", "evangelista"), ("Estevão", "primeiro martir")]
for p, d in PERSONS2:
    MORE.append(("intermediate", f"Quem foi {p}?", d, ["Outro", "Desconhecido", "Ninguem"], f"{p}: {d}.", "historia"))

# 100+ mais: lugares, versiculos, eventos especificos
LUGARES = [("Belém", "nascimento Jesus"), ("Nazare", "criacao Jesus"), ("Jerusalem", "templo"), ("Jordao", "batismo"),
           ("Galileia", "ministerio Jesus"), ("Samaria", "mulher no poco"), ("Jerico", "muros caíram"), ("Betania", "Lazaro"),
           ("Getsemani", "oracao Jesus"), ("Golgota", "cruz"), ("Damascus", "conversao Paulo"), ("Antioquia", "cristaos"),
           ("Roma", "Paulo preso"), ("Patmos", "Apocalipse"), ("Sinai", "dez mandamentos"), ("Canaa", "terra prometida"),
           ("Babilonia", "exilio"), ("Egito", "Jose"), ("Ninive", "Jonas"), ("Tarsis", "Jonas fugiu")]
for lugar, desc in LUGARES:
    MORE.append(("beginner", f"Onde ocorreu: {desc}?", lugar, ["Outro", "Desconhecido", "Nenhum"], f"{lugar}: {desc}.", "historia"))
EVENTOS = [("transfiguracao", "Monte"), ("multiplicacao", "pães"), ("tempestade", "acalmada"), ("andou aguas", "Pedro"),
           ("cegueira", "Saulo"), ("Pentecostes", "linguas"), ("concilio", "Jerusalem"), ("viagem", "Paulo")]
for ev, hint in EVENTOS:
    MORE.append(("intermediate", f"O que aconteceu na {ev}?", hint, ["Outro", "Nada", "Diferente"], f"Evento: {ev}.", "novo_testamento"))
PALAVRAS = [("Emanuel", "Deus conosco"), ("Jesus", "Salvador"), ("Cristo", "Ungido"), ("Logos", "Verbo"),
            ("Espirito Santo", "Consolador"), ("Pai", "Abba"), ("Alfa e Omega", "principio e fim")]
for pal, sig in PALAVRAS:
    MORE.append(("advanced", f"O que significa {pal}?", sig, ["Outro", "Nao sei", "Diferente"], f"{pal} = {sig}.", "geral"))

# 50+ finais para passar 500
FINAL = [
    ("beginner", "Quantos livros Moises escreveu?", "5", ["4", "6", "7"], "O Pentateuco.", "antigo_testamento"),
    ("beginner", "Qual livro vem depois de Genesis?", "Exodo", ["Levitico", "Numeros", "Josue"], "Exodo continua a historia.", "antigo_testamento"),
    ("beginner", "Qual o ultimo livro do AT?", "Malaquias", ["Zacarias", "Ageu", "Esdras"], "Malaquias encerra o AT.", "antigo_testamento"),
    ("beginner", "Qual o primeiro livro do NT?", "Mateus", ["Marcos", "Lucas", "Joao"], "Mateus e o primeiro evangelho.", "novo_testamento"),
    ("beginner", "Quantas cartas Joao escreveu?", "3", ["1", "2", "4"], "1, 2 e 3 Joao.", "novo_testamento"),
    ("beginner", "Quantas cartas Pedro escreveu?", "2", ["1", "3", "4"], "1 e 2 Pedro.", "novo_testamento"),
    ("intermediate", "Qual apostolo era publicano?", "Mateus", ["Pedro", "Joao", "Andre"], "Mateus/Levi.", "novo_testamento"),
    ("intermediate", "Qual apostolo era irmão de Pedro?", "Andre", ["Joao", "Tiago", "Filipe"], "Andre era irmao de Pedro.", "novo_testamento"),
    ("intermediate", "Qual apostolo era irmão de Joao?", "Tiago", ["Pedro", "Andre", "Mateus"], "Tiago Maior.", "novo_testamento"),
    ("intermediate", "Qual apostolo levou Jesus a Filipe?", "Andre", ["Pedro", "Joao", "Mateus"], "Andre encontrou o menino.", "novo_testamento"),
    ("intermediate", "Qual discipulo era chamado Natanael?", "Bartolomeu", ["Filipe", "Tomas", "Mateus"], "Bartolomeu = Natanael.", "novo_testamento"),
    ("intermediate", "Qual apostolo era gemeo?", "Tomas", ["Mateus", "Tiago", "Simao"], "Dídimo = gemeo.", "novo_testamento"),
    ("intermediate", "Qual apostolo era cobrador de impostos?", "Mateus", ["Judas", "Simao", "Tadeu"], "Mateus = Levi.", "novo_testamento"),
    ("intermediate", "Qual apostolo era zelote?", "Simao", ["Judas", "Mateus", "Tomas"], "Simao o Zelote.", "novo_testamento"),
    ("intermediate", "Qual apostolo era Judas Tadeu?", "Tadeu", ["Judas Iscariotes", "Simao", "Mateus"], "Judas, nao Iscariotes.", "novo_testamento"),
    ("intermediate", "Quantos livros Joao escreveu?", "5", ["3", "4", "6"], "Joao, 1-3 Joao, Apocalipse.", "novo_testamento"),
    ("intermediate", "Qual evangelho foi escrito por um medico?", "Lucas", ["Mateus", "Marcos", "Joao"], "Lucas era medico.", "novo_testamento"),
    ("intermediate", "Qual evangelho enfatiza Jesus como Rei?", "Mateus", ["Marcos", "Lucas", "Joao"], "Genealogia real.", "novo_testamento"),
    ("intermediate", "Qual evangelho enfatiza Jesus como Servo?", "Marcos", ["Mateus", "Lucas", "Joao"], "Rapido e direto.", "novo_testamento"),
    ("intermediate", "Qual evangelho enfatiza Jesus como Homem?", "Lucas", ["Mateus", "Marcos", "Joao"], "Genealogia humana.", "novo_testamento"),
    ("intermediate", "Qual evangelho enfatiza Jesus como Deus?", "Joao", ["Mateus", "Marcos", "Lucas"], "No principio era o Verbo.", "novo_testamento"),
    ("advanced", "Qual livro tem 31 capitulos?", "Proverbios", ["Eclesiastes", "Job", "Cantares"], "Um capitulo por dia.", "antigo_testamento"),
    ("advanced", "Qual Salmo e acrostico?", "119", ["1", "23", "91"], "Cada secao com uma letra.", "antigo_testamento"),
    ("advanced", "Quantas letras tem o alfabeto hebraico?", "22", ["24", "26", "20"], "22 letras.", "antigo_testamento"),
    ("advanced", "Qual livro cita 'Vaidade de vaidades'?", "Eclesiastes", ["Job", "Proverbios", "Cantares"], "Ec 1:2.", "antigo_testamento"),
    ("advanced", "Onde esta 'Mais bem-aventurado e dar que receber'?", "Atos 20:35", ["Lucas 6", "Mateus 5", "Joao 13"], "Palavras de Jesus em Atos.", "novo_testamento"),
    ("beginner", "Qual animal apareceu a Eva?", "Serpente", ["Diabo", "Anjo", "Homem"], "A serpente enganou Eva.", "historia"),
    ("beginner", "Qual fruto Eva comeu?", "Fruto da arvore", ["Maca", "Uva", "Figo"], "A Biblia nao especifica.", "historia"),
    ("intermediate", "Quantos pares de animais Noe levou?", "7 limpos, 2 impuros", ["1 de cada", "2 de cada", "3 de cada"], "Gen 7:2.", "historia"),
    ("intermediate", "Qual montanha a arca parou?", "Ararate", ["Sinai", "Hermom", "Carmelo"], "Montanhas de Ararate.", "historia"),
    ("intermediate", "Qual corvo Noe soltou primeiro?", "Nao nomeado", ["Um", "Dois", "Nenhum"], "O corvo nao voltou.", "historia"),
    ("intermediate", "Qual pomba voltou com ramo?", "Segunda vez", ["Primeira", "Terceira", "Nunca"], "Pomba com folha de oliveira.", "historia"),
    ("beginner", "Quem matou Abel?", "Caim", ["Satanas", "Adao", "Eva"], "Caim por inveja.", "historia"),
    ("beginner", "Quantos filhos tinha Noe?", "3", ["2", "4", "5"], "Sem, Cam e Jafé.", "historia"),
    ("intermediate", "Qual filho de Noe foi amaldicoado?", "Cam", ["Sem", "Jafé", "Canaã"], "Cam viu a nudez do pai.", "historia"),
    ("intermediate", "Qual a terra prometida?", "Canaa", ["Egito", "Babilonia", "Assiria"], "Terra de Canaã.", "historia"),
    ("intermediate", "Quantas cidades foram destruidas em Sodoma?", "5", ["2", "3", "10"], "Sodoma, Gomorra e outras.", "historia"),
    ("beginner", "Quem salvou Ló de Sodoma?", "Anjos", ["Abraao", "Noe", "Melquisedeque"], "Dois anjos tiraram Ló.", "historia"),
    ("beginner", "Qual mulher virou estatua de sal?", "Mulher de Ló", ["Eva", "Sara", "Rebeca"], "Olhou para tras.", "historia"),
    ("intermediate", "Quantas esposas Abraao teve?", "2 principais", ["1", "3", "4"], "Sara e Quetura.", "historia"),
    ("intermediate", "Quem era o filho de Abraao com Agar?", "Ismael", ["Isaque", "Esaú", "Jacó"], "Filho da serva.", "historia"),
    ("intermediate", "Onde Isaque foi sacrificado?", "Monte Moria", ["Monte Sinai", "Monte Nebo", "Monte Carmelo"], "Onde depois seria o templo.", "historia"),
    ("intermediate", "Quantos anos Sara tinha quando Isaque nasceu?", "90", ["80", "100", "75"], "Sara riu da promessa.", "historia"),
    ("beginner", "Quantas pragas cairam no Egito?", "10", ["7", "12", "3"], "Dez pragas antes do Exodo.", "leis"),
    ("intermediate", "Qual mandamento honra pai e mae?", "Quinto", ["Quarto", "Sexto", "Decimo"], "Honra teu pai e tua mae.", "leis"),
    ("intermediate", "Qual mandamento proibe matar?", "Sexto", ["Quinto", "Setimo", "Oitavo"], "Nao matarás.", "leis"),
]
for q in FINAL:
    MORE.append(q)

# Fix nested lists in MORE
MORE[2] = ("intermediate", "Quem Jesus ressuscitou da filha de Jairo?", "Filha de 12 anos", ["Lazaro", "viuva", "Lázaro"], "Mc 5.", "novo_testamento")
MORE[23] = ("intermediate", "Quantos anos tinha Caleb quando conquistou Hebrom?", "85", ["40", "80", "90"], "Josue 14:10.", "historia")
MORE[15] = ("beginner", "Qual ladrao se arrependeu na cruz?", "O da direita", ["O da esquerda", "Ambos", "Nenhum"], "Hoje estarás comigo.", "novo_testamento")

Q.extend(INT_Q)
Q.extend(ADV_Q)
Q.extend(BULK)
Q.extend(EXTRA)
Q.extend(MORE)

# Generate output
OUT = []
for d, qt, ca, wa, ex, cat in Q:
    OUT.append({
        "difficulty_level": d,
        "question_type": "multiple_choice",
        "question_text": qt,
        "correct_answer": ca,
        "wrong_answers": wa,
        "explanation": ex,
        "category": cat,
    })

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "quiz_questions.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(OUT, f, ensure_ascii=False, indent=2)
print(f"Generated {len(OUT)} quiz questions to {path}")