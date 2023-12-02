import os

from dotenv import load_dotenv, dotenv_values


class DotEnvReader:
    """
        This class reads in a .env file and adds it to the os environment
        """

    def __init__(self, env: str):
        """
        Reads in the .env file

        :param env: -str- name of .env file
        """
        self.env = "chat/environment/" + env
        self.dotenv_path = os.path.abspath(self.env)
        load_dotenv(self.dotenv_path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Built-in function to capture destruction of the class

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.clear()

    def read(self, key: str) -> str:
        """
        Finds the key in the environment and reads the value

        :param key: -str- key pair of value
        :return: -str- value found or "Key not Found" message
        """
        if key in os.environ:
            return os.getenv(key)
        else:
            return "Key Not Found"

    def clear(self) -> None:
        """
        Clears the environment of the variables passed to it from the
        .env file
        """
        temp = dotenv_values(self.dotenv_path)
        for key in temp:
            if key in os.environ:
                os.environ.pop(key)


