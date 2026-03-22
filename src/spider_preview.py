from spider_utils import load_split

def main():
    examples = load_split("train")
    if not examples:
        print("No Spider examples found in train_spider.json")
        return

    print("Showing first 5 examples from Spider (train split):")

    for i, ex in enumerate(examples[:5], start=1):
        print(f"\nExample {i}:")
        print("DB ID:   ", ex.get("db_id"))
        print("Question:", ex.get("question"))
        print("SQL:     ", ex.get("query"))

if __name__ == "__main__":
    main()
