from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config.settings import DB_CONFIG

encoded_password = quote_plus(DB_CONFIG["password"])

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_CONFIG['user']}:"
    f"{encoded_password}@"
    f"{DB_CONFIG['host']}:"
    f"{DB_CONFIG['port']}/"
    f"{DB_CONFIG['dbname']}"
)

engine = create_engine(DATABASE_URL)

def get_engine():
    return engine