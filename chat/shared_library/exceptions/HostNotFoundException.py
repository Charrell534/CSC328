class HostNotFoundException(Exception):
    """
    Exception class to handle host errors such as not correct formatting,
    host unreachable, etc.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)