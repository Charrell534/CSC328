# Craig R Harrell
# CSC 328 Final Project
# 12/10/2023
# Provides a GUI for user interaction with the chat server
import sys
from chat.gui.LogViewer import Monitor

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Incorrect number of arguments. "
              "Something is wrong in the bash script, check the sleep function may need to be increased.")
        exit()
    log_viewer = Monitor(sys.argv[1])
    log_viewer.run()
