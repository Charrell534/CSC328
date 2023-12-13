# Craig R Harrell
# CSC 328 Final Project
# 12/10/2023
# Provides a GUI for user interaction with the chat server
import json
import os
import signal
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext
import time


class Monitor:
    """
    Provides a GUI for user interaction with the chat server
    """
    def __init__(self, s_pid):
        """
        Initializes the GUI

        :param s_pid: str PID of the server.py script
        """
        self.pid = int(s_pid)
        current_day = datetime.now().strftime('%Y-%m-%d')
        self.server_file = f'logs/{current_day}_server.log'
        self.log_messages = None

        self.root = tk.Tk()
        self.root.title("Log Viewer")

        # String var for general message label
        self.str = tk.StringVar()

        # Label prompt
        self.label = tk.Label(self.root, text="Closing the monitor will close the server.")
        self.label.pack(pady=5, padx=5)

        # Message Log Area
        self.message_log_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.message_log_text.pack(fill=tk.BOTH, expand=True)

        # General Messages for GUI user
        self.msg_lbl = tk.Label(self.root, textvariable=self.str)
        self.msg_lbl.pack(padx=5, pady=5)

        # Start server button
        self.start_btn = tk.Button(self.root, text="Open", command=self._start)
        self.start_btn.pack(pady=5, padx=5)

        # Close server Button
        self.close_button = tk.Button(self.root, text="Close", command=self._close_window)
        self.close_button.pack(pady=5, padx=5)

        # Event handlers
        self.root.protocol("WM_DELETE_WINDOW", self._close_window)
        signal.signal(signal.SIGINT, self._close_window)

        # Schedule log update every 2 seconds
        self.root.after(1000, self._update_logs)

    def _update_logs(self):
        """
        This method is the handler for updating the log message area
        """
        self._populate_message_log()
        # Reschedule the update after 2 seconds
        self.root.after(1000, self._update_logs)

    def _populate_message_log(self):
        """
        Reads the server log file and displays the last line of the log in the
        GUI.
        """
        with open(self.server_file, 'r') as file:
            message_log = ""
            for line in file:
                message_log += f"{json.loads(line.strip())}\n"

        self.message_log_text.delete(1.0, tk.END)
        self.message_log_text.insert(tk.END, message_log)
        self.message_log_text.see(tk.END)

    def _close_window(self, signum=None, frame=None):
        """
        General purpose event handler for closing the window and server

        :param signum: signal or None Handle signal if passed if not handle the event
        :param frame: frame or None
        """
        os.kill(self.pid, signal.SIGINT)
        count = 4
        while count > 0:
            self.str.set(f"Shutting down in {count}")  # Use set to update the StringVar
            self.root.update_idletasks()
            time.sleep(1)
            count -= 1
        self.root.destroy()

    def _start(self):
        """
        Sends a signal to the server.py script to start the server
        """
        os.kill(self.pid, signal.SIGUSR1)
        self.str.set("Server starting")

    def run(self):
        """
        Handles the tk root loop
        """
        self.root.mainloop()
