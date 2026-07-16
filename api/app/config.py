import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY")
MODEL=os.getenv("MODEL")

# --- paths --- (__file__ = .../app/config.py; parent.parent = api/)
API_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = API_DIR / "data"
CORPUS_PATH = DATA_DIR / "onepiece.json"

# --- ingestion ---
WIKI_API = "https://onepiece.fandom.com/api.php"
USER_AGENT = "LoreEngine/0.1 (learning project; contact: you@example.com)"

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:lore@localhost:5432/lore")
EMBED_MODEL  = "all-MiniLM-L6-v2"
EMBED_DIM    = 384  # must match vector(384) in schema.sql