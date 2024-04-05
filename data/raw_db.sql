-- api_news DATABASE

-- DATABASE: api_news
DROP DATABASE IF EXISTS api_news;

CREATE DATABASE api_news;

-- Connect to database
\c api_news

-- SET database search path
SET search_path TO api_news;

-- CREATE SCHEMA
DROP SCHEMA IF EXISTS raw_db CASCADE;

CREATE SCHEMA IF NOT EXISTS raw_db;

-- SET Schema search path
SET search_path TO raw_db;

-- CREATE TABLES
CREATE TABLE noticias (
    id SERIAL PRIMARY KEY,
    autor VARCHAR(255) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    url VARCHAR(512) NOT NULL,
    imagem_url VARCHAR(500),
    data_publicacao TIMESTAMP NOT NULL,
    conteudo TEXT,
    tags VARCHAR(255),
    fonte VARCHAR(255) NOT NULL
);