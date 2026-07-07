import json
import streamlit as st


st.title("Behavioral Risk Factor Surveillance System")

st.sidebar.title("Table Selection")
config_path = 'config/allowed_tables.json'

with open(config_path, 'r') as f:
    tables_config = json.load(f)

# Fetch the tables for the given schema
allowed_tables = tables_config['ALLOWED_STAGING_TABLES']

selected_table = st.sidebar.selectbox(label='Select a table:', index=None, placeholder='None', options=tables_config['ALLOWED_STAGING_TABLES'], )

if selected_table is not None:
    if selected_table not in allowed_tables:
        st.error("Selected table is not allowed.")
        st.stop()

    # Initialize connection.
    conn = st.connection("postgresql", type="sql")

    if selected_table == 'behavioral_risk_factor_surveillance_system':
        question_query = f"""SELECT *
                            FROM staging.behavioral_risk_factor_surveillance_system_questions;"""
        

        brfss_question_df = conn.query(sql=question_query)

        selected_columns = st.sidebar.multiselect(
            label='Select one or more questions:',
            options=brfss_question_df['Question'].tolist()
        )