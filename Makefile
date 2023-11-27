all: run

client: client
	chmod +x client

server: server
	chmod +x server

.PHONY: run
run: server client
	./server
	./client
