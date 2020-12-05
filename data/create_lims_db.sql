DROP TABLE IF EXISTS Founding_Method CASCADE; 
DROP TABLE IF EXISTS Samples CASCADE; 
DROP TABLE IF EXISTS Projects CASCADE;
DROP TABLE IF EXISTS Clients CASCADE;
DROP TABLE IF EXISTS SOP_uses_Instruments CASCADE;
DROP TABLE IF EXISTS SOPs;
DROP TABLE IF EXISTS Companies;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS Cost_Types;
DROP TABLE IF EXISTS Instruments;


create table SOPs
(
	id INTEGER primary key,
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
	id INTEGER primary key,
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
	id INTEGER primary key,
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

create table Founding_Method
(
	funding_type VARCHAR(120),
	amount integer,
	client_email varchar(64),
	primary key (client_email, funding_type),
	foreign key (client_email) references Clients(email) on delete cascade
);

create table Projects
(
	id INTEGER primary key,
	title varchar(128) not null,
	goal varchar (1024),
	type varchar(1024),
	status varchar(34),
	client_email varchar(128) not null,
	foreign key (client_email) references Clients(email),
	sop_id INTEGER not null,
	foreign key (sop_id) references SOPs(id),
	member_id INTEGER not null,
	foreign key(member_id) references Members(id),
	cost_type varchar(1024) not null,
	foreign key(cost_type) references Cost_Types(name)
	
);

create table Samples
(
	id INTEGER primary key,
	name varchar(128) not null,
	sample_group varchar(128),
	type varchar(32),
	amount integer,
	amount_unit varchar(32),
	project_id INTEGER not null,
	foreign key (project_id) references Projects(id)
);

create table SOP_uses_instruments
(
	id INTEGER,
	sop_id INTEGER,
	inst_id INTEGER,
	foreign key (sop_id) references SOPs(id) on delete cascade,
	foreign key (inst_id) references Instruments(id) on delete cascade
);


\COPY SOPs FROM 'SOPs.csv' DELIMITER ',' CSV HEADER;
\COPY Companies FROM 'Companies.csv' DELIMITER ',' CSV HEADER;
\COPY Members FROM 'Members.csv' DELIMITER ',' CSV HEADER;
\COPY Cost_Types FROM 'Cost_Types.csv' DELIMITER ',' CSV HEADER;
\COPY Instruments FROM 'Instruments.csv' DELIMITER ',' CSV HEADER;
\COPY Clients FROM 'Clients.csv' DELIMITER ',' CSV HEADER;
\COPY Founding_Method FROM 'Founding_Method.csv' DELIMITER ',' CSV HEADER;
\COPY Projects FROM 'Projects.csv' DELIMITER ',' CSV HEADER;
\COPY Samples FROM 'Samples.csv' DELIMITER ',' CSV HEADER;
\COPY SOP_uses_instruments FROM 'SOP_uses_Instruments.csv' DELIMITER ',' CSV HEADER;

