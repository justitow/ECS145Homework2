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

open_files = {}

def parse_command(x):
    if (x.cmd == 'r'):
    elif (x.cmd == 'w'):
    elif (x.cmd == 'o'):
        return file_open(x)
    elif ()
    
def file_open(x):
    open_files[x.filename] = open(x.filename)
    return x
    
def file_write(x):
    return x

def file_read(x):
    if x.data == -1:
        x.data = open_files[x.file_name].read()
    else:
        x.data = open_file[x.file_name].read(x.data)
    return x
    
def file_close(x):
    open_files[x.filename].close()
    del open_files[x.filename]
    return x
    
def close_all(conn):
    conn.close()
    for file in open_files:
        file.close()
    

def main():
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Associate socket with a port
    host = ''
    port = 1338
    s.bind((host, port))
    
    
    
    
    while(1):
        # accept "call" from client
        s.listen(1)
        
        conn, addr = s.accept()
        print 'Client is at', addr
        
        mf = conn.makefile()
        x = pickle.load(mf)
        mf.close()
        
        if x.cmd == 'k':
            close_all(conn)
            break
        
        # Parse Command
        x = parse_command(x)
            
        
        # Send Back Packet
        mf = conn.makefile()
        pickle.dump(x, mf)
        
        conn.close()


if __name__ == '__main__': main()
