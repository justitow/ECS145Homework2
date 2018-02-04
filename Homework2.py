# Client.py
# Creates a socket for communicating witht the server
# Sends Commands for opening, reading, writing files

import pickle, os, sys, socket

class packet:
    def __init__(self, name, command, data):
        self.filename = name
        self.cmd = command
        self.data = data


class G:
    hostList = ''
    port = 0


# dInit()
# Initialized the Client Code
def dInit(hostList, portnum):
    G.hostList = hostList
    G.port = portnum


# Returns FilePointer Object
# Use:
#   file_ptr = dopen(filename)
#   file_ptr.read(), file_ptr.write(), etc
def dopen(filename, mode='r'):
    remote_file = dFile(filename)
    remote_file.dopen(filename, mode)
    return remote_file

class dFile:
    def __init__(self, fname):
        'Constructor'
        self.name = fname

    def sendPacket(self, command, data):
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        'Sends Packets to Server'
        'Create a Packet'
        p = packet(self.name,command,data)

        # Hash the Index
        serverindex = hash(self.name) % len(G.hostList)

        # Connect to Server and Send Packet
        remote_socket.connect((G.hostList[serverindex], G.port))

        # Sends Packet with mf.close()
        mf = remote_socket.makefile()
        pickle.dump(p, mf)
        mf.close()
        print "packet sent"

        # Recieve the response packet
        mf = remote_socket.makefile()
        x = pickle.load(mf)
        mf.close()
        print "packet recieved"
        if (x.cmd == 'f'):
            print x.data
        # Close Connection
        remote_socket.shutdown(socket.SHUT_WR)
        remote_socket.close()
        return x

    def dread(self, parameter = -1):
        recieved_packet = self.sendPacket('r', parameter)
        return recieved_packet.data


    def dwrite(self, data):
        x = self.sendPacket('w', data)
        return x

    def dclose(self):
        x = self.sendPacket('c', '')
        return x

    def dopen(self, filename, mode='r'):
        x = self.sendPacket('o', mode)
        return x


 # This is how to server tells what operation will be done on the open files.
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


# Any of the file_*** functions will be how to server operates on the files
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
    try:
        for file in open_files:
            file.close()
    except:
        return "Unable to close all files"


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