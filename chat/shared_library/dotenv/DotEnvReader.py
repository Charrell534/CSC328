import os

from dotenv import load_dotenv, dotenv_values


class DotEnvReader:
    def __init__(self, env: str):
        self.env = "chat/environment/" + env
        self.dotenv_path = os.path.abspath(self.env)
        load_dotenv(self.dotenv_path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clear_env()

    def read_env(self, key: str) -> str:
        if key in os.environ:
            return os.getenv(key)
        else:
            return "Key Not Found"

    def clear_env(self):
        temp = dotenv_values(self.dotenv_path)
        for key in temp:
            if key in os.environ:
                os.environ.pop(key)




