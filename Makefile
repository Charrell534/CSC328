all: run

client: client
	chmod +x client

server: server
	chmod +x server

.PHONY: run
run: server client
	./server
	@read -p "Enter the number of clients: " num; \
	for i in $$(seq $$num); do \
		./client; \
	done

