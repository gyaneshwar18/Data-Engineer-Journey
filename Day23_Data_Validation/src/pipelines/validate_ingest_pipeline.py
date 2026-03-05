
import csv
from src.db.postgres_connector import PostgresConnector
from src.validation.validator import validate_record

def run_pipeline():
    connector = PostgresConnector()
    conn = connector.connect()
    cursor = conn.cursor()

# Create tables
    with open("sql/schema.sql") as f:
        cursor.execute(f.read())

    with open("sql/reject_table.sql") as f:
        cursor.execute(f.read())

    conn.commit()

    valid_count = 0
    reject_count = 0

    with open("data/orders_dirty.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            reason = validate_record(row)

            if reason is None:
                cursor.execute(
                    """
                    INSERT INTO orders(customer_id, order_date, amount, status)
                    VALUES (%s,%s,%s,%s)
                    """,
                    (
                        int(row["customer_id"]),
                        row["order_date"],
                        float(row["amount"]),
                        row["status"]
                    )
                )   
                valid_count += 1
            else:
                cursor.execute(
                """
                INSERT INTO rejected_orders(customer_id, order_date, amount, status, reason)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    row["customer_id"],
                    row["order_date"],
                    row["amount"],
                    row["status"],
                    reason
                )
            )
            reject_count += 1

    conn.commit()

    cursor.close()
    conn.close()

    print("Pipeline completed")
    print("Valid records:", valid_count)
    print("Rejected records:", reject_count)




if __name__ == "__main__":
    run_pipeline()