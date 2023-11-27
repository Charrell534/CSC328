import time

from chat import PortRangeException, PortWindow
from server_script import ServerMonitor


def do_shutdown():
    count = 3
    while count > 0:
        print(f"shutting down in...{count}")
        time.sleep(1)
        count -= 1


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