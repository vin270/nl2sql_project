Author: Vindya Ashok
MSc Software Engineering (City, University of London)
Project Title: Natural Language to SQL Translation Using Deep Learning for Database Accessibility
This folder contains the full implementation of the hybrid NL2SQL system described in the accompanying dissertation. The system supports:
rule-based SQL generation
neural T5-small model generation
hybrid validation with fallback logic
execution against a PostgreSQL database
a Streamlit interface for user interaction

To start application:
streamlit run app.py

Quick Start
python src/create_db.py
python src/demo.py      # ask questions and see results
python src/eval_compare.py      # quick accuracy on toy dataset

Core Implementation
app.py – Streamlit UI
simple_generator.py – Rule-based SQL generator
model_generator.py – T5-small generator
validator.py – Hybrid SQL validator
eval_compare.py – Evaluation script for rule vs neural
eval_hybrid.py – Evaluation script for hybrid model
Data & Schema
dataset.json – 140 natural language → SQL pairs
schema.sql – PostgreSQL schema
Model (optional)
If the fine-tuned model folder is included, it will appear as t5-small-finetuned/.
If not included, the model can be reloaded automatically or downloaded using HuggingFace.

Note for assessors:
The Spider dataset is not included to keep submission size appropriate.
Only SELECT statements are allowed by design for safety.
All results shown in the dissertation are reproducible using the included evaluation scripts.
