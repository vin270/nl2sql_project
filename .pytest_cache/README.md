Natural Language to SQL Interface (NL2SQL)

Overview

An AI-powered system that converts natural language queries into SQL
statements, enabling intuitive database interaction.

This improves accessibility for non-technical users by removing the need
to write SQL manually.

Originally developed as part of an MSc Software Engineering project at
City, University of London.

------------------------------------------------------------------------

Key Highlights

-   Built a hybrid AI system combining rule-based and transformer-based
    approaches
-   Designed and evaluated multiple SQL generation strategies
-   Achieved reliable query generation with validation and fallback
    mechanisms

------------------------------------------------------------------------

Features

-   Rule-based SQL query generation for deterministic outputs
-   Neural SQL generation using a fine-tuned T5 model
-   Hybrid validation system with intelligent fallback logic
-   Execution against a PostgreSQL database
-   Interactive user interface using Streamlit

------------------------------------------------------------------------

Technologies Used

-   Python
-   SQL (PostgreSQL)
-   Machine Learning (T5 Transformer Model)
-   Streamlit

------------------------------------------------------------------------

Project Structure

-   app.py – Streamlit user interface
-   src/simple_generator.py – Rule-based SQL generator
-   src/model_generator.py – Neural T5-based generator
-   src/validator.py – Hybrid validation logic
-   src/eval_compare.py – Rule vs neural evaluation
-   src/eval_hybrid.py – Hybrid model evaluation
-   dataset.json – Natural language to SQL dataset
-   schema.sql – Database schema

------------------------------------------------------------------------

How to Run

Run the application

streamlit run app.py

Quick start scripts

python src/create_db.py python src/demo.py python src/eval_compare.py

------------------------------------------------------------------------

Example

Input: “Show all employees with salary above 50000”

Generated SQL: SELECT * FROM employees WHERE salary > 50000;

------------------------------------------------------------------------

Model Information

-   Uses a fine-tuned T5-small transformer model
-   Model folder: t5-small-finetuned/ (optional)
-   If not included, the model can be downloaded automatically via
    HuggingFace

------------------------------------------------------------------------

Notes

-   The Spider dataset is not included due to size constraints
-   Only SELECT queries are supported for safety
-   Results presented in the dissertation are reproducible using
    included scripts

------------------------------------------------------------------------

Future Improvements

-   Support more complex SQL queries (JOIN, GROUP BY)
-   Improve model accuracy with larger datasets
-   Deploy as a web application

------------------------------------------------------------------------

Author

Vindya Ashok
MSc Software Engineering with Cloud Computing (Merit)
City, University of London
