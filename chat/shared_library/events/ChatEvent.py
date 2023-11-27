#
# Craig R Harrell
# CSC328 - Final Project
# File: ChatEvent.py
# This class is used as a generic event class to trigger events across
# classes.
#

from typing import Callable


class ChatEvent:
    """
    Custom Event class that is used within the chat to handle events such as
    closing, new message, etc.
    """

    def __init__(self, name: str) -> None:
        """
        Initializes the custom event class

        :param name: the name you are giving the event
        """
        self.name = name
        self.handlers = []

    def add_handler(self, handler: Callable) -> None:
        """
        Add a handler function to the list of handlers.

        :param handler: name of handler function
        """
        self.handlers.append(handler)

    def remove_handler(self, handler: Callable) -> None:
        """
        Remove a handler function from the list of handlers.

        :param handler: name of handler to be removed
        """
        if handler in self.handlers:
            self.handlers.remove(handler)

    def trigger(self, *args, **kwargs) -> None:
        """
        Trigger the event and call all registered handlers.

        :param args: any number of arguments
        :param kwargs: any number of keyword arguments
        """
        for handler in self.handlers:
            handler(*args, **kwargs)
