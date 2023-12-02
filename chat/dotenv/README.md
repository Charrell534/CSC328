# DotEnvReader 

Provides an easy-to-use interface for reading and accessing 
environmental variables from an env file. 

## To initialize

To initialize this class use the following:

    env = DotEnvReader(<env_file_name>)

This class is already set up to look in the correct location for 
the named file. The location to store your .env files is:

chat/environment/

## read(str)

To read from the loaded env file use the following

    my_var = env.read("<key>")


## clear()

In order to use the same keys again in cases such as WINDOW_TITLE within 
your .env file you will need to clear the environment of any previously
loaded .env files. To do this use the following:

    env.clear()

This will remove any key value pairs that were loaded and gives you a 
fresh environment to load new key value pairs into. 



