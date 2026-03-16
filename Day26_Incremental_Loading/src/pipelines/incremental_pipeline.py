from src.db.postgres_connector import PostgresConnector


def get_last_loaded_id():

    with open("metadata/last_loaded_id.txt") as f:
        return int(f.read().strip())


def update_last_loaded_id(new_id):

    with open("metadata/last_loaded_id.txt", "w") as f:
        f.write(str(new_id))


def run_pipeline():

    connector = PostgresConnector()
    conn = connector.connect()
    cursor = conn.cursor()

    last_id = get_last_loaded_id()

    print("Last loaded order_id:", last_id)

    with open("sql/schema.sql") as f:
        cursor.execute(f.read())

    with open("sql/incremental_load.sql") as f:
        query = f.read()

    cursor.execute(query, (last_id,))

    conn.commit()

    cursor.execute("SELECT MAX(order_id) FROM orders")
    new_last_id = cursor.fetchone()[0]

    update_last_loaded_id(new_last_id)

    print("Pipeline finished")
    print("New last loaded id:", new_last_id)

    cursor.close()
    conn.close()
    
if __name__ == "__main__":
    run_pipeline()