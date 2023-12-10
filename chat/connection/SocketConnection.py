# Craig R Harrell
# CSC 328 Final Project
# 12/10/2023
# Shared socket implementation for chat server and client
import socket


class Connection:
    """
    Provides the methods needed for socket communication
    """
    def __init__(self, host, port):
        """
        Initializes the socket

        :param host:
        :param port:
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        """
        Starts the server socket
        """
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def start_client(self):
        """
        Starts the client socket
        """
        self.socket.connect((self.host, self.port))

    def send_message(self, message, c_client=None):
        """
        Sends a message from the socket if one is passed otherwise sends a message
        from the predefined socket of the class

        :param message: json str
        :param c_client: socket passed in socket to send from
        """
        message = message.encode('utf-8')
        if c_client is None:
            self.socket.sendall(len(message).to_bytes(4, byteorder='big') + message)
        else:
            c_client.sendall(len(message).to_bytes(4, byteorder='big') + message)

    def receive_message(self, c_socket=None):
        """
        Receives messages from the socket if one is passed otherwise receives on the
        predefined socket of the class

        :param c_socket: socket passed in socket to receive from
        """
        if c_socket is None:
            length_bytes = self.socket.recv(4)
        else:
            length_bytes = c_socket.recv(4)
        if not length_bytes:
            return None
        length = int.from_bytes(length_bytes, byteorder='big')
        if c_socket is None:
            data = self.socket.recv(length).decode('utf-8')
        else:
            data = c_socket.recv(length).decode('utf-8')
        return data

    def close(self):
        """
        Properly closes the socket connection
        """
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
