import time
from datetime import datetime
import threading
import tkinter as tk
from tkinter import scrolledtext

from chat.connection.Conn import Conn
from chat.dotenv.DotEnvReader import DotEnvReader




class ServerWindow:
    def __init__(self, root, data):
        """
        Sets up our environment for a gui window
        :param root: tk.Tk
        :param data: dict must contain the keys host and port
        """
        self.close_btn = None
        self.message_label = None
        self.message_list = None
        self.window = root
        self.env = DotEnvReader(".env.server")
        self.user_list = None

        # create a dict to hold our users
        self.clients = {}

        # Create a lock for the clients dictionary
        self.clients_lock = threading.Lock()

        # create our window, so we can start sending data to it
        self.create_window()
        # get our socket connection for a server
        self.conn = Conn("server", data)

        # update the user on our connection
        msg = f"Server listening on {data['host']}:{data['port']}"
        self._update_message_label(msg)

        self.handle_thread = None

        self.stop_thread = threading.Event()
        # Start a thread to accept incoming connections
        self.accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
        self.accept_thread.start()

    def create_window(self):
        """
        Creates the widgets for the window
        """
        # set window specifics
        self.window.title(self.env.read("WINDOW_TITLE"))
        self.window.resizable(True, True)
        self.window.geometry(self.env.read("WINDOW_SIZE"))

        # Create scrolled text widget for messages
        self.message_list = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=40, height=10)
        self.message_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create scrolled text widget for users
        self.user_list = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=20, height=10)
        self.user_list.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # create a message output for server messages
        self.message_label = tk.Label(self.window)
        self.message_label.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        # create a button to shut down the server
        self.close_btn = tk.Button(self.window, text="Close Server", command=self.shutdown)
        self.close_btn.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Make the columns expandable
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

        # Make the rows expandable
        self.window.rowconfigure(0, weight=1)

    def _accept_connections(self):
        """
        Accepts client connections and puts them into their own threads
        """
        while not self.stop_thread.is_set():
            client_socket, addr = self.conn.socket.accept()
            # Start a thread to handle the client's messages
            with self.clients_lock:
                # Acquire the lock before modifying the clients dictionary
                self.clients[client_socket] = None

            with client_socket:
                self.handle_thread = threading.Thread(target=self._handle_client, args=(client_socket,))
                self.handle_thread.start()

    def _handle_client(self, c_socket):
        """
        Handles the clients within a threaded scope requires user to enter username and it be
        unique before they are able to start messaging.

        :param c_socket: client socket connection
        """
        while not self.stop_thread.is_set():
            try:
                while True:
                    username = self.conn.recv(c_socket)
                    if username['type'] == "username":
                        with self.clients_lock:
                            # Check if the username is unique
                            if username['username'] in self.clients.values():
                                self.conn.send({"type": "username", "username": "taken"}, c_socket)
                            else:
                                self.clients[c_socket] = username['username']
                                self.conn.send({"type": "username", "username": "good"}, c_socket)
                                self._update_message_label(f"User '{username['username']}' connected.")
                                break

                # Broadcast the new connection to all clients
                with self.clients_lock:
                    self._update_user_list()
                    self._broadcast(
                        {"type": "message", "username": "server", "message": f"{username['username']} has joined the "
                                                                             f"chat\n", "timestamp": f"{self._get_time()}"})

                # Start handling messages for the connected client
                self._handle_messages(c_socket, username['username'])

            except ConnectionResetError:
                with self.clients_lock:
                    # Handle client disconnect
                    username = self.clients.get(c_socket, "Unknown User")
                    self._update_message_label(f"User '{username}' disconnected.")
                    del self.clients[c_socket]
                    self._broadcast({"type": "message", "username": "admin",
                                     "message": f"{username} has left the chat", "timestamp": f"{self._get_time()}"})
                    break

    def _handle_messages(self, c_socket, username):
        """
        Handles the clients chat messages

        :param c_socket: client socket connection
        :param username: client username
        :return:
        """
        while True:
            try:
                # Receive messages
                message = self.conn.recv(c_socket)

                if not message:
                    break

                if message['type'] == "message":
                    # update our message list
                    self._update_message_list(
                        {"username": f"{username}", "message": f"{message['message']}",
                         "timestamp": f"{self._get_time()}"})
                    # Broadcast the message to all clients
                    self._broadcast({"type": "message", "username": f"{username}", "message": f"{message['message']}",
                                     "timestamp": f"{self._get_time()}"})

            except ConnectionResetError:
                # Handle client disconnect
                self._update_message_label(f"User '{username}' disconnected.")
                del self.clients[c_socket]
                # TODO update for json
                self._broadcast({"type": "message", "username": "admin",
                                 "message": f"{username} has left the chat", "timestamp": f"{self._get_time()}"})
                break

    def _broadcast(self, message):
        """
        Handles broadcasting message to all connected users

        :param message: string message
        """
        with self.clients_lock:
            for c_socket in self.clients:
                try:
                    self.conn.send(message, c_socket)
                except ConnectionResetError:
                    # Handle disconnected clients
                    username = self.clients.get(c_socket, "Unknown User")
                    self._update_message_label(f"User '{username}' disconnected.")
                    del self.clients[c_socket]
                    self._broadcast({"type": "message", "username": "admin",
                                     "message": f"{username} has left the chat", "timestamp": f"{self._get_time()}"})

    def shutdown(self):
        """
        Handles shutting down the server
        """
        count_down = 5
        while count_down > 0:
            msg = {"type": "exit", "username": "admin",
                   "message": f"Server shutting down in...{count_down} seconds.", "timestamp": f"{self._get_time()}"}
            self._broadcast(msg)
            print(count_down)
            self._update_message_list(msg)
            time.sleep(1)
            count_down -= 1
        self._close()

    @staticmethod
    def _get_time() -> str:
        """
        Returns the current time

        :return: str time in format m-d-Y H:M:S
        """
        current_time = datetime.now()
        return current_time.strftime("%m-%d-%Y %H:%M:%S")

    def run(self):
        """
        Shows the window
        """
        self.window.mainloop()

    def _close(self):
        """
        Destroys the window
        """
        self.stop_thread.set()
        self.accept_thread.join()

        # Close all client sockets
        with self.clients_lock:
            for client_socket in self.clients.keys():
                client_socket.close()

        # Wait for threads to join
        if self.handle_thread:
            self.handle_thread.join()
        self.conn.close()
        self.window.destroy()

    def _update_message_label(self, msg):
        """
        Updates the admin user of server changes by updating a label in the gui

        :param msg: string server change
        """
        self.message_label.config(text=msg)

    def _update_message_list(self, msg):
        """
        Updates teh chat area of the gui

        :param msg: dict message from the user
        """
        format_msg = f"<{msg['timestamp']} {msg['username']}>: {msg['message']} \n"
        # make sure we are at the end and add msg
        self.message_list.insert(tk.END, format_msg)
        # Scroll to the bottom
        self.message_list.see(tk.END)

    def _update_user_list(self):
        """
        Updates the list of users area of the gui
        """
        self.user_list.delete(1.0, tk.END)
        for users in self.clients.values():
            user = f"{users}\n"
            self.user_list.insert(tk.END, user)
            self.user_list.see(tk.END)


"""
Consider Logging:

    Instead of printing messages for debugging purposes, consider using the logging module. It provides a more flexible and configurable way to handle log messages.

Improve Exception Handling:

    Consider catching more specific exceptions where applicable, instead of catching a broad Exception or ConnectionResetError.

Docstrings:

    Add detailed docstrings for methods, describing their purpose, parameters, and return values.

Separation of Concerns:

    Consider breaking down the large methods into smaller, more focused methods. This improves code readability and makes it easier to understand and maintain.

Logging in ServerWindow Initialization:

    Consider adding log statements to indicate when the server window is initialized and when the server starts listening.

Close Connections on Server Shutdown:

    Ensure that all client connections are properly closed during server shutdown.

Error Handling in Socket Operations:

    Add appropriate error handling for socket operations, such as handling socket.error or specific socket-related exceptions.

Configurability:

    Consider making some parameters, such as window title and size, configurable (e.g., by passing them as arguments or reading from a configuration file).
"""