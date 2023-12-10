#!/bin/bash

# Craig R Harrell
# CSC 328 Final Project
# 12/3/2023
# Performs the necessary commands to run the server and monitor


# check if two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Invalid number of arguments: "
    echo "Usage: $0 <host> <port>"
    exit 1
fi

# set variables from arguments
host=$1
port=$2

# check the port number for correct range
if [ "$port" -lt 1025 ]; then
  echo "Invalid port number port numbers need to be 1025-65536"
  exit 1
fi

# start the server in the background
python3 server.py $host $port &

# wait for the server to finish initializing
sleep 2

# get the PID of the last background process (should be the server)
server_pid=$!

# run the monitor passing in the PID of the server for signaling
python3 monitor.py $server_pid

# close the bash program
exit 0