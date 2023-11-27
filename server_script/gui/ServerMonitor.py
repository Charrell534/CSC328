import tkinter as tk
from typing import Callable

from chat import ChatEvent
from chat import DotEnvReader
from chat import Scrollable


class ServerMonitor:
    def __init__(self, handler: Callable, env: str, data: dict):
        """
        Initializes a tk window for server monitoring

        :param handler: -Callable- main handler for closing
        :param env: -str- .env file name
        :param data: -dict- data being passed to run the server
        """
        self.name = "name"
        self.window = tk.Tk()
        self.event = ChatEvent("Closing")
        self.event.add_handler(handler)

        self.data = data
        self.env = DotEnvReader(env)

        self.users = {}

        self.messages_txt = tk.StringVar()
        self.users_txt = tk.StringVar()
        self.num_users = tk.StringVar()

        self.error_label = None
        self.message_scrollable = None
        self.users_scrollable = None

        print(self.data)

    def start_server_monitor(self):
        self.window.title(self.env.read_env("WINDOW_TITLE"))
        self.window.geometry("500x500")

        self.window.resizable(True, True)

        label = tk.Label(self.window, text=self.env.read_env("USERS"))
        label.grid(column=0, row=0, pady=5, padx=5)
        self.users_scrollable = Scrollable().scrollable_text(self.window, 1, 0, 65, 10)

        label_msg = tk.Label(self.window, text=self.env.read_env("MESSAGES"))
        label_msg.grid(column=0, pady=5, row=2, padx=5)
        self.users_scrollable = Scrollable().scrollable_text(self.window, 3, 0, 65, 10)

        log_user_btn = tk.Button(self.window, text=self.env.read_env("LOG_USERS"))
        log_user_btn.grid(column=0, pady=5, padx=5, row=4)

        log_msg_btn = tk.Button(self.window, text=self.env.read_env("LOG_MESSAGES"))
        log_msg_btn.grid(column=0, pady=5, padx=5, row=5)

        shutdown_btn = tk.Button(self.window, text=self.env.read_env("SHUTDOWN"),
                                 command=self.do_pre_shutdown)
        shutdown_btn.configure(fg="#FF0000")
        shutdown_btn.grid(column=0, padx=5, pady=5, row=7)

        self.window.bind("<Button-3>", self.on_right_click)
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.window.mainloop()

    def on_right_click(self):
        # eventually send to do pre_shutdown
        self.event.trigger()
        self.window.destroy()

    def _on_closing(self):
        # eventually send to pre_shutdown
        self.event.trigger()
        self.window.destroy()

    def do_pre_shutdown(self):
        # TODO actually do pre-shutdown stuff before we trigger the event
        self.event.trigger()
        self.window.destroy()
