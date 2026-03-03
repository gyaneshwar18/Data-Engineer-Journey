import time
from src.db.postgres_connector import PostgresConnector
from src.utils.logger import logging


def ingest_with_copy(file_path):
    connector = PostgresConnector()
    conn = connector.connect()
    cursor = conn.cursor()

    try:
        # Create schema first
        with open("sql/schema.sql", "r") as f:
            schema_query = f.read()
        cursor.execute(schema_query)
        conn.commit()

        start_time = time.time()
        logging.info("Starting CSV ingestion using COPY")

        with open(file_path, "r") as f:
            cursor.copy_expert(
                """
                COPY orders(customer_id, order_date, amount, status)
                FROM STDIN
                WITH CSV HEADER
                """,
                f
            )

        conn.commit()

        end_time = time.time()
        execution_time = end_time - start_time

        logging.info("CSV ingestion completed successfully")
        print(f"Execution Time: {execution_time:.2f} seconds")

        # Validate row count
        cursor.execute("SELECT COUNT(*) FROM orders;")
        total = cursor.fetchone()[0]
        print("Total rows in table:", total)

    except Exception as e:
        conn.rollback()
        logging.error(f"Ingestion failed: {e}")
        print("Error occurred. Transaction rolled back.")

    finally:
        cursor.close()
        connector.close()


if __name__ == "__main__":
    ingest_with_copy("data/sample_orders.csv")