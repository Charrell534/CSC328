all: server client

server: server.py
	chmod +x server.py

client: client.py
	chmod +x client.py
