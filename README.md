# LIMS

Laboratory information management system (LIMS) will allow the lab members to track sample storage, project type, cost, methods used to process the projects, instrument information, client information, and lab member information. 

## Requirement
_Python 3\
_PostgreSQL 12\
_Streamlit

## Installation

Use Makefile located in setup-scripts folder to initialize database.
(Note: PostgreSQL 12 must be installed, up and running)
```bash
cd setup-scripts
```

Create database.
```bash
createdb your-database-name
```

Open Makefile and modify your database environment.
```bash
USERNAME=your-postgres-username
DB=your-database-name
PORT=your-port (ex: 5432)
```

Create schema.
```bash
make create
```

Populate data into schema (Note: All data are just random samples which located under data/sample_data_csv) .
```bash
make populate
```
Open database.ini in main folder and modify Streamlit environment for connection with PostgreSQL.
```bash
[postgresql]
host=localhost
port=yourdbport
dbname=yournetid-db
user=yournetid
```

Run the project by running project.py located in the main folder.
```bash
streamlit run project.py
```

## Contributing
Created by Duc Tran and Yik Siu.

## License
[MIT](https://choosealicense.com/licenses/mit/)
