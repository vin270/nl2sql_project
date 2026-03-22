from spider_utils import load_split
from collections import Counter

def main():
    examples = load_split("train")
    counts = Counter(ex["db_id"] for ex in examples)
    print("Available db_ids in Spider (train split):")
    for db_id, cnt in counts.most_common():
        print(f"{db_id}: {cnt} examples")

if __name__ == "__main__":
    main()
