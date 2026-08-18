CREATE TABLE IF NOT EXISTS filmes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    genero TEXT NOT NULL,
    ano INTEGER NOT NULL,
    nota REAL NOT NULL CHECK(nota >= 0 AND nota <= 10)
);

INSERT INTO filmes (titulo, genero, ano, nota) VALUES
('Interestelar', 'Ficção Científica', 2014, 9.5),
('O Poderoso Chefão', 'Drama', 1972, 9.2),
('Homem-Aranha: No Aranhaverso', 'Animação', 2018, 9.0);
