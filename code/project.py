import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

# This part of the code is refrenced from the demo.py from the lab to set up the configrations
@st.cache
def get_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


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

def insert_db(sql: str):
    db_info = get_config()
    error_status = False
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.DatabaseError as error:
        error_status = True
    finally:
        conn.close()
        return error_status

def insert_clients(table_name):
    email = st.text_input("Email", "")
    name =  st.text_input("Name", "")
    phone = st.text_input("Phone", "")

    all_company_names_query = f"""
                                    SELECT name
                                    FROM companies;
                                """
    all_company_names = query_db(all_company_names_query)['name'].tolist()
    company_name = st.selectbox('Works for', all_company_names)

    if st.button('Submit'):
        table_query = f'INSERT INTO {table_name}(email, name, phone, company_name) VALUES (\'{email}\', \'{name}\', \'{phone}\', \'{company_name}\');'
        if insert_db(table_query):
            st.error("Cannot insert " + table_name + ". Please check your input!")
        else:
            st.success("Successfully insert into table " + table_name)

def insert_companies(table_name):
    name = st.text_input("Name", "")
    address =  st.text_input("Address", "")
    industry_type = st.text_input("Industry Type", "")
    within_network = st.selectbox("Within Network", [True, False])

    if st.button('Submit'):
        table_query = f'INSERT INTO {table_name}(name, address, industry_type, within_network) VALUES (\'{name}\', \'{address}\', \'{industry_type}\', \'{within_network}\');'
        if insert_db(table_query):
            st.error("Cannot insert " + table_name + ". Please check your input!")
        else:
            st.success("Successfully insert into table " + table_name)

def insert_cost_types(table_name):
    name = st.text_input("Name", "")
    unit_cost =  st.number_input("Unit Cost", min_value=0, value=0)
    discounted_unit_cost = st.number_input("Discounted Unit Cost", min_value=0, value=0)

    if st.button('Submit'):
        table_query = f'INSERT INTO {table_name}(name, unit_cost, discounted_unit_cost) VALUES (\'{name}\', \'{unit_cost}\', \'{discounted_unit_cost}\');'
        if insert_db(table_query):
            st.error("Cannot insert " + table_name + ". Please check your input!")
        else:
            st.success("Successfully insert into table " + table_name)

def insert_funding_method(table_name):
    funding_type = st.text_input("Funding Type", "")
    amount =  st.number_input("Amount", min_value=1, value=1)

    all_client_emails_query = f"""
                                    SELECT email
                                    FROM clients;
                                """
    all_client_emails = query_db(all_client_emails_query)['email'].tolist()
    client_email = st.selectbox('Funding belongs to', all_client_emails)

    if st.button('Submit'):
        table_query = f'INSERT INTO {table_name}(funding_type, amount, client_email) VALUES (\'{funding_type}\', \'{amount}\', \'{client_email}\');'
        if insert_db(table_query):
            st.error("Cannot insert " + table_name + ". Please check your input!")
        else:
            st.success("Successfully insert into table " + table_name)

def insert_instruments(table_name):
    instr_id = st.text_input("Instrument Id", "")
    name =  st.text_input("Name", "")

    if st.button('Submit'):
        table_query = f'INSERT INTO {table_name}(id, name) VALUES (\'{instr_id}\', \'{name}\');'
        if insert_db(table_query):
            st.error("Cannot insert " + table_name + ". Please check your input!")
        else:
            st.success("Successfully insert into table " + table_name)

def insert_members(table_name):
    mem_id = st.text_input("Member Id", "")
    name =  st.text_input("Name", "")
    job_title = st.text_input("Job Title", "")

    if st.button('Submit'):
        table_query = f'INSERT INTO {table_name}(id, name, job_title) VALUES (\'{mem_id}\', \'{name}\', \'{job_title}\');'
        if insert_db(table_query):
            st.error("Cannot insert " + table_name + ". Please check your input!")
        else:
            st.success("Successfully insert into table " + table_name)

def insert_samples(table_name):
    sample_id = st.text_input("Sample Id", "")
    name =  st.text_input("Name", "")
    sample_group = st.text_input("Sample Group", "")
    sample_type = st.text_input("Type", "")
    amount = st.number_input("Amount", min_value=1, value=1)
    amount_unit= st.text_input("Amount Unit", "")

    #Project input
    all_projects_title_query = f"""
                            SELECT title
                            FROM projects;
                        """
    all_projects_title = query_db(all_projects_title_query)['title'].tolist()
    projects_title = st.selectbox('This sample belongs to project', all_projects_title)

    projects_id_query = f"""
                        SELECT id
                        FROM projects
                        WHERE title = '{projects_title}';
                    """
    project_id = int(query_db(projects_id_query)['id'])

    if st.button('Submit'):
        table_query = f'INSERT INTO {table_name}(id, name, sample_group, type, amount, amount_unit, project_id) VALUES (\'{sample_id}\', \'{name}\', \'{sample_group}\', \'{sample_type}\', \'{amount}\', \'{amount_unit}\', \'{project_id}\');'
        if insert_db(table_query):
            st.error("Cannot insert " + table_name + ". Please check your input!")
        else:
            st.success("Successfully insert into table " + table_name)

def insert_sop_uses_instruments(table_name):

    #SOPs input
    all_sops_query = f"""
                            SELECT sop_description
                            FROM sops;
                        """
    all_sops_desc = query_db(all_sops_query)['sop_description'].tolist()
    sops_desc = st.selectbox('Standard Operating Protocols', all_sops_desc)

    sops_id_query = f"""
                        SELECT id
                        FROM sops
                        WHERE sop_description = '{sops_desc}';
                    """
    sop_id = int(query_db(sops_id_query)['id'])

    #Instrument input
    all_instruments_name_query = f"""
                            SELECT name
                            FROM instruments;
                        """
    all_instruments_name = query_db(all_instruments_name_query)['name'].tolist()
    instruments_name = st.selectbox('Instruments', all_instruments_name)

    instrument_id_query = f"""
                        SELECT id
                        FROM instruments
                        WHERE name = '{instruments_name}';
                    """
    instrument_id = int(query_db(instrument_id_query)['id'])

    if st.button('Submit'):
        table_query = f'INSERT INTO {table_name}(id, sop_id, inst_id) VALUES ((SELECT MAX(id) FROM {table_name})+1, \'{sop_id}\', \'{instrument_id}\');'
        st.write(table_query)
        if insert_db(table_query):
            st.error("Cannot insert " + table_name + ". Please check your input!")
        else:
            st.success("Successfully insert into table " + table_name)



def insert_projects(table_name):
    proj_id = st.text_input("Project Id", "")
    title =  st.text_input("Title", "")
    goal = st.text_input("Goal", "")
    proj_type = st.text_input("Type", "")
    status = st.selectbox("Status", ["In process", "Complete", "Failed"])

    #Client email input
    all_client_emails_query = f"""
                                    SELECT email
                                    FROM clients;
                                """
    all_client_emails = query_db(all_client_emails_query)['email'].tolist()
    client_email = st.selectbox('Requested by', all_client_emails)

    #SOPs input
    all_sops_query = f"""
                            SELECT sop_description
                            FROM sops;
                        """
    all_sops_desc = query_db(all_sops_query)['sop_description'].tolist()
    sops_desc = st.selectbox('Standard Operating Protocols', all_sops_desc)

    sops_id_query = f"""
                        SELECT id
                        FROM sops
                        WHERE sop_description = '{sops_desc}';
                    """
    sop_id = int(query_db(sops_id_query)['id'])

    #Members input
    all_members_query = f"""
                            SELECT name
                            FROM members;
                        """
    all_members_name = query_db(all_members_query)['name'].tolist()
    members_name = st.selectbox('Assigned to', all_members_name)

    members_id_query = f"""
                        SELECT id
                        FROM members
                        WHERE name = '{members_name}';
                    """
    member_id = int(query_db(members_id_query)['id'])

    #Cost types input
    all_cost_types_query = f"""
                            SELECT name
                            FROM cost_types;
                        """
    all_cost_types_name = query_db(all_cost_types_query)['name'].tolist()
    cost_type = st.selectbox('Cost types', all_cost_types_name)


    if st.button('Submit'):
        table_query = f'INSERT INTO {table_name}(id, title, goal, type, status, client_email, sop_id, member_id, cost_type) VALUES (\'{proj_id}\', \'{title}\', \'{goal}\', \'{proj_type}\', \'{status}\', \'{client_email}\', \'{sop_id}\', \'{member_id}\', \'{cost_type}\');'
        st.write(table_query)
        if insert_db(table_query):
            st.error("Cannot insert " + table_name + ". Please check your input!")
        else:
            st.success("Successfully insert into table " + table_name)

def insert_sops(table_name):
    sop_id = st.text_input("SOP Id", "")
    sop_description =  st.text_input("SOP Description", "")

    if st.button('Submit'):
        table_query = f'INSERT INTO {table_name}(id, SOP_description) VALUES (\'{sop_id}\', \'{sop_description}\');'
        st.write(table_query)
        if insert_db(table_query):
            st.error("Cannot insert " + table_name + ". Please check your input!")
        else:
            st.success("Successfully insert into table " + table_name)


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
    sample_exist_check_query = f"SELECT * FROM samples WHERE project_id = {project_ID}"
    df_check = query_db(sample_exist_check_query)
    if df_check.empty:
        st.error("This project has no sample assgined to it, please add the sample information in the sample table!")
    else:
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
query_type = st.radio('Select query type for lab memeber workload information', ['All Projects', 'Historical Projects', 'Open Projects','Memebers without project assignment currently'])
if query_type == 'Historical Projects':
    all_members = ''
    output = ', COUNT(p.id) AS processed_project_count'
    constraint = "WHERE p.status = 'Complete' OR p.status = 'Failed'"

elif query_type == 'Open Projects':
    all_members = ''
    output = ', COUNT(p.id) AS open_project_count'
    constraint = "WHERE p.status = 'In process'"

elif query_type == 'Memebers without project assignment currently':
    all_members = "(SELECT m.name, m.id, m.job_title AS title FROM members m) EXCEPT"
    output = ''
    constraint = "WHERE p.status = 'In process'"

else:
    all_members = ''
    output = ', COUNT(p.id) AS all_project_count'
    constraint = ''

project_assignment_query = f"""{all_members}    
                    (SELECT m.name, m.id, m.job_title AS title {output}
                    FROM members m
                    JOIN projects p
                    ON m.id = p.member_id
                    {constraint}
                    GROUP BY m.name, m.id, m.job_title
                    ORDER BY COUNT(p.id) DESC);
                    """

df6 = query_db(project_assignment_query)
st.table(df6)

if query_type != 'Memebers without project assignment currently':
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

'## Insert information'
all_table_names_query = "SELECT table_name FROM information_schema.tables WHERE table_schema ='public';"
all_table_names = query_db(all_table_names_query)['table_name'].tolist()
table_name = st.selectbox('Choose a table to insert the data', all_table_names)
options = {"clients" : insert_clients,
            "companies": insert_companies,
            "cost_types": insert_cost_types,
            "members": insert_members,
            "instruments": insert_instruments,
            "funding_method": insert_funding_method,
            "projects": insert_projects,
            "samples": insert_samples,
            "sop_uses_instruments": insert_sop_uses_instruments,
            'sops': insert_sops
}
options[table_name](table_name)