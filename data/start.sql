CREATE DATABASE toto;
\c toto;
CREATE TABLE t1 (id int);

CREATE TABLE noticias (
    id SERIAL PRIMARY KEY,
    autor VARCHAR(255),
    titulo VARCHAR(255),
    descricao TEXT,
    url VARCHAR(512),
    imagem_url VARCHAR(500),
    data_publicacao TIMESTAMP,
    conteudo TEXT,
    tags VARCHAR(255),
    fonte VARCHAR(255)
);

CREATE TABLE autor (
    id SERIAL PRIMARY KEY,
    autor VARCHAR(255),
);

CREATE TABLE fonte (
    id SERIAL PRIMARY KEY,
    fonte VARCHAR(255),
);

CREATE TABLE autor_fonte (
    id_autor INT,
    id_fonte INT
);

