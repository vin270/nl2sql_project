import os
import csv
from typing import List, Dict

import torch
from torch.utils.data import Dataset

from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    TrainingArguments,
    Trainer,
)

print("🚀 Starting train_t5.py...", flush=True)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
MAIN_DATASET = os.path.join(DATA_DIR, "dataset.csv")
SPIDER_DATASET = os.path.join(DATA_DIR, "spider_subset.csv")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "models", "t5_nl2sql")

print(f"DATA_DIR = {DATA_DIR}", flush=True)
print(f"MAIN_DATASET = {MAIN_DATASET}", flush=True)
print(f"OUTPUT_DIR = {OUTPUT_DIR}", flush=True)


class NL2SQLDataset(Dataset):
    def __init__(self, rows: List[Dict[str, str]], tokenizer, max_input_len=64, max_target_len=128):
        self.tokenizer = tokenizer
        self.rows = rows
        self.max_input_len = max_input_len
        self.max_target_len = max_target_len

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        ex = self.rows[idx]
        nl = ex["nl"]
        sql = ex["sql"]

        src_text = f"translate English to SQL: {nl}"

        src_enc = self.tokenizer(
            src_text,
            max_length=self.max_input_len,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )
        tgt_enc = self.tokenizer(
            sql,
            max_length=self.max_target_len,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

        return {
            "input_ids": src_enc["input_ids"].squeeze(0),
            "attention_mask": src_enc["attention_mask"].squeeze(0),
            "labels": tgt_enc["input_ids"].squeeze(0),
        }


def load_csv(path: str) -> List[Dict[str, str]]:
    print(f"📂 Loading CSV from: {path}", flush=True)
    rows = []
    if not os.path.exists(path):
        print("⚠️ File does not exist.", flush=True)
        return rows
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if "nl" in r and "sql" in r and r["nl"].strip() and r["sql"].strip():
                rows.append({"nl": r["nl"].strip(), "sql": r["sql"].strip()})
    print(f"✅ Loaded {len(rows)} rows from {path}", flush=True)
    return rows


def main():
    print("📁 Ensuring output directory exists...", flush=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("📥 Loading main dataset...", flush=True)
    rows = load_csv(MAIN_DATASET)

    print("📥 Attempting to load Spider subset (optional)...", flush=True)
    spider_rows = load_csv(SPIDER_DATASET)
    if spider_rows:
        print(f"✅ Loaded {len(spider_rows)} Spider examples, adding to training set.", flush=True)
        rows.extend(spider_rows)
    else:
        print("ℹ️ No Spider subset found or empty. Training only on main dataset.", flush=True)

    if not rows:
        raise RuntimeError("❌ No training data found. Check data/dataset.csv (and optional data/spider_subset.csv).")

    print(f"📊 Total training examples: {len(rows)}", flush=True)

    split_idx = int(0.8 * len(rows))
    train_rows = rows[:split_idx]
    val_rows = rows[split_idx:]

    print(f"📊 Train: {len(train_rows)}, Val: {len(val_rows)}", flush=True)

    model_name = "t5-small"
    print(f"📦 Loading tokenizer and model: {model_name}", flush=True)
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    print("🧹 Moving model to device...", flush=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print(f"📟 Using device: {device}", flush=True)

    train_ds = NL2SQLDataset(train_rows, tokenizer)
    val_ds = NL2SQLDataset(val_rows, tokenizer)

    print("⚙️ Setting up TrainingArguments...", flush=True)
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        learning_rate=3e-4,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_steps=10,
        load_best_model_at_end=True,
        save_total_limit=2,
        remove_unused_columns=False,
        logging_dir=os.path.join(OUTPUT_DIR, "logs"),
    )

    def compute_metrics(eval_pred):
        return {}

    print("🚂 Initialising Trainer...", flush=True)
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    print("🏁 Starting training loop...", flush=True)
    trainer.train()
    print("✅ Training complete, saving model...", flush=True)

    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"🎉 Model and tokenizer saved to {OUTPUT_DIR}", flush=True)


if __name__ == "__main__":
    main()
