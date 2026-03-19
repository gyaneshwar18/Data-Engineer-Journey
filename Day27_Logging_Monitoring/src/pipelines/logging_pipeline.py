import time
from src.db.postgres_connector import PostgresConnector
from src.utils.logger import get_logger


def run_pipeline():

    logger = get_logger()

    logger.info("Pipeline started")

    start_time = time.time()

    try:
        connector = PostgresConnector()
        conn = connector.connect()
        cursor = conn.cursor()

        logger.info("Database connection established")

        # sample query
        cursor.execute("SELECT COUNT(*) FROM orders;")
        count = cursor.fetchone()[0]

        logger.info(f"Total records in orders table: {count}")

        conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        print("Error occurred. Check logs.")

    end_time = time.time()

    logger.info(f"Pipeline completed in {end_time - start_time:.2f} seconds")

    print("Pipeline executed successfully")


if __name__ == "__main__":
    run_pipeline()