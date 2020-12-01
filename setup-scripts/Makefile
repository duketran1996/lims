USERNAME=your-postgres-username
DB=your-database-name
PORT=your-port (ex: 5432)

all: create populate

create:
	./create-db $(DB)

populate:
	./populate-db $(USERNAME) $(DB) $(PORT)
