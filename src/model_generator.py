# model_generator.py
import os
from typing import Optional

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "..", "models", "t5_nl2sql")

_tokenizer = None
_model = None


def _load_model():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        if not os.path.exists(MODEL_DIR):
            raise RuntimeError(
                f"Model directory {MODEL_DIR} not found. "
                "Train the model first with train_t5.py."
            )
        _tokenizer = T5Tokenizer.from_pretrained(MODEL_DIR)
        _model = T5ForConditionalGeneration.from_pretrained(MODEL_DIR)
        _model.eval()
    return _tokenizer, _model


def generate_sql_model(nl: str, max_length: int = 64) -> str:
    """
    Generate SQL from natural language using the fine-tuned T5 model.
    """
    tokenizer, model = _load_model()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    prompt = f"translate English to SQL: {nl}"
    enc = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64,
    ).to(device)

    with torch.no_grad():
        output_ids = model.generate(
            **enc,
            max_length=max_length,
            num_beams=4,
            early_stopping=True,
        )

    sql = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return sql.strip()
