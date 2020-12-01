DROP TABLE Clients CASCADE;
DROP TABLE Financial_Transactions CASCADE;
DROP TABLE Projects CASCADE;
DROP TABLE Samples CASCADE;
DROP TABLE SOPs;
DROP TABLE Companies;
DROP TABLE Members;
DROP TABLE Cost_Types;
DROP TABLE Instruments;


create table SOPs
(
	id varchar(32) primary key,
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
	id varchar(32) primary key,
	name varchar(128) not null,
	job_title varchar(128)
);

create table Cost_Types
(
	name varchar(128) primary key,
	cost integer
);

create table Instruments
(
	id varchar(32) primary key,
	name varchar(128)
);

create table Clients
(
	email varchar(64) primary key,
	name varchar(128) not null,
	phone varchar(32),
	company_name varchar(32) not null,
	foreign key (company_name) references Companies(name)
);

create table Financial_Transactions
(
	time date,
	method varchar(32),
	amount integer,
	client_email varchar(64),
	primary key (client_email, time),
	foreign key (client_email) references Clients(email) on delete cascade
);

create table Projects
(
	id varchar(32) primary key,
	title varchar(128) not null,
	goal varchar (128),
	type varchar(32),
	client_email varchar(64) not null,
	foreign key (client_email) references Clients(email),
	sop_id varchar(32) not null,
	foreign key (sop_id) references SOPs(id),
	member_id varchar(32) not null,
	foreign key(member_id) references Members(id),
	cost_type varchar(128) not null,
	foreign key(cost_type) references Cost_Types(name)
);

create table Samples
(
	id varchar(32) primary key,
	name varchar(128) not null,
	sample_group varchar(128),
	type varchar(32),
	amount integer,
	amount_unit varchar(32),
	project_id varchar(32) not null,
	foreign key (project_id) references Projects(id)
);