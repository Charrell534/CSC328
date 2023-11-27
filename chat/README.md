# Chat Library

The following folders and files contained within this 
directory are shared Libraries for both the client chat app and server
that handles the chat. The libraries include the following:

## chat.shared_library.dotenv.DotEnvReader
Contains the class DotEnvReader which is responsible for reading .env files and 
getting their contents. 

#### Usage:
##### Import 

    from chat import DotEnvReader

##### To read from .env
    
    env=DotEnvReader("<env_file>")
    data = env.read_env("<KEY>") 

##### To remove env data from os.env
    env=DotEnvReader("<env_file>")
    env.clear_env()

This is important especially if you have multiple variables with the same name
(i.e. WINDOW_TITLE='Setup', WINDOW_TITLE='Chat')

## chat.shared_library.events.ChatEvent
Custom Event class that is used within the chat to handle events such as
    closing, new message, etc.

#### Usage:
##### Import
    from chat import ChatEvent

##### Adding a new event
    self._closing_event = ChatEvent("Closing")
    self._closing_event.add_handler(handler)

Where 'handler' is a Callable to handle the event.
##### Removing a handler
    self._closing_event.remove_handler(handler)
##### Triggering an event
    self._closing_event.trigger(*argv, **kwargs)

## chat.shared_library.exceptions.HostNotFoundException
Exception class to handle host errors such as not correct formatting,
    host unreachable, etc.

#### Usage:
##### Import
    from chat import HostNotFoundException

##### Raising the exception
    raise HostNotFoundException("<message>")

## chat.shared_library.exceptions.PortRangeException

PortRangeException is raised when a user entered port number
    is out of the specified range

#### Usage:
##### Import
    from chat import PortRangeException

##### Raise the exception
    raise PortRangeException("<message>")

## chat.shared_library.gui.PortWindow
This class is used to display a prompt window for port and host
    variables from the user in a GUI.

#### Usage
##### Import 
    from chat import PortWindow

##### Initialize
    window = PortWindow(<event_handling_function_for_close>)
    window.create_port_window()

##### To get port and host info (after close)
    window.create_port_window()
    data = window.data
    print(data['port'])
    print(data['host'])

## chat.shared_library.validate.ValidateInput
This class handles user input validation. Currently, handles port number, host name, message.

#### Usage
##### Import
    from chat import ValidateInput
##### Validate Port number
    validate = ValidateInput("<port_env>")
    if validate.validate_port(<user_input>):
        port = validate.data['port']

##### Validate Host input
    validate = ValidateInput("<port_env>")
    if validate.validate_host(<user_input>):
        host = validate.data['host']

##### Clean Message input
    validate = ValidateInput("<message_env>")
    clean_input = validate.clean_message(<user_input>)


