class packet:
  filename = ''
  cmd = ''
  data = ''



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
port = 1337
s.bind((host, port))

# accept "call" from client
s.listen(1)

conn, addr = s.accept()
print 'Client is at', addr

mf = conn.makefile()
x = pickle.load(mf)

print x.filename, x.cmd

conn.close()
