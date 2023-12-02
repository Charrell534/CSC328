import tkinter as tk
from chat.dotenv.DotEnvReader import DotEnvReader
from chat.validation.Validation import ValidateUserInput


class PortWindow:
    """

    """
    def __init__(self) -> None:
        """
        Initializes the variables needed to open and use the window
        """
        self.error_label = None
        self.host_entry = None
        self.port_entry = None
        self.window = tk.Tk()
        self.data = {}
        self.env = DotEnvReader('.env.port')

    def create_window(self) -> None:
        """
        Creates the components for our window
        """
        self.window.title(self.env.read("WINDOW_TITLE"))
        self.window.resizable(True, True)
        self.window.geometry(self.env.read("WINDOW_SIZE"))

        # build the components of the window
        host_label = tk.Label(text=self.env.read("HOST_PROMPT"))
        host_label.pack(pady=5, padx=5)

        self.host_entry = tk.Entry(self.window)
        self.host_entry.pack(padx=5, pady=5)

        label = tk.Label(text=self.env.read("PORT_PROMPT"))
        label.pack(padx=5, pady=5)

        self.port_entry = tk.Entry()
        self.port_entry.pack(padx=5, pady=5)

        self.error_label = tk.Label(fg="red")
        self.error_label.pack(padx=5, pady=5)

        button = tk.Button(text=self.env.read("SUBMIT_BTN"), command=self._data_entered)
        button.pack(padx=5, pady=5)

    def _data_entered(self) -> None:
        """
        Event handler for start button to check user input and close window on good input
        """
        valid = ValidateUserInput()
        if self.host_entry.get() != "":
            if valid.validate_host(self.host_entry.get()):
                self.data['host'] = self.host_entry.get()
            else:
                self.error_label.config(text=self.env.read("HOST_ERROR"))
        else:
            self.data['host'] = "0.0.0.0"

        if self.port_entry.get() != "":
            if valid.validate_port(self.port_entry.get()):
                self.data['port'] = int(self.port_entry.get())
            else:
                self.error_label.config(text=self.env.read("PORT_ERROR"))
        else:
            self.data['port'] = 10000
        if self.data.get('host') is not None:
            self.close()

    def close(self) -> None:
        """
        Closes our window
        """
        self.env.clear()
        self.env = None
        try:
            if self.window.winfo_exists():
                self.window.destroy()
        except tk.TclError as e:
            # widget has been destroyed ignore and go on
            pass

    def run(self) -> None:
        """
        Opens our window
        """
        # Start the Tkinter event loop after creating the window
        self.window.mainloop()
