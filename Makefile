all: server client

server: server.py
	chmod +x server.py

client: client.py
	cp client.py client
	chmod +x client
.PHONY: clean
clean:
	rm -f client
