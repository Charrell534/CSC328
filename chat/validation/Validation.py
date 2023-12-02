import re

from multipledispatch import dispatch
from chat.exceptions.Exceptions import PortRangeException, HostNotFoundException


class ValidateUserInput:
    """
       This class handles user input validation. Currently, handles port number, host name, message.
       """

    def __init__(self) -> None:
        """
        Initializes the components to run validation within the class
        """
        self.ipv4 = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        self.pattern_ip4 = re.compile(self.ipv4)
        self.ipv6 = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
        self.pattern_ip6 = re.compile(self.ipv6)
        self.pattern_local = "localhost"

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
                return True
        except ValueError:
            raise PortRangeException("Error")

    def validate_host(self, host: str) -> bool:
        """
        Validates a host name to either IPv4, IPv6 or "localhost"

        :param host: -str- name of host
        :return: -bool- true if it matches any of the criteria
        """
        try:
            if self.pattern_ip4.match(host) or self.pattern_ip6.match(host) or self.pattern_local == host:
                return True
            else:
                raise HostNotFoundException("Error")
        except HostNotFoundException:
            return False
