# Custom Exception Classes

This package includes the following exception handlers for this
project.

## PortRangeException

Custom exception handler for a port out of range exception

    try:
        raise PortRangeException("Out of Range")
    exception PortRangeException as e:
        print(e)

## HostNotFoundException

Custom exception handler for Host not found exception

    try:
        raise HostNotFoundException("Host is lost")
    exception HostNotFoundException as e:
        print(e)

## MessageException

Custom exception handler for a message error we can't recover from

    try:
        raise MessageException("Message is lost")
    exception MessageException as e:
        print(e)

## ImplementationError

Custom exception handler for the wrong Implementation of a socket connection

    try:
        raise ImplementationError("Wrong Implementation")
    exception ImplementationError as e:
        print(e)