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

def main():

    dInit(['pc8.cs.ucdavis.edu','pc10.cs.ucdavis.edu'], 1337)
    f = dopen('./test.txt', 'w')
    print f.dwrite('This is a text File')
    print f.dread()
    f.dclose()


    f = dopen('./test.txt', 'a')
    f.dwrite('\nappended sentence\n')
    f.dclose()


    f = dopen('./test.txt', 'r+')
    print f.dread()
    f.dclose()


if __name__ == '__main__': main()
