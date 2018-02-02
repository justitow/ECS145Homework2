# Client.py
# Creates a socket for communicating witht the server
# Sends Commands for opening, reading, writing files

import pickle, os, sys, socket

class packet:
  filename = ''
  cmd = ''
  data = ''

p = packet()

p.filename = 'test.txt'
p.cmd = 'read'


# Create a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'pc10.cs.ucdavis.edu'
port = 1337

s.connect((host, port))
mf = s.makefile()
pickle.dump(p, mf)
s.close()
