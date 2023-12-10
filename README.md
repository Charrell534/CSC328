ID block

## How to build and run the client and server

### Run make
To build the client and server use the following:
    
    make

This will make the appropriate scripts executable.

To clean up after use, use the following:

    make clean


### Run Server

Assuming you have ran make, enter the following into the terminal. 
Please allow a moment or two for the GUI to initialize.

    ./start.sh <host_name> <port_number>

Port numbers must be between 1025-65536 on a personal computer. You 
can enter either "localhost" or any IPv4 or IPv6 host address. 





## File/folder manifest 

### Root Folder contents:

    monitor.py - Provides a GUI for server
    server.py  - Provides the methods to run a chat server
    start.sh   - Main entry point for running both the server and GUI monitor

### Root > chat > connections 

    SocketConnection.py - Provides the shared library object for both the 
                            server and client chat apps. 

## Responsibility matrix 

| Aspect | Contribution | 
|:-------|:------------:|
| server | Craig        |       
| client | Emily    |   
 | Documentation| Both |
| Library| Craig | 

