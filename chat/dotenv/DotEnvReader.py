#
#
#
#
#
import os
import dotenv


class Env:
    """
    Really quick and dirty class to grab .env variables
    """
    def __init__(self, env_file=None):
        """
        Initializes the class with the env file

        :param env_file str Nullable name of .env file you wish to read
        """
        if env_file is None:
            self.env_path = os.path.abspath("environment/.env.server")
        elif os.path.isfile(os.path.abspath(f'environment/{env_file}')):
            self.env_path = os.path.abspath(f'environment/{env_file}')
        else:
            raise FileNotFoundError(f"{env_file} could not be found. In the environment folder")

    def read(self, key):
        """
        Reads the value of the key in the env

        :param key: str KEY for env variable
        :return: string|None
        """
        return dotenv.get_key(self.env_path, key)



