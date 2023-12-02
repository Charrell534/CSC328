#!/usr/bin/env python3
import tkinter as tk

from chat.gui.PortWindow import PortWindow
from chat.gui.ServerWindow import ServerWindow

if __name__ == "__main__":
    server = None
    try:

        window = PortWindow()
        window.create_window()
        window.run()
        data = window.data
        root = tk.Tk()
        server = ServerWindow(root, data)
        server.run()

    except KeyboardInterrupt:
        if server:
            server.shutdown()
