import sqlite3
import random
import string
from datetime import datetime, timedelta

conn = sqlite3.connect("day20_indexing_optimization/data/ecommerce.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    amount REAL,
    status TEXT
)
""")

statuses = ["completed", "cancelled", "pending"]

for i in range(1, 100001):  # 100K rows
    cursor.execute("""
    INSERT INTO orders (customer_id, order_date, amount, status)
    VALUES (?, ?, ?, ?)
    """, (
        random.randint(1, 10000),
        (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d"),
        round(random.uniform(100, 10000), 2),
        random.choice(statuses)
    ))

conn.commit()
conn.close()