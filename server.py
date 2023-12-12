
# Craig R Harrell
# CSC 328 Final Project
# 12/10/2023
# Provides the class to implement the socket chat server


import sys

from chat.dotenv.DotEnvReader import Env
from chat.connection.ServerImp import Server


if __name__ == '__main__':
    try:
        # check for correct params passed
        if len(sys.argv) < 3:
            print(Env().read("ERROR_MSG_ARGS"))
            print(f"Usage: {sys.argv[0]} <host_name> <host_port>")
            exit()
        else:
            server = Server(sys.argv[1], int(sys.argv[2]))
    # shouldn't hit any of these, but users ARE stupid
    except ValueError as e:
        print(f"Value err: {e}")
        print(Env().read("ERROR_MSG_ARGS"))
        print(f"Usage: {sys.argv[0]} <host_name> <host_port>")
    except OSError as e:
        print(f"OS error {e}")
        print(Env().read("ERROR_MSG_ARGS"))
        print(f"Usage: {sys.argv[0]} <host_name> <host_port>")
