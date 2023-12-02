import json
import socket

from multipledispatch import dispatch

from chat.exceptions.Exceptions import ImplementationError


class Conn:
    def __init__(self, mode, data):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CHUNK_SIZE = 10
        self.imp_type = mode
        try:
            if mode == "client":
                self.socket.connect((data['host'], data['port']))
            elif mode == "server":
                self.socket.bind((data['host'], data['port']))
                self.socket.listen()
                self.client_socket, self.client_addr = None, None
            else:
                raise ConnectionError()
        except OSError:
            print("Address is in use, please wait a moment and try running it again.")
            exit()

    @dispatch(dict, socket.socket)
    def send(self, message: dict, c_client: socket.socket):
        json_str = json.dumps(message)
        message_bytes = json_str.encode('utf-8')
        message_size = len(json_str).to_bytes(4, byteorder='big')
        c_client.send(message_size)
        c_client.send(message_bytes)

    @dispatch(dict)
    def send(self, message: dict) -> None:
        json_str = json.dumps(message)
        message_bytes = json_str.encode('utf-8')
        message_size = len(json_str).to_bytes(4, byteorder='big')
        self.socket.send(message_size)
        self.socket.send(message_bytes)

    def recv(self, c_socket) -> dict:
        message_size_bytes = c_socket.recv(4)
        message_size = int.from_bytes(message_size_bytes, byteorder='big')
        chunks = []
        while message_size > 0:
            chunk = c_socket.recv(min(self.CHUNK_SIZE, message_size))
            if not chunk:
                break
            chunks.append(chunk)
            message_size -= len(chunk)
        message = b''.join(chunks)
        print(message)
        return json.loads(message.decode('utf-8'))

    def close(self):
        self.socket.close()

    def accept(self):
        if self.imp_type != "server":
            raise ImplementationError("wrong implementation")
        self.client_socket, self.client_addr = self.socket.accept()
        return {self.client_socket: self.client_addr}

