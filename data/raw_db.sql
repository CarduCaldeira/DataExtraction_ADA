-- raw_db Schema

-- Create schema
DROP SCHEMA IF EXISTS raw_db CASCADE;
CREATE SCHEMA IF NOT EXISTS raw_db;

-- Set search path for the schema
SET search_path TO raw_db;

-- Create table for news
CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    author VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    url VARCHAR(512),
    image_url VARCHAR(500),
    publication_date TIMESTAMP,
    content TEXT,
    tags VARCHAR(255),
    source VARCHAR(255)
);
