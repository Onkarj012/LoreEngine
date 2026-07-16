import json
from app.config import CORPUS_PATH, EMBED_MODEL
from app.db import pool
from sentence_transformers import SentenceTransformer

def main() -> None:
    rows = json.loads(CORPUS_PATH.read_text())
    model = SentenceTransformer(EMBED_MODEL)
    embs = model.encode([r["text"] for r in rows], normalize_embeddings=True)

    with pool.connection() as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE chunks")              # clean refill for now
        cur.executemany(
            "INSERT INTO chunks (source, text, embedding) VALUES (%s, %s, %s)",
            [(r["source"], r["text"], emb) for r, emb in zip(rows, embs)],
        )
    print(f"seeded {len(rows)} chunks")
    pool.close()

if __name__ == "__main__":
    main()