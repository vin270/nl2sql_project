import csv
from simple_generator import generate_sql
from validator import execute_sql
def normalize_sql(s): return " ".join(s.lower().split())
def main():
    gold = []
    with open("../data/dataset.csv") as f:
        for row in csv.DictReader(f):
            gold.append((row["nl"], row["sql"]))
    exact = exec_ok = 0; total = len(gold)
    for nl, gold_sql in gold:
        pred = generate_sql(nl)
        if normalize_sql(pred) == normalize_sql(gold_sql): exact += 1
        res = execute_sql(pred)
        if "error" not in res: exec_ok += 1
    print(f"Exact match: {exact}/{total} = {exact/total:.2%}")
    print(f"Executable:  {exec_ok}/{total} = {exec_ok/total:.2%}")
if __name__ == "__main__": main()
