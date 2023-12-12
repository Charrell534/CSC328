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

# check if host is valid
# regex for IPv4
ipv4_regex="^([0-9]{1,3}\.){3}[0-9]{1,3}$"

# regex for IPv6
# source https://stackoverflow.com/questions/53497/regular-expression-that-matches-valid-ipv6-addresses
ipv6_regex="^([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}$|^([0-9a-fA-F]{1,4}:){1,7}:|^([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}$|^([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}$|^([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}$|^([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}$|^([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}$|^[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})?$"

# regex for "localhost"
localhost_regex="^localhost$"

# check if the host input matches any of the regex patterns
if [[ $host =~ $ipv4_regex || $host =~ $ipv6_regex || $host =~ $localhost_regex ]]; then
    :  # Do nothing
else
    echo "Invalid host name given. Host name needs to be a valid IPv4 or IPv6 address or 'localhost'."
    exit 1
fi


# check the port number for correct range
# set to this because most system use ports in range of 0-1024 for their own use.
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