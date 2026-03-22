import re

def generate_sql(question: str) -> str:
    """
    Improved rule-based SQL generator.
    Uses keyword detection, simple column extraction, numeric filtering,
    and table selection for the project's fixed schema.
    Always returns valid SQL as a fallback.
    """

    try:
        q = question.lower()


        # 1. TABLE SELECTION
        if "customer" in q:
            table = "customers"
        elif "order" in q:
            table = "orders"
        elif "product" in q:
            table = "products"
        else:
            table = "products"  


        # 2. NUMERIC FILTERS

        number_match = re.search(r"(\d+(\.\d+)?)", q)
        value = number_match.group(1) if number_match else None

        if value and table == "products" and (
            "less than" in q or "cheaper than" in q or "under" in q
        ):
            return f"SELECT id, name, price FROM products WHERE price < {value};"
        
        if value and table == "products" and (
            "greater than" in q or "above" in q or "more than" in q
        ):
            return f"SELECT id, name, price FROM products WHERE price > {value};"

        if table == "orders" and value and ("customer" in q or "customer id" in q):
            return f"SELECT id, customer_id, order_date, total_amount FROM orders WHERE customer_id = {value};"

        # JOIN RULES (valid for schema)
 

        if ("customer" in q and "order" in q) or "customers with orders" in q or "orders with customers" in q:
            return """
                SELECT customers.id AS customer_id,
                    customers.name,
                    customers.city,
                    orders.id AS order_id,
                    orders.order_date,
                    orders.total_amount
                FROM customers
                JOIN orders ON customers.id = orders.customer_id;
            """


        # 3 COLUMN EXTRACTION

        columns_map = {
            "name": "name",
            "names": "name",
            "id": "id",
            "ids": "id",
            "price": "price",
            "prices": "price",
            "city": "city",
            "cities": "city",
            "date": "order_date",
            "total": "total_amount",
            "amount": "total_amount"
        }

        detected_cols = []

        for word in q.split():
            if word in columns_map:
                detected_cols.append(columns_map[word])


        if detected_cols:
            col_str = ", ".join(sorted(set(detected_cols)))
            return f"SELECT {col_str} FROM {table};"

        # 4 CANNED RULES

        if "all" in q or "list" in q or "show" in q:
            if table == "customers":
                return "SELECT id, name, city FROM customers;"
            if table == "products":
                return "SELECT id, name, price FROM products;"
            if table == "orders":
                return "SELECT id, customer_id, order_date, total_amount FROM orders;"

        
        return f"SELECT * FROM {table};"

    except Exception as e:
        print(f"[ERROR] simple_generator.py - Failed to generate SQL: {e}")
        return "SELECT * FROM products;"
