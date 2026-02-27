import sqlite3
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "data", "ecommerce.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\nRunning query BEFORE index...\n")

start = time.time()
cursor.execute("SELECT * FROM orders WHERE customer_id = 5000;")
rows = cursor.fetchall()
end = time.time()

print("Rows returned:", len(rows))
print("Execution time:", end - start)

print("\nQuery Plan:")
cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 5000;")
print(cursor.fetchall())

conn.close()