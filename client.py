"""
This is a really basic example with no gui, it has errors and is missing key functionality. Just
wanted to show you the idea.
"""

import threading
from chat.connection.Conn import Conn


def receive_messages(client_socket):
    while True:
        # Receive and print messages from the server
        data = conn.recv(client_socket)
        print(f"{data['timestamp']} {data['username']}: {data['message']}\n")


def get_username(client_socket):
    while True:
        user_input = input("Enter a username: ")
        conn.send({"type": "username", "username": f"{user_input}"})
        data = conn.recv(client_socket)
        print(data)
        if data['type'] == "username":
            if data["username"] == "good":
                break
            else:
                print("Username is taken, please try again: ")


conn = Conn('client', {'host': '127.0.0.1', 'port': 10000})


# get username
get_username(conn.socket)
# Create a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(conn.socket,))
receive_thread.start()

while True:
    message = input("Enter your message: ")
    print("\n")
    # Send the message to the server
    conn.send({'type': 'message', 'message': f"{message}"})
