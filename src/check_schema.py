import psycopg2

conn = psycopg2.connect("your database URL here")
cur = conn.cursor()

for table in ["customers", "orders", "products"]:
    print("\nTable:", table)
    cur.execute(f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table}';
    """)
    print(cur.fetchall())
