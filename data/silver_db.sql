-- silver_db Schema 

-- CREATE SCHEMA
DROP SCHEMA IF EXISTS silver_db CASCADE;

CREATE SCHEMA IF NOT EXISTS silver_db;

-- SET Schema search path
SET search_path TO silver_db;


CREATE TABLE autores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE fontes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE noticias (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    url VARCHAR(512) NOT NULL,
    imagem_url VARCHAR(500),
    data_publicacao TIMESTAMP NOT NULL,
    conteudo TEXT,
    id_autor INT REFERENCES autores(id) NOT NULL,
    id_fonte INT REFERENCES fontes(id) NOT NULL
);

CREATE TABLE noticias_tags (
    id_noticia INT REFERENCES noticias(id),
    tag VARCHAR(255),
    PRIMARY KEY (id_noticia, tag)
);
