-- silver_db Schema 
\c api_news
-- CREATE SCHEMA
SET search_path TO api_news;

DROP SCHEMA IF EXISTS silver_db CASCADE;
CREATE SCHEMA IF NOT EXISTS silver_db;

-- Set search path for the schema
SET search_path TO silver_db;

-- Create tables
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    url VARCHAR(512) NOT NULL,
    image_url VARCHAR(500),
    publication_date TIMESTAMP NOT NULL,
    content TEXT,
    author_id INT REFERENCES authors(id) NOT NULL,
    source_id INT REFERENCES sources(id) NOT NULL
);

CREATE TABLE news_tags (
    news_id INT REFERENCES news(id),
    tag VARCHAR(255),
    PRIMARY KEY (news_id, tag)
);

CREATE TABLE news_sources (
    news_id INT REFERENCES news(id),
    source_id INT REFERENCES sources(id),
    PRIMARY KEY (news_id, source_id)
);

