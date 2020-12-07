DROP TABLE IF EXISTS Funding_Method CASCADE; 
DROP TABLE IF EXISTS Samples CASCADE; 
DROP TABLE IF EXISTS Projects CASCADE;
DROP TABLE IF EXISTS Clients CASCADE;
DROP TABLE IF EXISTS SOP_Uses_Instruments CASCADE;
DROP TABLE IF EXISTS SOPs;
DROP TABLE IF EXISTS Companies;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS Cost_Types;
DROP TABLE IF EXISTS Instruments;


create table SOPs
(
	id integer primary key,
	SOP_description varchar(1024)
);

create table Companies
(
	name varchar(128) primary key,
	address varchar(128),
	industry_type varchar(64),
	within_network boolean not null
);

create table Members
(
	id integer primary key,
	name varchar(128) not null,
	job_title varchar(128)
);

create table Cost_Types
(
	name varchar(128) primary key,
	unit_cost integer,
	discounted_unit_cost integer
);

create table Instruments
(
	id integer primary key,
	name varchar(128)
);

create table Clients
(
	email varchar(64) primary key,
	name varchar(128) not null,
	phone varchar(32),
	company_name varchar(1024) not null,
	foreign key (company_name) references Companies(name)
);

create table Funding_Method
(
	funding_type varchar(120),
	amount integer,
	client_email varchar(64),
	primary key (client_email, funding_type),
	foreign key (client_email) references Clients(email) on delete cascade
);

create table Projects
(
	id integer primary key,
	title varchar(128) not null,
	goal varchar (1024),
	type varchar(1024),
	status varchar(34),
	client_email varchar(128) not null,
	foreign key (client_email) references Clients(email),
	sop_id integer not null,
	foreign key (sop_id) references SOPs(id),
	member_id integer not null,
	foreign key(member_id) references Members(id),
	cost_type varchar(1024) not null,
	foreign key(cost_type) references Cost_Types(name)
	
);

create table Samples
(
	id integer primary key,
	name varchar(128) not null,
	sample_group varchar(128),
	type varchar(32),
	amount integer,
	amount_unit varchar(32),
	project_id integer not null,
	foreign key (project_id) references Projects(id)
);

create table SOP_Uses_Instruments
(
	id integer primary key,
	sop_id integer,
	inst_id integer,
	foreign key (sop_id) references SOPs(id) on delete cascade,
	foreign key (inst_id) references Instruments(id) on delete cascade
);

-- Import dummy data.
\COPY SOPs FROM 'SOPs.csv' DELIMITER ',' CSV HEADER;
\COPY Companies FROM 'Companies.csv' DELIMITER ',' CSV HEADER;
\COPY Members FROM 'Members.csv' DELIMITER ',' CSV HEADER;
\COPY Cost_Types FROM 'Cost_Types.csv' DELIMITER ',' CSV HEADER;
\COPY Instruments FROM 'Instruments.csv' DELIMITER ',' CSV HEADER;
\COPY Clients FROM 'Clients.csv' DELIMITER ',' CSV HEADER;
\COPY Funding_Method FROM 'Funding_Method.csv' DELIMITER ',' CSV HEADER;
\COPY Projects FROM 'Projects.csv' DELIMITER ',' CSV HEADER;
\COPY Samples FROM 'Samples.csv' DELIMITER ',' CSV HEADER;
\COPY SOP_Uses_Instruments FROM 'SOP_Uses_Instruments.csv' DELIMITER ',' CSV HEADER;

