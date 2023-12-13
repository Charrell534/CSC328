# CSC 328 Final Network Program Implementation
## Authors
Emily Deneen, Craig R Harrell

December 12, 2023

## Class
CSC 328

## About
This project implements a chat server and client using sockets, allowing multiple users to be clients and communicate
with each other. 


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

### Run Client

After running make, you can use the following command:
./client <host_name> <port_number>



## File/folder manifest 

### Root Folder contents:

    monitor.py - Provides a GUI for server
    server.py  - Provides the methods to run a chat server
    start.sh   - Main entry point for running both the server and GUI monitor
    Makefile   - Provides the necessary functions to run the applications.
    README.md  - Provides descriptions and information needed to successfully run the programs contained 
                 within this package.
    client.py - provides the methons needed to run client application. Runs client in terminal.

    chat       - [Directory] Python package library- see below for details.


### chat.connections 

    SocketConnection.py - Provides the shared library object for both the 
                            server and client chat apps.
    ServerImp.py        - Provides the implementation of the server.
    
### chat.dotenv

    DotaEnvReader.py - Provides an quick and dirty .env reader.


### chat.gui
    LogViewer.py - Provides a GUI for user interaction with the chat server

## Responsibility matrix 

| Aspect | Contribution | 
|:-------|:------------:|
| server | Craig        |       
| client | Emily    |   
 | Documentation| Both |
| Library| Craig | 

## Tasks

Major tasks are shown below with time to complete and
contributor. 

| Task          | Time    | Contribution |
|:--------------|---------|:------------:|
| Server alone  | 8 hrs   |    Craig     |
| Server GUI    | 6 days  |    Craig     |
| Documentation | 1 month |    Craig     |
| Client        | 2.5 hrs |    Emily     |
| Client GUI    | 4.5 hrs |    Emily     |
| Documentation | 1 hr    |    Emily     |

## Protocol

Please see [ClientServer-NetworkProgramDesign](CleintServer-NetworkProgramDisign.docx)

## Assumptions

### Server
It is assumed that the user will use the bash file (start.sh) to enter into the server program on a local machine with 
all required dependencies. (json, dotenv, tkinter)
The user should enter a host name and port number they wish the server to work on as arguments for the bash file. 
The bash runs and checks the arguments and then the server is started and enters idle mode. 
After which the bash grabs the PID of the server app and starts the server monitor app passing it the PID. 
The server monitor app then is able to communicate with the server app using signals to start and close the server.
The server monitor app also reads the server logs displaying the last action that was performed on the server.

Once the server monitor is closed, the server should close as well if it was not closed prior to now, the bash script
finishes. 

### Client
The user will not be sending very long messages (see Discussions)


## Discussions

Python's threading library is terrible about closing. This issued arose when trying to close the tkinter window, the 
script would hang. This was solved by separating the logic of the tkinter window and threading, adding additional exception 
handling, and lots and lots of head scratching, tears, yelling(cursing), and finally just giving up for a simpler setup.

Because of how the curses library works, the user can only send a message as long as their terminal window. While this is not ideal, this would prevent users from trolling by flooding the entire screen with a very large message, so it has its upsides. There is no reasonable way to fix this, and I am not going through the curses library's code.

## Status

The server has been completed to the specifications given, and works as required. There are no known bugs, however,
I was not able to test it for every scenario and condition it may encounter in the wild.







