from db_connector import DBConnector
from query_executor import QueryExecutor

db = DBConnector("data/ecommerce.db")
conn = db.get_connection()
executor = QueryExecutor(conn)

with open("sql/top_customers.sql", "r") as file:
    query = file.read()

top_customers = executor.fetch_all(query, (5,))

print("Top 5 Customers:")
for row in top_customers:
    print(row)

conn.close()