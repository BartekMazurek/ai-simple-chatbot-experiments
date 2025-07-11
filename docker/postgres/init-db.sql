CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA vector

CREATE TABLE vector.items
(
    id              SERIAL PRIMARY KEY,
    content         TEXT,
    embedding       vector(384)
);
