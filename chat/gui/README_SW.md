# ServerWindow

Provides a gui interface to view activity on a server implementation of
this project. 

You need only to initialize this window once, and it will run 
till the server is terminated. It does not return any data.

## To initialize

To initialize this window use the following:

    root = tk.Tk()
    window = ServerWindow(root, data)
    window.run()

The data in this instance is the data gained from the port window object. 

    window = PortWindow()
    window.create_window()
    window.run()
    data = window.data
    root = tk.Tk()
    window = ServerWindow(root, data)
    window.run()