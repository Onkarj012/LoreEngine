from psycopg_pool import ConnectionPool
from pgvector.psycopg import register_vector
from app.config import DATABASE_URL

pool = ConnectionPool(DATABASE_URL, open=True, configure=register_vector)

