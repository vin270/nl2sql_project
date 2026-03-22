import sqlite3, os, re
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'shop.db')
BLOCKED = ["insert","update","delete","drop","create","alter","attach","replace","vacuum","pragma"]
def is_safe_select(sql: str) -> bool:
    s = sql.strip().lower()
    if not s.startswith("select"):
        return False
    for kw in BLOCKED:
        if re.search(rf"\b{kw}\b", s):
            return False
    return True
def execute_sql(sql: str):
    if not is_safe_select(sql):
        return {"error":"Only safe SELECT queries are allowed."}
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        conn.close()
        return {"columns": cols, "rows": rows}
    except Exception as e:
        return {"error": str(e)}
