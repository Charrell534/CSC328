all: client server

client:
	chmod +x client

server:
	chmod +x server

.PHONY: run server client
run_client: client
	@read -p "Enter the number of clients: " num; \
	for i in $$(seq $$num); do \
		./client; \
	done
run_server:
	./server
