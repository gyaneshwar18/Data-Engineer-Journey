import psycopg2
from src.db.config import DB_CONFIG


class PostgresConnector:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(**DB_CONFIG)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()