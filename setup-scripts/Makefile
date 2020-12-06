USERNAME=ductran
DB=lims-db
PORT=5432

all: create populate

create:
	./create-db $(DB)

populate:
	./populate-db $(USERNAME) $(DB) $(PORT)
