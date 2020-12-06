import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

# This part of the code is refrenced from the demo.py in class to set up the configrations
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

# main part of the web app
'# Metabolomics Core Laboratory Project Mangement System'

'## Table overview'
all_table_names_query = "SELECT table_name FROM information_schema.tables WHERE table_schema ='public';"
all_table_names = query_db(all_table_names_query)['table_name'].tolist()
table_name = st.selectbox('Choose a table to show all the data', all_table_names)
if table_name:
    table_query = f'select * from {table_name};'
    df1 = query_db(table_query)
    st.table(df1)


'## Sample ID lookup'
sample_ID = st.number_input("Please enter the sample ID here", min_value = 1, step=1)
if sample_ID:
    sample_query = f"""
                    SELECT s.id, s.name,s.sample_group, s.type, s.amount, s.amount_unit, 
                    p.id AS project_id, p.title AS project_title, p.type As project_type, p.status AS project_status, 
                    c.name AS cliet_name,
                    m.name AS project_assgigned_to 
                    FROM samples s
                    JOIN projects p
                    ON s.project_id = p.id
                    JOIN clients c
                    ON p.client_email = c.email
                    JOIN members m
                    on p.member_id = m.id
                    WHERE s.id = {sample_ID};
                        """
    df2 = query_db(sample_query)
    if df2.empty:
        st.text("No matching sample ID found in database!")
    else:
        st.table(df2)

'## Project ID lookup'
project_ID = st.number_input("Please enter the project ID here", min_value = 1, step=1)
if project_ID:
    isDiscounted_query = f"""
                            SELECT cp.within_network
                            FROM projects p
                            JOIN clients c
                            ON p.client_email = c.email
                            JOIN companies cp
                            ON c.company_name = cp.name
                            WHERE p.id = {project_ID}
                            """
    df3 = query_db(isDiscounted_query)
    if df3.empty:
        st.text("No matching Project ID found in database!")
    else:
        isDiscounted = df3['within_network'][0]

        if isDiscounted == True :
            unit_cost_type = 'discounted_unit_cost'
            cost_note = "_discounted"
        else:
            unit_cost_type = 'unit_cost'
            cost_note = "_full_price"

        project_query = f"""
                        SELECT p.id, p.status, p.title, p.goal, p.type, p.sop_id,c.name AS client_name, m.name AS Assgined_to,
                        COUNT(*) AS Total_Samples,
                        (COUNT(*) * ct.{unit_cost_type}) AS Total_Cost{cost_note}
                        FROM projects p
                        JOIN cost_types ct
                        ON p.cost_type = ct.name
                        JOIN clients c
                        ON p.client_email = c.email
                        JOIN members m
                        ON p.member_id = m.id
                        JOIN samples s
                        ON p.id = s.project_id
                        WHERE p.id = {project_ID}
                        GROUP BY p.id, c.name, m.name, ct.{unit_cost_type};
                        """
        df4 = query_db(project_query)
        st.table(df4) 

        client_name = df4['client_name'][0]
        project_cost = df4[f'total_cost{cost_note}'][0]
        client_avaliable_funding_query = f"""SELECT c.name, sum(fm.amount) AS toatal_funding_amount
                                FROM clients c
                                JOIN funding_method fm
                                ON c.email = fm.client_email
                                WHERE c.name = '{client_name}'
                                GROUP BY c.name;
                                """
        client_avaliable_funding = query_db(client_avaliable_funding_query)['toatal_funding_amount'][0]
        if project_cost > client_avaliable_funding:
            st.warning('Client does not have enough funding for this project')
        else:
            st.success('Project fully funded')

        see_all_samples = st.button("See all samples")

        if see_all_samples:
            see_all_samples_query = f"""
                                    SELECT s.id, s.name, s.sample_group, s.type, s.amount, s.amount_unit
                                    FROM samples s
                                    WHERE s.project_id = {project_ID};
                                    """
            df5 = query_db(see_all_samples_query)
            st.table(df5)

'## Lab Members Project Assginment'
query_type = st.radio('Select query type for lab memeber workload information', ['All Projects', 'Historical Projects', 'Open Projects'])
if query_type == 'Historical Projects':
    output = 'processed_project_count'
    constraint = "WHERE p.status = 'Complete' OR p.status = 'Failed'"
elif query_type == 'Open Projects':
    output = 'open_project_count'
    constraint = "WHERE p.status = 'In process'"
else:
    output = 'all_project_count'
    constraint = ''

project_assignment_query = f"""SELECT m.name, m.id, m.job_title, COUNT(*) AS {output}
                    FROM members m
                    JOIN projects p
                    ON m.id = p.member_id
                    {constraint}
                    GROUP BY m.name, m.id, m.job_title
                    ORDER BY {output} DESC;
                    """

df6 = query_db(project_assignment_query)
st.table(df6)

show_detail = st.button('Show detail')
if show_detail:
    show_detail_query = f"""SELECT m.name, m.job_title, p.id AS project_id, p.title, p.goal, p.status
                    FROM members m
                    JOIN projects p
                    ON m.id = p.member_id
                    {constraint}
                    ORDER BY m.name
                    """
    df7= query_db(show_detail_query)
    st.table(df7)

'## Instrument Status'
instrument_query_options = st.selectbox('Please select one instrument usage report: ',['Historical instrument usage information', 'Current instrument usage information', 'List all unused instruments currently'])
if instrument_query_options == 'Historical instrument usage information':
    instrument_usage_query = """SELECT i.name, count(i.name) AS num_time_used
                                FROM instruments i
                                JOIN sop_uses_instruments sui
                                ON i.id = sui.inst_id
                                JOIN projects p
                                ON sui.sop_id = p.sop_id
                                GROUP BY i.name
                                ORDER BY num_time_used DESC;"""
elif instrument_query_options == 'Current instrument usage information':
    instrument_usage_query = """SELECT i.name, count(i.name) AS num_time_used
                                FROM instruments i
                                JOIN sop_uses_instruments sui
                                ON i.id = sui.inst_id
                                JOIN projects p
                                ON sui.sop_id = p.sop_id
                                WHERE p.status = 'In process'
                                GROUP BY i.name
                                ORDER BY num_time_used DESC;"""

else:
    instrument_usage_query = """(SELECT i.name
                                FROM instruments i)
                                EXCEPT
                                (SELECT i.name
                                FROM instruments i
                                JOIN sop_uses_instruments sui
                                ON i.id = sui.inst_id
                                JOIN projects p
                                ON sui.sop_id = p.sop_id
                                WHERE p.status = 'In process');
                                """
df8= query_db(instrument_usage_query)
st.table(df8)