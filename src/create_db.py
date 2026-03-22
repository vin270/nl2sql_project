import sqlite3, os
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'shop.db')
schema = '''
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;

CREATE TABLE customers ( id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL );
CREATE TABLE products  ( id INTEGER PRIMARY KEY, name TEXT NOT NULL, price REAL NOT NULL );
CREATE TABLE orders    ( id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, order_date TEXT NOT NULL, total_amount REAL NOT NULL,
                         FOREIGN KEY(customer_id) REFERENCES customers(id) );
'''
customers = [
    (1, "Jane Smith", "London"),
    (2, "John Doe", "Manchester"),
    (3, "Alice Johnson", "Birmingham"),
    (4, "Bob Lee", "London"),
    (5, "Sara Khan", "Leeds")
]
products = [
    (1, "Pro Keyboard", 49.99),
    (2, "Basic Mouse", 9.99),
    (3, "USB-C Cable", 6.50),
    (4, "Gaming Headset", 79.00),
    (5, "Pro Monitor", 199.99)
]
orders = [
    (1, 1, "2025-07-01", 129.99),
    (2, 2, "2025-06-15", 19.99),
    (3, 1, "2025-07-20", 249.00),
    (4, 3, "2024-12-01", 15.99),
    (5, 4, "2025-08-02", 300.00),
    (6, 5, "2025-09-10", 29.99)
]
def main():
    os.makedirs(os.path.join(os.path.dirname(DB_PATH)), exist_ok=True)
    conn = sqlite3.connect(DB_PATH); cur = conn.cursor()
    cur.executescript(schema)
    cur.executemany("INSERT INTO customers (id,name,city) VALUES (?,?,?)", customers)
    cur.executemany("INSERT INTO products (id,name,price) VALUES (?,?,?)", products)
    cur.executemany("INSERT INTO orders (id,customer_id,order_date,total_amount) VALUES (?,?,?,?)", orders)
    conn.commit(); conn.close(); print(f"Database created at {DB_PATH}")
if __name__ == "__main__": main()
