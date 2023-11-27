class PortRangeException(Exception):
    """
    PortRangeException is raised when a user entered port number
    is out of the specified range
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)