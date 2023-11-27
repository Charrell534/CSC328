# README.md

## Description:
This is a team project for CSC328 that creates a chat system with a server and client written in python.

## How to run the server:

To run the server, download the code and place it on your drive.
Open a terminal at the directory and run the following command:

    $>make server

Then enter the following command:
    
    $>./server

The script will run and you will enter a virtual environment, a 
window will then open prompting you for host and port information.
Enter the information and submit. The server is now running and a 
second window will open.

## How to run the client

Start the server first (see above). Enter the following into a new 
terminal window open to the program's directory:

    $>make client

Then enter:

    $>./client

The script will run creating a virtual environment and 
open a window prompt for port and host. Once the connection is 
made with the information provided a chat window will open. 

## Alternative to run both

The Makefile contains a command to run both server and client scripts. This will 
ask for the number of clients you would like to start at once. Realize each one 
will open a window and ask for the server information.

To run this alternative enter the following into the command line

    $>make run
    $>Enter the number of clients: <n>

