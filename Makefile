all: server client

server:
	chmod +x start.sh

client:
	chmod +x client.py

clean:
	chmod -x start.sh
	chmod -x client.py
