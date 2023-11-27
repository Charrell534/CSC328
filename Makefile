all: run


server: server_test
	chmod +x server_test

.PHONY: run
run: server
	./server_test
