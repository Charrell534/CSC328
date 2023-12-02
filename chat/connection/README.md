# Conn documentation

This class contains the necessary methods for a socket program to run and communicate.

The following are the methods and how to use them.

## To Initialize
    connection = Conn(str, dict)

The string variable takes only two options, "server" or "client". 

The dictionary is the values for the host and port and should be set up as 
follows.

    my_dict = {"host": "<host_value_as_string>", "port": <port_val_as_int>}

Putting this all together to initialize you would:

    my_dict = {"host": "localhost", "port": 10000}
    connection = Conn("client", my_dict)

## send(str) or send(str, socket)

The send method is overloaded and depends on which implementation of 
the Conn object you have created. This method handles conversion to json object 
and to bytes for you. 


#### Client

The client is able to send messages via a json object as follows:

    my_dict = {"host": "localhost", "port": 10000}
    connection = Conn("client", my_dict)
    connection.send({"type": "message", "message": "<message>"})

#### Server

The server can also use the same method to send with an additional argument

    my_dict = {"host": "localhost", "port": 10000}
    connection = Conn("server", my_dict)
    connection.send({"type": "message", "message": "<message>"}, <client_socket>)

## recv()

RETURNS: dictionary object

To receive a message you would use the following in you code:

    conn.recv()

Conversion and byte chunking is handled in this method for you. 
It returns a dictionary object. It is implementation independent.

## close()

To close the connection use the following:

    conn.close()

This will close your socket. It is implementation independent.

## accept()

RETURNS: dict obj of {client_socket, client_addr} 
THROWS: ImplementationError

Server implementation dependent. Accepts clients sockets:

    client_socket, client_addr = conn.accept()

This will throw an ImplementationError in a client environment. 


