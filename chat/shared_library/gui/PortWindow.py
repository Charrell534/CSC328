#
# Craig R Harrell
# CSC328 - Final Project
# File: PortWindow.py
# This class is used to display a prompt window for port and host
# variables from the user in a gui
#
import tkinter as tk
from typing import Callable

from chat import ChatEvent, DotEnvReader, ValidateInput


class PortWindow:
    """
    This class is used to display a prompt window for port and host
    variables from the user in a gui
    """
    def __init__(self, handler: Callable) -> None:
        """
        Initializes the port window

        :param handler: Handler for any events that might be triggered
        """
        self.error_label = None
        self.port_entry = None
        self.host_entry = None
        self._port_window = None
        self.dot_env = DotEnvReader(".env.port")

        self.data = {}
        self._closing_event = ChatEvent("Closing")
        self.handler = handler
        self._closing_event.add_handler(handler)

    def create_port_window(self) -> None:
        """
        Creates the port window and displays it. Window will have
        a port number entry, host name entry and a start button with
        labels and error messaging
        """
        self._port_window = tk.Tk()
        self._port_window.title(self.dot_env.read_env("WINDOW_TITLE"))
        self._port_window.geometry("300x300")

        host_label = tk.Label(text=self.dot_env.read_env("HOST_PROMPT"))
        host_label.pack(pady=5, padx=5)

        self.host_entry = tk.Entry(self._port_window)
        self.host_entry.pack(padx=5, pady=5)
        self.host_entry.insert(0, self.dot_env.read_env("HOST_DEFAULT"))

        label = tk.Label(text=self.dot_env.read_env("PORT_PROMPT"))
        label.pack(padx=5, pady=5)

        self.port_entry = tk.Entry()
        self.port_entry.pack(padx=5, pady=5)

        self.port_entry.bind('<Return>', self.test_enter)

        self.error_label = tk.Label(fg="red")
        self.error_label.pack(padx=5, pady=5)

        button = tk.Button(text=self.dot_env.read_env("WINDOW_SUBMIT"),
                           command=self._data_entered)
        button.pack(padx=5, pady=5)

        # listen for window close from window close button
        self._port_window.bind("<Button-3>", self.on_right_click)
        self._port_window.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._port_window.mainloop()

    def test_enter(self, *args):
        print("enter pressed")

    def _data_entered(self) -> None:
        """
        Captures the data that was entered on submit, validates it using the
        ValidInput class and places that data into our data object
        """
        validate = ValidateInput(".env.port")
        if validate.validate_port(self.port_entry, self.error_label)\
                and validate.validate_host(self.host_entry.get(), self.error_label):
            self.data = validate.data
            self.close()

    def _on_closing(self) -> None:
        """
        Captures a close event within the window, broadcasts that event to our
        program and closes the window.
        """
        self._closing_event.trigger()
        self._port_window.destroy()

    def is_open(self) -> bool:
        """
        Checks if our port window is open

        :return: bool true if window is open
        """
        if self._port_window.winfo_exists():
            return True
        else:
            return False

    def close(self) -> None:
        """
        Performs the necessary clean-up of our class
        """
        self.dot_env.clear_env()
        self.dot_env = None
        self._closing_event.remove_handler(self.handler)
        self._closing_event = None
        self._port_window.destroy()

    def on_right_click(self, event) -> None:
        """
        Captures if the user does a right click to exit the window

        :param event: right click event
        """
        self._on_closing()
