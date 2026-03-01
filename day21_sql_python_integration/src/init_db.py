from db_connector import DBConnector
from query_executor import QueryExecutor
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

db = DBConnector("data/ecommerce.db")
conn = db.get_connection()
executor = QueryExecutor(conn)

# Create table
executor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL
);
""")

# Insert sample data
sample_data = [
    (101, 200.0),
    (102, 150.0),
    (101, 300.0),
    (103, 500.0),
    (102, 100.0),
    (104, 250.0)
]

for customer_id, amount in sample_data:
    executor.execute(
        "INSERT INTO orders (customer_id, amount) VALUES (?, ?)",
        (customer_id, amount)
    )

print("Database initialized successfully!")

conn.close()