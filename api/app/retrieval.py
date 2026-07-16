from dataclasses import dataclass
from app.config import EMBED_MODEL
from app.db import pool
from sentence_transformers import SentenceTransformer

@dataclass(frozen=True)
class Snippet:
    source: str
    text: str

class Index:
    def __init__(self, model_name: str = EMBED_MODEL):
        self.model = SentenceTransformer(model_name)
    
    def top_k(self, question: str, k: int = 2) -> list[tuple[float, Snippet]]:
        q = self.model.encode([question], normalize_embeddings=True)[0]
        with pool.connection() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT source, text, 1 - (embedding <=> %s) AS score "
                "FROM chunks ORDER BY embedding <=> %s LIMIT %s",
                (q, q, k),
            )
            return [(float(score), Snippet(source, text))
                for source, text, score in cur.fetchall()]
