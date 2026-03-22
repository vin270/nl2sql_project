from simple_generator import generate_sql
from validator import execute_sql
def main():
    print("NL2SQL Demo. Type a question (e.g., 'show all customers'). Ctrl+C to quit.")
    while True:
        try:
            nl = input("\nYour question: ")
            sql = generate_sql(nl)
            print("Generated SQL:", sql)
            result = execute_sql(sql)
            if "error" in result:
                print("Error:", result["error"])
            else:
                cols = result["columns"]; rows = result["rows"]
                print("Results:"); print(cols)
                for r in rows: print(r)
        except KeyboardInterrupt:
            print("\nBye."); break
if __name__ == "__main__":
    main()
