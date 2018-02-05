# Homework 2 - Distributed File System

The goal of this project was to create a distributed file system in python.
It will be started up by a manager file with a given host list and port number.
The computer for the file to be saved/retrieved from is chosen from the hash of the filename.

## On Startup

In order for the hosts to start up, the HwkII.py files will need to be in the home directory of whatever computer you are trying to SSH into.

The manager starts the nodes by using the sysStart function with the hostList and port number.
## Manager

Using a list of strings in the form
```python
hostList = [host1, host2, etc]
```
The manager sends an SSH command to each host to start server code on the remote machines.
The manager uses 'nohup' in order to allow the python script to keep executing, even after the SSH connection closes.

STDOUT for the program is redirrected to STDERR with the >&- command.

Finally, the python script is told to execute in the background with the & command.

#### Alternative To This

We could have also caused the program to fork and create an SSH connection with each host
that is maintained while the host is online, but we chose to go with the nohup background method because we wanted
the server to be as independant from the manager's operation as possible


## The Packet

All of the communication between the client and the hosts happens over a TCP socket.
To make this communication easier and simpler, we send a 'packet' object back and forth.
To send it over the TCP socket, we pickle the object and put the output into a makefile of the connection.

The class is below:
```python
class packet:
    def __init__(self, name, command, data):
        self.filename = name
        self.cmd = command
        self.data = data
```
The 'cmd' field is for whatever operation is being used. 'data' can be used for either
parameters for the file function, or for data/errors being returned from the function.

Additionally, to make it easier to code the manager for closing down the hosts, 
it also just opens a connection to the hosts and sends a special 'kill' command.

## The Server

The server has a dictionary for the files that it has open. The key of the dictionary is the filename
and the value is the file object.

The server's primary operation happens within an infinite loop. When the file is run as __main__
with a port number as an argument, it begins listening to the specified port.

First, it opens the connection, creates a makefile for that, and waits for the client to
finish transmitting on the makefile. It loads the object from the makefile, and performs
whatever specified operations.

Then, it sends a packet object back. If the operation required information to be returned,
that info will be in the data portion of the packet object.

## The Client

The client mostly relies on the dFile class. The dFile class makes it seem as though there
are no network operations happening. Whenever one of the 'd' operations are performed, it
sends a packet to the relevant host.
