import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from simple_generator import generate_sql
from model_generator import generate_sql_model

def test_rule_generator_basic():
    sql = generate_sql("show all products")
    assert "SELECT" in sql.upper()

def test_model_generator_basic():
    sql = generate_sql_model("list all customers")
    assert isinstance(sql, str)
    assert "SELECT" in sql.upper()
