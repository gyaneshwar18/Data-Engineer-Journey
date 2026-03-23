import logging
from src.db.postgres_connector import PostgresConnector

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_transformation():

    logging.info("Starting transformation pipeline")

    connector = PostgresConnector()
    conn = connector.connect()  
    cursor = conn.cursor()

    logging.info("Database connection established")

    # create table
    with open("sql/schema.sql") as f:
        cursor.execute(f.read())
    conn.commit()

    logging.info("Schema executed successfully")

    # run transformation
    with open("sql/transformations.sql") as f:
        cursor.execute(f.read())
    conn.commit()

    logging.info("Transformation query executed")

    cursor.execute("SELECT * FROM daily_sales_summary;")
    rows = cursor.fetchall()

    logging.info("Fetched analytics results")

    print("Daily Sales Summary")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()

    logging.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_transformation()