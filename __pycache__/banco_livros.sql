CREATE TABLE Livros (
    id INTEGER PRIMARY KEY,
    titulo TEXT,
    autor TEXT,
    ano INTEGER,
    genero TEXT,
    disponivel BOOLEAN
);

INSERT INTO Livros (titulo, autor, ano, genero, disponivel) VALUES
    ('Receita para o Céu', 'Victor Sousa', 1999, 'Romance', 1),
    ('Um dia na Eternidade', 'B Rubben', 1939, 'Fantasia', 1),
    ('Celeiro da Paz', 'Jackson Loyd', 1967, 'Realismo Mágico', 1),
    ('Uma Prisão de Mil Homens', 'Miranda Alencar', 1943, 'Drama', 1),
    ('Cavalos Livres', 'Yago Gomez', 1937, 'Fábula', 1);

SELECT * FROM Livros WHERE disponivel = 1;

UPDATE Livros SET disponivel = 0 WHERE titulo = 'Cavalos Livres';

SELECT * FROM Livros ORDER BY ano DESC;

DELETE FROM Livros WHERE ano < 1940;

DROP TABLE IF EXISTS Livros;

CREATE TABLE Livros (
    id INTEGER PRIMARY KEY,
    titulo TEXT,
    autor TEXT,
    ano INTEGER,
    genero TEXT,
    disponivel BOOLEAN
);