import psycopg2 as pg
from src.core.config import DB_CONFIG


def get_db():
    conn = pg.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()