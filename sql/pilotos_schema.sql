CREATE TABLE pilotos (
    driverId TEXT PRIMARY KEY NOT NULL,
    biografia TEXT UNIQUE,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    dataDeNascimento VARCHAR(10),
    nacionalidade TEXT
);