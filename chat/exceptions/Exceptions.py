
class PortRangeException(Exception):
    """
    Custom exception handler for a port out of range exception
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class HostNotFoundException(Exception):
    """
    Custom exception handler for Host not found exception
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MessageException(Exception):
    """
    Custom exception handler for a message error we can't recover from
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ImplementationError(Exception):
    """
    Custom exception handler for the wrong Implementation of a socket connection
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
