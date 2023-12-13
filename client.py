#!/usr/bin/env python3
import json
import threading
from chat.connection.SocketConnection import Connection
import sys
import signal
import curses


class ChatClient(Connection):
    """
    Provides the methods to run a client application using sockets
    """

    def __init__(self, shost, sport):
        """
        Initializes the components needed for our client to function
        :param shost: str host name
        :param sport: int host port number
        """
        super().__init__(shost, sport)
        self.listen_thread = None
        self.username = None
        self.thread_lock = threading.Lock()
        signal.signal(signal.SIGINT, self.close_client)
        self.message_window = None
        # Flag needs to be set because threads hate me and won't propery close on ctrl + C otherwise.
        self.exit_flag = False

    def connect(self):
        """
        Connects to server and runs client application
        """
        self.start_client()
        self.register_user()
        self.listen_thread = threading.Thread(target=self.get_message)
        self.listen_thread.start()

        try:
            curses.wrapper(self.curses_main)
        except KeyboardInterrupt:
            self.close_client()
            print("\nUser closed client")
            exit()

    def curses_main(self, screen):
        """
        Handles separating the terminal screen for input and chat output
        :param screen: initscr from curses library. Assumes wrapper() function will be used.
        """
        screen.clear()
        curses.echo()
        self.message_window = curses.newwin(curses.LINES - 2, curses.COLS, 0, 0)
        input_window = curses.newwin(2, curses.COLS, curses.LINES - 2, 0)
        self.message_window.scrollok(True)
        input_window.addstr(0, 0, "Enter message or type 'exit' to close chat: ")
        input_window.refresh()

        # Input things to the chat at any time, no need to wait turns
        while True:
            message = input_window.getstr(1, 0).decode('utf-8')
            if message.lower() == "exit":
                self.send_message(json.dumps({"type": "exit"}))
                break
            self.send_message(json.dumps({"type": "message", "message": f"{message}"}))
            message = "You: " + message + "\n"
            self.display_message(message)
            input_window.clear()
            input_window.addstr(0, 0, "Enter message or type 'exit' to close chat: ")
            input_window.refresh()
        self.close()

    def display_message(self, message):
        """
        Displays messages to the output part of the split screen terminal
        :param message: str message to output
        """
        self.message_window.addstr(message)
        self.message_window.refresh()

    def register_user(self):
        """
        Asks for username repeatedly until server sends "good" message
        """
        data = json.loads(self.receive_message())
        if data.get("message"):
            print(data.get("message"))
        while True:
            userinput = input("Enter a username: ")
            user = json.dumps({"type": "username", "username": f"{userinput}"})
            self.send_message(user)
            data = json.loads(self.receive_message())
            if data.get("type"):
                if data["username"] == "good":
                    self.username = userinput
                    break
                else:
                    print("Username is not unique")

    def get_message(self):
        """
        Gets messages sent from the server.
        """
        try:
            while not self.exit_flag:
                data = json.loads(self.receive_message())
                if data.get("type") == "message":
                    message = f"{data.get('timestamp')}: {data.get('username')}: {data.get('message')} \n"
                    self.display_message(message)
                elif data.get("type") == "exit":
                    message = f"{data.get('message')}"
                    self.display_message(message)
        except KeyboardInterrupt:
            self.close_client()
        except OSError:
            # Threads do not want to close, this is supposed to catch that
            return
        except TypeError:
            return
        except AttributeError:
            return

    def close_client(self):
        """
        Closes the client and exits the program
        """
        self.exit_flag = True
        curses.endwin()
        self.close()
        exit()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("Invalid number of arguments. Format should be: \n./client <host> <port>")

    try:
        chat = ChatClient(sys.argv[1], int(sys.argv[2]))
        chat.connect()
    except KeyboardInterrupt:
        print("\nUser closed client")
        chat.close_client()
    except Exception as e:
        print("Error: ", e)
    finally:
        exit()
