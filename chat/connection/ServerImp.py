# Craig R Harrell
# CSC 328 Final Project
# 12/10/2023
# Provides the class to implement the socket chat server

import json
import signal
import threading
import os
import time
from datetime import datetime

from chat.connection.SocketConnection import Connection
from chat.dotenv.DotEnvReader import Env


class Server(Connection):
    """
    Provides the methods to run a server implementation using sockets.
    """
    def __init__(self, host_s, port_s):
        """
        Initializes the components we will need for our server to function.

        :param host_s: str Host name
        :param port_s: int host port number
        """
        super().__init__(host=host_s, port=port_s)
        self.server_log = None
        self.clients = {}
        self.reserved_usernames = ['admin', 'mod', 'super', 'owner']
        self.env = Env()
        self.thread_lock = threading.Lock()
        self.is_running = False
        self.user_thread = None
        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)
        signal.signal(signal.SIGUSR1, self._start)
        self.idle()

    def idle(self):
        """
        Performs setup actions and puts the app in idle mode. It is here so
        we can get the PID and start the monitor which will have a button to actually
        start the server.
        """
        self.write_file_with_current_day()
        self.write_to_log({'message': 'Idle'})
        while not self.is_running:
            continue

    def _start(self, signum, frame):
        """
        Starts the server and accepts clients and puts them in their own thread

        """
        self.write_to_log({"message": f"{self.env.read('MSG_STARTING')}"})
        self.is_running = True

        super().start_server()
        self.write_to_log({"message": f"Listening on {self.host}:{self.port}"})
        try:
            while self.is_running:
                client_socket, address = self.socket.accept()
                self.user_thread = threading.Thread(target=self._handle_client, args=(client_socket,))
                self.user_thread.start()
        except ConnectionAbortedError:
            # close gracefully if possible Shouldn't get this error at all with current setup.
            self.close()

    def write_file_with_current_day(self):
        """
        Creates a log file with today's date as part of the file name
        """
        current_day = datetime.now().strftime('%Y-%m-%d')
        self.server_log = f'logs/{current_day}_server.log'

        if os.path.isfile(self.server_log):
            return

        with open(self.server_log, 'w') as file:
            file.write("")
        file.close()

    def _stop(self, signum, frame):
        """
        Signals the server to shut down

        :param signum: not used but required
        :param frame: not used but required
        """
        self.close()

    def _handle_client(self, c_socket):
        """
        Handles client interactions

        :param c_socket: socket of client
        """
        try:
            # get username before accepting messages
            self.request_username(c_socket)
            self.broadcast_message({"type": "message", "message": f"{self.clients[c_socket]} has joined the chat!",
                                    "username": "server", "timestamp": f"{self.get_time()}"}, c_socket)

            while self.is_running:
                # listen for messages from client and act accordingly
                message = self.receive_message(c_socket)

                if not message:
                    continue

                message = json.loads(message)

                if message["type"] == "message":
                    self.log_and_broadcast(message, c_socket)
                if message["type"] == "exit":
                    self.exit_user(c_socket)
                    break
        except OSError:
            # this is here cause closing threads in python sucks, and it will throw this error no
            # matter what you do, so we force the thread to return.
            return
        except TypeError:
            # this is here cause users could close out their client incorrectly
            return
        finally:
            # we are done so remove the user accordingly
            self.remove_user(c_socket)

    def log_and_broadcast(self, message, c_socket):
        """
        Logs the user's message and broadcasts it

        :param message: dict of message
        :param c_socket: client socket
        """
        message['timestamp'] = f"{self.get_time()}"
        message['username'] = f"{self.clients[c_socket]}"
        self.write_to_log(message)
        self.broadcast_message(message, c_socket)

    def exit_user(self, c_socket):
        """
        Removes user from the server once they decide to leave

        :param c_socket: socket of client
        """
        msg = {"type": "message", "username": "server",
               "message": f"{self.clients[c_socket]} has left the chat.",
               "timestamp": f"{self.get_time()}"}
        # exiting message in logs
        self.store_username(c_socket, self.clients[c_socket], 'X')
        self.write_to_log(msg)
        self.broadcast_message(msg, c_socket)

    def broadcast_message(self, message, originator=None):
        """
        Broadcasts messages to all clients except the originating client if one is provided. If
        an originator is not provided, the message will be sent to all connected clients

        :param message: dict of message to send
        :param originator: socket client socket if provided (optional)
        """
        with self.thread_lock:
            for client_socket, _ in self.clients.items():
                if client_socket != originator:
                    try:
                        message_json = json.dumps(message)
                        self.send_message(message_json, client_socket)
                    except Exception as e:
                        print(f"Error broadcasting message: {e}")

    def store_username(self, c_socket, username, action):
        """
        Stores the user's information in a log file

        :param c_socket: socket client's socket info
        :param username: str client's username
        :param action: char what action is being performed 'E' for entering 'X' for exit
        """
        address = c_socket.getpeername()
        msg = {"action": f"{action}", "address/port": f"{address[0]}:{address[1]}",
               "username": f"{username}", "timestamp": f"{self.get_time()}"}
        self.write_to_log(msg)
        with self.thread_lock:
            self.clients[c_socket] = username

    def request_username(self, c_socket):
        """
        Requires clients to provide a username. Username is checked for uniqueness and for banned
        usernames. Username is then store in a dict with socket as key

        :param c_socket: socket client socket
        """
        msg = json.dumps({"type": "message", "message": f"{self.env.read('MSG_WELCOME')}", "username": "server",
                          "timestamp": f"{self.get_time()}"})
        self.send_message(msg, c_socket)
        self.write_to_log(msg)
        while True:
            try:
                user_response = json.loads(self.receive_message(c_socket))
            except TypeError:
                continue
            if user_response.get("username"):
                if not self.is_unique(user_response['username']):
                    taken_msg = json.dumps({"type": "username", "username": "taken",
                                            "timestamp": f"{self.get_time()}"})
                    self.send_message(taken_msg, c_socket)
                    self.write_to_log(taken_msg)
                    continue
                else:
                    self.store_username(c_socket, user_response['username'], "E")
                    self.send_message(json.dumps({"type": "username", "username": "good",
                                                  "timestamp": f"{self.get_time()}"}), c_socket)
                    self.write_to_log({"type": "username", "username": "good",
                                       "timestamp": f"{self.get_time()}"})
                    break

    def is_unique(self, username):
        """
        Checks for uniqueness of a username and if it is not of a variation of a banned username

        :param username: str clients suggested username
        :return: bool True for unique and not a banned name
        """
        with self.thread_lock:
            # check if it contains a reserved username
            if any(reserved in username.lower() for reserved in self.reserved_usernames):
                return False
            # now check if it is unique
            return all(user[1] != username for user in self.clients.items())

    def close(self):
        """
        Performs the closing actions necessary for the server to shut down gracefully.

        """
        count = 5
        while count > 0:
            msg = {"type": "exit", "message": f"Server shutting down in...{count} seconds.",
                   "timestamp": f"{self.get_time()}"}
            self.broadcast_message(msg)
            self.write_to_log(msg)
            time.sleep(1)
            count -= 1
        self.is_running = False
        # Close all client connections
        with self.thread_lock:
            for client_socket, _ in self.clients.items():
                client_socket.close()
        # Close the server socket
        self.socket.close()
        exit()

    def remove_user(self, c_socket):
        """
        Removes the user from our client list and closes their connection to the server

        :param c_socket: socket client socket
        """
        with self.thread_lock:
            for client_socket, _ in self.clients.items():
                if client_socket == c_socket:
                    client_socket.close()
                    del self.clients[c_socket]
                    break

    @staticmethod
    def get_time():
        """
        Returns the current time of the server

        :return: str formatted datetime (mm-dd-yyyy hh:mm:ss) in 24-hour format
        """
        current_time = datetime.now()
        return current_time.strftime("%m-%d-%Y %H:%M:%S")

    def log_message(self, message, c_socket):
        """
        Logs the messages sent by a client into a message log file

        :param message: dict message sent by client in json format
        :param c_socket: socket client socket
        """
        addr = c_socket.getpeername()
        msg = f"{addr[0]}:{addr[1]}, {message['username']}," \
              f"{message['timestamp']}, {message['message']}\n"
        self.write_to_log(msg)

    def write_to_log(self, param):
        """
        Write the action to the log file

        :param param: json str Log message in json format
        """
        with open(self.server_log, 'a') as file:
            file.write(f"{json.dumps(param)}\n")
        file.close()
