import time

from chat import PortRangeException, PortWindow
from server_script import ServerMonitor


def do_shutdown():
    exit()  # this should be final however may need to adjust for PortWindow


if __name__ == '__main__':
    try:
        port_window = PortWindow(do_shutdown)
        port_window.create_port_window()
        data = port_window.data
        server_monitor = ServerMonitor(do_shutdown, ".env.server", data)
        server_monitor.start_server_monitor()

    except KeyboardInterrupt:
        do_shutdown()
    except PortRangeException as e:
        print(e.message)
        do_shutdown()



# TODO revise word doc to include turn taking
# TODO add gnome-terminal to make doc for auto loading clients