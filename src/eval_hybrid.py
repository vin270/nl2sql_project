import pandas as pd
from simple_generator import generate_sql as rule_sql
from model_generator import generate_sql_model as model_sql
from validator import execute_sql
from tqdm import tqdm


df = pd.read_csv("../data/dataset.csv")

hybrid_exact = 0
hybrid_exec = 0
total = len(df)

results = []

for i, row in tqdm(df.iterrows(), total=total):
    nl = row["nl"]
    gold = row["sql"]

    
    model_query = model_sql(nl)

    
    model_result = execute_sql(model_query)

    
    if isinstance(model_result, dict) and "error" in model_result:
        final_sql = rule_sql(nl)
        exec_result = execute_sql(final_sql)
        fallback_used = True
    else:
        final_sql = model_query
        exec_result = model_result
        fallback_used = False

    
    exact_match = (final_sql.strip().lower() == gold.strip().lower())
    if exact_match:
        hybrid_exact += 1

    
    gold_result = execute_sql(gold)
    exec_match = (exec_result == gold_result)
    if exec_match:
        hybrid_exec += 1

    results.append({
        "nl": nl,
        "gold": gold,
        "hybrid_sql": final_sql,
        "fallback": fallback_used,
        "exact": exact_match,
        "exec_match": exec_match
    })


print("\nHybrid Results on 140-query dataset:")
print(f"Hybrid exact match: {hybrid_exact}/{total} = {hybrid_exact/total*100:.2f}%")
print(f"Hybrid execution accuracy: {hybrid_exec}/{total} = {hybrid_exec/total*100:.2f}%")


out = pd.DataFrame(results)
out.to_csv("../results/eval_hybrid.csv", index=False)
print("Saved detailed hybrid evaluation to results/eval_hybrid.csv")
