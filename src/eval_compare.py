import csv
from simple_generator import generate_sql as rule_sql
from model_generator import generate_sql_model as model_sql
from validator import execute_sql
import pandas as pd

def normalize_sql(s: str) -> str:
    return " ".join(s.lower().split())

def main():
    print("🚀 Starting eval_compare.py", flush=True)

    gold = []
    with open("../data/dataset.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            gold.append((row["nl"], row["sql"]))

    total = len(gold)
    print(f"📂 Loaded {total} examples from dataset.csv", flush=True)

    exact_rule = exec_rule = 0
    exact_model = exec_model = 0

    
    saved_examples = []

    for i, (nl, gold_sql) in enumerate(gold, start=1):
        pred_r = rule_sql(nl)
        if normalize_sql(pred_r) == normalize_sql(gold_sql):
            exact_rule += 1

        res_r = execute_sql(pred_r)
        if "error" not in res_r:
            exec_rule += 1

        try:
            pred_m = model_sql(nl)
        except Exception as e:
            print(f"❌ Model error on example {i}: {e}", flush=True)
            pred_m = ""

        if pred_m:
            if normalize_sql(pred_m) == normalize_sql(gold_sql):
                exact_model += 1

            res_m = execute_sql(pred_m)
            if "error" not in res_m:
                exec_model += 1

        
        if i % 5 == 0 or i == total:
            print(f"✅ Processed {i}/{total} examples...", flush=True)

        
        if (
            i <= 5
            or (
                normalize_sql(pred_m) == normalize_sql(gold_sql)
                and normalize_sql(pred_r) != normalize_sql(gold_sql)
            )
        ):
            saved_examples.append({
                "i": i,
                "nl": nl,
                "gold": gold_sql,
                "rule": pred_r,
                "model": pred_m
            })

    
    print("\n📊 Results on domain dataset:")
    print(f"Rule-based exact:  {exact_rule}/{total} = {exact_rule/total:.2%}")
    print(f"Rule-based exec:   {exec_rule}/{total} = {exec_rule/total:.2%}")
    print(f"Model exact:       {exact_model}/{total} = {exact_model/total:.2%}")
    print(f"Model exec:        {exec_model}/{total} = {exec_model/total:.2%}")

    
    df = pd.DataFrame(saved_examples)
    df.to_csv("../results/eval_detailed.csv", index=False)
    print("\n📁 Saved detailed evaluation to results/eval_detailed.csv")

    
    print("\n🔍 Detailed Examples:\n")
    for ex in saved_examples:
        print("-----------")
        print(f"Example {ex['i']}")
        print(f"NL:    {ex['nl']}")
        print(f"Gold:  {ex['gold']}")
        print(f"Rule:  {ex['rule']}")
        print(f"Model: {ex['model']}")

if __name__ == "__main__":
    main()
