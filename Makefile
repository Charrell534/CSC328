all: client server

client:
	chmod +x client

server:
	chmod +x server

.PHONY: server client
