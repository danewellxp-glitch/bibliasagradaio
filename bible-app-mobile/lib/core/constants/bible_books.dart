class BibleBook {
  final int number;
  final String name;
  final String abbreviation;
  final int chapters;
  final String testament;

  const BibleBook({
    required this.number,
    required this.name,
    required this.abbreviation,
    required this.chapters,
    required this.testament,
  });
}

const List<BibleBook> bibleBooks = [
  // Antigo Testamento
  BibleBook(number: 1, name: 'Genesis', abbreviation: 'Gn', chapters: 50, testament: 'AT'),
  BibleBook(number: 2, name: 'Exodo', abbreviation: 'Ex', chapters: 40, testament: 'AT'),
  BibleBook(number: 3, name: 'Levitico', abbreviation: 'Lv', chapters: 27, testament: 'AT'),
  BibleBook(number: 4, name: 'Numeros', abbreviation: 'Nm', chapters: 36, testament: 'AT'),
  BibleBook(number: 5, name: 'Deuteronomio', abbreviation: 'Dt', chapters: 34, testament: 'AT'),
  BibleBook(number: 6, name: 'Josue', abbreviation: 'Js', chapters: 24, testament: 'AT'),
  BibleBook(number: 7, name: 'Juizes', abbreviation: 'Jz', chapters: 21, testament: 'AT'),
  BibleBook(number: 8, name: 'Rute', abbreviation: 'Rt', chapters: 4, testament: 'AT'),
  BibleBook(number: 9, name: '1 Samuel', abbreviation: '1Sm', chapters: 31, testament: 'AT'),
  BibleBook(number: 10, name: '2 Samuel', abbreviation: '2Sm', chapters: 24, testament: 'AT'),
  BibleBook(number: 11, name: '1 Reis', abbreviation: '1Rs', chapters: 22, testament: 'AT'),
  BibleBook(number: 12, name: '2 Reis', abbreviation: '2Rs', chapters: 25, testament: 'AT'),
  BibleBook(number: 13, name: '1 Cronicas', abbreviation: '1Cr', chapters: 29, testament: 'AT'),
  BibleBook(number: 14, name: '2 Cronicas', abbreviation: '2Cr', chapters: 36, testament: 'AT'),
  BibleBook(number: 15, name: 'Esdras', abbreviation: 'Ed', chapters: 10, testament: 'AT'),
  BibleBook(number: 16, name: 'Neemias', abbreviation: 'Ne', chapters: 13, testament: 'AT'),
  BibleBook(number: 17, name: 'Ester', abbreviation: 'Et', chapters: 10, testament: 'AT'),
  BibleBook(number: 18, name: 'J\u00f3', abbreviation: 'J\u00f3', chapters: 42, testament: 'AT'),
  BibleBook(number: 19, name: 'Salmos', abbreviation: 'Sl', chapters: 150, testament: 'AT'),
  BibleBook(number: 20, name: 'Proverbios', abbreviation: 'Pv', chapters: 31, testament: 'AT'),
  BibleBook(number: 21, name: 'Eclesiastes', abbreviation: 'Ec', chapters: 12, testament: 'AT'),
  BibleBook(number: 22, name: 'Canticos', abbreviation: 'Ct', chapters: 8, testament: 'AT'),
  BibleBook(number: 23, name: 'Isaias', abbreviation: 'Is', chapters: 66, testament: 'AT'),
  BibleBook(number: 24, name: 'Jeremias', abbreviation: 'Jr', chapters: 52, testament: 'AT'),
  BibleBook(number: 25, name: 'Lamentacoes', abbreviation: 'Lm', chapters: 5, testament: 'AT'),
  BibleBook(number: 26, name: 'Ezequiel', abbreviation: 'Ez', chapters: 48, testament: 'AT'),
  BibleBook(number: 27, name: 'Daniel', abbreviation: 'Dn', chapters: 12, testament: 'AT'),
  BibleBook(number: 28, name: 'Oseias', abbreviation: 'Os', chapters: 14, testament: 'AT'),
  BibleBook(number: 29, name: 'Joel', abbreviation: 'Jl', chapters: 3, testament: 'AT'),
  BibleBook(number: 30, name: 'Amos', abbreviation: 'Am', chapters: 9, testament: 'AT'),
  BibleBook(number: 31, name: 'Obadias', abbreviation: 'Ob', chapters: 1, testament: 'AT'),
  BibleBook(number: 32, name: 'Jonas', abbreviation: 'Jn', chapters: 4, testament: 'AT'),
  BibleBook(number: 33, name: 'Miqueias', abbreviation: 'Mq', chapters: 7, testament: 'AT'),
  BibleBook(number: 34, name: 'Naum', abbreviation: 'Na', chapters: 3, testament: 'AT'),
  BibleBook(number: 35, name: 'Habacuque', abbreviation: 'Hc', chapters: 3, testament: 'AT'),
  BibleBook(number: 36, name: 'Sofonias', abbreviation: 'Sf', chapters: 3, testament: 'AT'),
  BibleBook(number: 37, name: 'Ageu', abbreviation: 'Ag', chapters: 2, testament: 'AT'),
  BibleBook(number: 38, name: 'Zacarias', abbreviation: 'Zc', chapters: 14, testament: 'AT'),
  BibleBook(number: 39, name: 'Malaquias', abbreviation: 'Ml', chapters: 4, testament: 'AT'),
  // Novo Testamento
  BibleBook(number: 40, name: 'Mateus', abbreviation: 'Mt', chapters: 28, testament: 'NT'),
  BibleBook(number: 41, name: 'Marcos', abbreviation: 'Mc', chapters: 16, testament: 'NT'),
  BibleBook(number: 42, name: 'Lucas', abbreviation: 'Lc', chapters: 24, testament: 'NT'),
  BibleBook(number: 43, name: 'Joao', abbreviation: 'Jo', chapters: 21, testament: 'NT'),
  BibleBook(number: 44, name: 'Atos', abbreviation: 'At', chapters: 28, testament: 'NT'),
  BibleBook(number: 45, name: 'Romanos', abbreviation: 'Rm', chapters: 16, testament: 'NT'),
  BibleBook(number: 46, name: '1 Corintios', abbreviation: '1Co', chapters: 16, testament: 'NT'),
  BibleBook(number: 47, name: '2 Corintios', abbreviation: '2Co', chapters: 13, testament: 'NT'),
  BibleBook(number: 48, name: 'Galatas', abbreviation: 'Gl', chapters: 6, testament: 'NT'),
  BibleBook(number: 49, name: 'Efesios', abbreviation: 'Ef', chapters: 6, testament: 'NT'),
  BibleBook(number: 50, name: 'Filipenses', abbreviation: 'Fp', chapters: 4, testament: 'NT'),
  BibleBook(number: 51, name: 'Colossenses', abbreviation: 'Cl', chapters: 4, testament: 'NT'),
  BibleBook(number: 52, name: '1 Tessalonicenses', abbreviation: '1Ts', chapters: 5, testament: 'NT'),
  BibleBook(number: 53, name: '2 Tessalonicenses', abbreviation: '2Ts', chapters: 3, testament: 'NT'),
  BibleBook(number: 54, name: '1 Timoteo', abbreviation: '1Tm', chapters: 6, testament: 'NT'),
  BibleBook(number: 55, name: '2 Timoteo', abbreviation: '2Tm', chapters: 4, testament: 'NT'),
  BibleBook(number: 56, name: 'Tito', abbreviation: 'Tt', chapters: 3, testament: 'NT'),
  BibleBook(number: 57, name: 'Filemom', abbreviation: 'Fm', chapters: 1, testament: 'NT'),
  BibleBook(number: 58, name: 'Hebreus', abbreviation: 'Hb', chapters: 13, testament: 'NT'),
  BibleBook(number: 59, name: 'Tiago', abbreviation: 'Tg', chapters: 5, testament: 'NT'),
  BibleBook(number: 60, name: '1 Pedro', abbreviation: '1Pe', chapters: 5, testament: 'NT'),
  BibleBook(number: 61, name: '2 Pedro', abbreviation: '2Pe', chapters: 3, testament: 'NT'),
  BibleBook(number: 62, name: '1 Joao', abbreviation: '1Jo', chapters: 5, testament: 'NT'),
  BibleBook(number: 63, name: '2 Joao', abbreviation: '2Jo', chapters: 1, testament: 'NT'),
  BibleBook(number: 64, name: '3 Joao', abbreviation: '3Jo', chapters: 1, testament: 'NT'),
  BibleBook(number: 65, name: 'Judas', abbreviation: 'Jd', chapters: 1, testament: 'NT'),
  BibleBook(number: 66, name: 'Apocalipse', abbreviation: 'Ap', chapters: 22, testament: 'NT'),
];

List<BibleBook> get oldTestamentBooks =>
    bibleBooks.where((b) => b.testament == 'AT').toList();

List<BibleBook> get newTestamentBooks =>
    bibleBooks.where((b) => b.testament == 'NT').toList();

BibleBook getBookByNumber(int number) =>
    bibleBooks.firstWhere((b) => b.number == number);
