import json
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
SPIDER_DIR = os.path.join(BASE_DIR, "data", "spider")


def _load_json(name: str):
    path = os.path.join(SPIDER_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_tables():
    """Load tables.json (schema definitions)."""
    return _load_json("tables.json")


def load_split(split: str = "train"):
    """
    Load Spider split.
    split: 'train' or 'dev'
    Returns list of examples.
    """
    fname = "train_spider.json" if split == "train" else "dev.json"
    return _load_json(fname)


def get_schema_for_db(db_id: str, tables=None) -> str:
    """
    Build a simple human-readable schema text for a given db_id,
    using tables.json.
    """
    if tables is None:
        tables = load_tables()

    for t in tables:
        if t["db_id"] == db_id:
            lines = []
            table_names = t["table_names_original"]
            columns = t["column_names_original"]  # list of [table_idx, column_name]

            for table_idx, table_name in enumerate(table_names):
                cols = [col_name for ti, col_name in columns if ti == table_idx]
                # remove "*" pseudo-column if present
                cols = [c for c in cols if c != "*"]
                lines.append(f"{table_name}({', '.join(cols)})")

            return "\n".join(lines)

    return f"(schema not found for db_id={db_id})"


def sample_examples_for_db(db_id: str, split: str = "train", n: int = 5):
    """Get n random examples from a specific database id."""
    examples = load_split(split)
    subset = [e for e in examples if e["db_id"] == db_id]
    if not subset:
        raise ValueError(f"No Spider examples for db={db_id}")
    return random.sample(subset, min(n, len(subset)))
