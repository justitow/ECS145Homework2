class packet:
    def __init__(self, name, command, data):
        self.filename = name
        self.cmd = command
        self.data = data



# Server Code:
# Opens a socket and gets connection
# Recieves a string and echoes back to client in multiple copies

import pickle
import socket
import sys

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associate socket with a port
host = ''
port = 1338
s.bind((host, port))

# accept "call" from client
s.listen(1)

conn, addr = s.accept()
print 'Client is at', addr

mf = conn.makefile()
x = pickle.load(mf)
mf.close()

# Send Back Packet
mf = conn.makefile()
f = open(x.filename)
x.data = f.read()

pickle.dump(x, mf)

conn.close()
