#
# Craig R Harrell
# CSC328 - Final Project
# File: Scrollable.py
# This class handles the creation and appending of a scrollable text area
#

from tkinter import scrolledtext
import tkinter as tk


class Scrollable:
    """
    This is a helper class to minimize code required to create and update a
    scrollable text area.
    """
    def __init__(self):
        self.name = "ScrollableText"

    def scrollable_text(self, parent: tk.Tk, row: int, column: int, width: float, height: float)\
            -> scrolledtext.ScrolledText:
        """
        Creates a scrollable text area

        :param parent: tk.Tk() - the window
        :param row: -int- row you want the text area to appear
        :param column: -int- column you want the text area to appear
        :param width: -float- width of text area
        :param height: -float- height of text area
        :return: tk.scrolledtext.ScrolledText
        """
        frame = tk.Frame(parent)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=width, height=height)
        text_widget.pack(expand=True, fill='both')
        return text_widget

    def update_txt(self, widget: tk.scrolledtext.ScrolledText, new_content: str) -> None:
        """
        Updates a scrolled text area

        :param widget: scrolledtext
        :param new_content: -str- text you want to add
        """
        widget.insert(tk.END, new_content + "\n")
