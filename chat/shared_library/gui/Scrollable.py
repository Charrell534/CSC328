from tkinter import scrolledtext
import tkinter as tk


class Scrollable:
    def __init__(self):
        self.name = "ScrollableText"

    def scrollable_text(self, parent, row, column, width, height) -> scrolledtext.ScrolledText:
        frame = tk.Frame(parent)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=width, height=height)
        text_widget.pack(expand=True, fill='both')
        return text_widget

    def update_txt(self, widget, new_content):
        widget.insert(tk.END, new_content + "\n")
