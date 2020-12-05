import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

@st.cache
def get_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    db_info = get_config()
    conn = psycopg2.connect(**db_info)
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    conn.commit()
    cur.close()
    conn.close()
    df = pd.DataFrame(data=data, columns=column_names)

    return df


'# Metabolomics Core Laboratory Project Mangement system'

all_table_names_query = "SELECT table_name FROM information_schema.tables WHERE table_schema ='public';"
all_table_names = query_db(all_table_names_query)['table_name'].tolist()
table_name = st.selectbox('Choose a table to show all the data', all_table_names)
if table_name:
    sql_table = f'select * from {table_name};'
    df = query_db(sql_table)
    st.dataframe(df)

