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
    publication_date TIMESTAMP NOT NULL,
    query0 SMALLINT,
    query1 SMALLINT,
    query2 SMALLINT,
    source_id INT REFERENCES sources(id) NOT NULL,
    author_id INT REFERENCES authors(id) NOT NULL,
    CONSTRAINT unique_title_url UNIQUE (title, url)
);


CREATE TABLE news_sources (
    news_id INT REFERENCES news(id),
    source_id INT REFERENCES sources(id),
    PRIMARY KEY (news_id, source_id)
);

