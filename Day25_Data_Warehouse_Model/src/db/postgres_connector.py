import psycopg2
from src.db.config import DB_CONFIG


class PostgresConnector:

    def connect(self):
        return psycopg2.connect(**DB_CONFIG)