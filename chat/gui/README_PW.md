# PortWindow

Provides a gui interface for the user to input their desired host and port numbers.

## To initialize

To initialize this window use the following:

    port_win = PortWindow()
    port_win.create_window()
    port_win.run()

## To get the data 

To get the data the user inputted use the following:

    port_win  = PortWindow()
    port_win.create_window()
    port_win.run()
    data = port_win.data

Be sure to write it in that order otherwise your data object will be empty.

It creates an object with the following format:

    {"host": "<host>", "port": <int> }

That is it, the class handles everything else and its private methods 
should not be accessed. 