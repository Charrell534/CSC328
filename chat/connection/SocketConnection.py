import socket


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def start_client(self):
        self.socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send_message(self, message):
        message = message.encode('utf-8')
        self.socket.sendall(len(message).to_bytes(4, byteorder='big') + message)

    def receive_message(self):
        length_bytes = self.socket.recv(4)
        if not length_bytes:
            return None
        length = int.from_bytes(length_bytes, byteorder='big')
        data = self.socket.recv(length).decode('utf-8')
        return data

    def close(self):
        self.socket.close()
