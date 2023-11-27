#
# Craig R Harrell
# CSC328 - Final Project
# File: ValidateInput.py
# This class validates and sanitizes user input
#

import re
import tkinter as tk

from multipledispatch import dispatch

from chat import DotEnvReader
from chat import HostNotFoundException
from chat import PortRangeException


class ValidateInput:
    """
    This class handles user input validation. Currently, handles port number, host name, message.
    """
    def __init__(self, env: str) -> None:
        """
        Initializes the components to run validation within the class

        :param env: -str- name of .env file to grab error messages from
        """
        self.env = DotEnvReader(env)

        self.ipv4 = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        self.pattern_ip4 = re.compile(self.ipv4)

        self.ipv6 = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
        self.pattern_ip6 = re.compile(self.ipv6)

        self.pattern_local = "localhost"

        self.data = {}

    @dispatch(str)
    def validate_port(self, port_num: str) -> bool:
        """
        Validates a port number

        :param port_num: -str- port number
        :return: -bool- true if port is in range
        """
        try:
            temp = int(port_num)
            if temp < 10000 or temp > 65535:
                return False
            else:
                self.data['port'] = temp
                return True
        except ValueError:
            raise PortRangeException(self.env.read_env("PORT_ERROR"))

    @dispatch(tk.Entry, tk.Label)
    def validate_port(self, port_entry: tk.Entry, error_label: tk.Label) -> bool:
        """
        Validates a port entered in a tk window

        :param port_entry: -tk.Entry- the Entry widget for port info
        :param error_label: -tk.Label- the label for error messages
        :return: -bool- true if port is in range
        """
        try:
            temp = int(port_entry.get())
            if temp < 10000 or temp > 65535:
                error_label.config(text=self.env.read_env("PORT_ERROR"))
                return False
            else:
                self.data['port'] = temp
                return True
        except ValueError:
            error_label.config(text=self.env.read_env("PORT_ERROR"))
            return False

    @dispatch(str)
    def validate_host(self, host: str) -> bool:
        """
        Validates a host name to either IPv4, IPv6 or "localhost"

        :param host: -str- name of host
        :return: -bool- true if it matches any of the criteria
        """
        try:
            if self.pattern_ip4.match(host) or self.pattern_ip6.match(host) or self.pattern_local == host:
                self.data['host'] = host
                return True
            else:
                raise HostNotFoundException(self.env.read_env("HOST_ERROR"))
        except HostNotFoundException:
            return False

    @dispatch(str, tk.Label)
    def validate_host(self, host: str, error_label: tk.Label) -> bool:
        """
        Validates the host using regex for tkinter window

        :param error_label: tkinter Label
        :param host: string- Required. name of host
        :raises HostNotFoundException
        :return: boolean - True if matches expectations
        """
        try:
            if self.pattern_ip4.match(host) or self.pattern_ip6.match(host) or self.pattern_local == host:
                self.data['host'] = host
                return True
            else:
                raise HostNotFoundException(self.env.read_env("HOST_ERROR"))
        except HostNotFoundException:
            error_label.config(text=self.env.read_env("HOST_ERROR"))
            return False

    @dispatch(str)
    def clean_message(self, msg: str) -> str:
        """
        Cleans a message of anything that isn't in our regex.

        :param msg: -str- client message
        :return: -str- clean string
        """
        return re.sub(r'[^a-zA-Z0-9\s]', '', msg)
