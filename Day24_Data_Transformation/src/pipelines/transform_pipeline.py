from src.db.postgres_connector import PostgresConnector


def run_transformation():

    connector = PostgresConnector()
    conn = connector.connect()
    cursor = conn.cursor()

    # create table
    with open("sql/schema.sql") as f:
        cursor.execute(f.read())

    conn.commit()

    # run transformation
    with open("sql/transformations.sql") as f:
        cursor.execute(f.read())

    conn.commit()

    # check results
    cursor.execute("SELECT * FROM daily_sales_summary;")
    rows = cursor.fetchall()

    print("Daily Sales Summary")
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    run_transformation()