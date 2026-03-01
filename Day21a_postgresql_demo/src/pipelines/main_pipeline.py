from src.db.postgres_connector import PostgresConnector
from src.db.sqlalchemy_engine import get_engine
import pandas as pd


def run_pipeline():
    # Connect using psycopg2
    connector = PostgresConnector()
    conn = connector.connect()
    cursor = conn.cursor()

    # -------------------------------
    # STEP 1: Create Schema
    # -------------------------------
    with open("sql/schema.sql", "r") as f:
        schema_query = f.read()

    cursor.execute(schema_query)
    conn.commit()
    print("Schema created successfully.")

    # -------------------------------
    # STEP 2: Insert Sample Data
    # -------------------------------
    insert_query = """
    INSERT INTO orders (customer_id, order_date, amount, status)
    VALUES (%s, %s, %s, %s)
    """

    sample_data = [
        (101, "2026-02-01", 2500, "completed"),
        (102, "2026-02-02", 1800, "pending"),
        (103, "2026-02-03", 3200, "completed"),
    ]

    for row in sample_data:
        cursor.execute(insert_query, row)

    conn.commit()
    print("Sample data inserted.")

    cursor.close()
    connector.close()

    # -------------------------------
    # STEP 3: Use SQLAlchemy + Pandas
    # -------------------------------
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM orders;", engine)

    print("\nData from PostgreSQL:")
    print(df.head())


if __name__ == "__main__":
    run_pipeline()