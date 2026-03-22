import streamlit as st

from simple_generator import generate_sql as rule_generate_sql
from model_generator import generate_sql_model
from validator import execute_sql


st.set_page_config(page_title="NL2SQL Demo", page_icon="🧠")
st.title("🧠 Natural Language to SQL Demo")

st.write(
    "Enter a natural language question below. "
    "The system will generate SQL using either the rule-based approach, the fine-tuned T5 model, "
    "or both. Then it will validate and execute the SQL on the sample database."
)


nl_query = st.text_input("Your question:", "show all customers")

mode = st.radio(
    "SQL generator:",
    ["Rule-based", "Model (T5)", "Both"],
    index=0,
)



if st.button("Run"):
    sqls = []

    
    if mode in ("Rule-based", "Both"):
        sql_rule = rule_generate_sql(nl_query)
        sqls.append(("Rule-based", sql_rule))

    
    if mode in ("Model (T5)", "Both"):
        try:
            model_query = generate_sql_model(nl_query)
        except Exception as e:
            st.error(f"Model error: {e}")
            model_query = None

        if model_query:
            st.subheader("Model (T5) SQL")
            st.code(model_query, language="sql")

            model_result = execute_sql(model_query)


            if "error" in model_result and mode == "Model (T5)":
                st.warning("Model SQL failed to execute. Falling back to rule-based query.")
                fallback_sql = rule_generate_sql(nl_query)
                st.code(fallback_sql, language="sql")
                model_result = execute_sql(fallback_sql)


    #   DISPLAY RESULTS

    for label, sql in sqls:
        st.subheader(f"{label} SQL")
        st.code(sql, language="sql")

        result = execute_sql(sql)

        if "error" in result:
            st.error(result["error"])
        else:
            cols = result["columns"]
            rows = result["rows"]

            if not rows:
                st.info("No rows returned for this query.")
            else:
                st.write("Results:")
                st.dataframe([dict(zip(cols, row)) for row in rows])

