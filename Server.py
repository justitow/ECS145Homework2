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
        return file_read(x)
    elif (x.cmd == 'w'):
        return file_write(x)
    elif (x.cmd == 'o'):
        return file_open(x)
    elif (x.cmd == 'c'):
        return file_close(x)
    else:
        return x

def file_open(x):
    try:
        open_files[x.filename] = open(x.filename, x.data)
    except IOError:
        x.data = 'File ' + x.filename + ' does not exist'
        x.cmd = 'f'
    print "file ", x.filename, " opened"
    return x

def file_write(x):
    try:
        open_files[x.filename].write(x.data)
    except IOError:
        x.data = "Not able to write to" + x.filename
        x.cmd = 'f'
    return x

def file_read(x):
    try:
        if x.data == -1:
            x.data = open_files[x.filename].read()
        else:
            x.data = open_files[x.filename].read(int(x.data))
    except IOError:
        x.data = 'Unable to Read File' +  x.filename
        x.cmd = 'f'

    return x

def file_close(x):

    try:
        open_files[x.filename].close()
        del open_files[x.filename]
    except IOError:
        x.data = 'Unable to Close File'
        x.cmd = 'f'
    return x

def close_all(conn):
    for file in open_files:
        file.close()


def main():
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Associate socket with a port
    host = ''
    port = int(sys.argv[1])
    s.bind((host, port))




    while(1):
        # accept "call" from client
        s.listen(1) ## pretty sure don't need to

        conn, addr = s.accept()
        print 'Client is at', addr

        mf = conn.makefile()
        x = pickle.load(mf)
        mf.close()



        # Parse Command
        x = parse_command(x)


        # Send Back Packet
        mf = conn.makefile()
        pickle.dump(x, mf)
        mf.close()
        print "packet sent back"
        conn.close()

        if x.cmd == 'k':
            s.listen(0)
            s.shutdown(socket.SHUT_RDWR)
            s.close() # may not need this here?
            close_all(conn)
            return 0


if __name__ == '__main__': main()
