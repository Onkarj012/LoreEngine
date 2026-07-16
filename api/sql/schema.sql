CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
    id        bigserial PRIMARY KEY,
    source    text   NOT NULL,        -- wiki page title (your citation)
    text      text   NOT NULL,        -- the snippet prose
    embedding vector(384) NOT NULL   -- 384 = all-MiniLM-L6-v2 output dims
);

-- approximate-nearest-neighbour index for cosine distance
CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw
    ON chunks USING hnsw (embedding vector_cosine_ops);