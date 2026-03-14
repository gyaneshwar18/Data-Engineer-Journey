from src.db.postgres_connector import PostgresConnector

def run_pipeline():

    connector = PostgresConnector()
    conn = connector.connect()
    cursor = conn.cursor()

    with open("sql/schema.sql") as f:
        cursor.execute(f.read())

    with open("sql/load_dimensions.sql") as f:
        cursor.execute(f.read())

    with open("sql/load_fact.sql") as f:
        cursor.execute(f.read())

    conn.commit()

    print("Data warehouse loaded successfully")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    run_pipeline()