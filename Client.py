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
def dopen(filename):
    return dFile(filename)

class dFile:
    def __init__(self, fname):
        'Constructor'
        self.name = fname
        # Create a Socket
        self.socket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def sendPacket(self, command, data):
        'Sends Packets to Server'
        'Create a Packet'
        p = packet(self.name,command,data)
        
        # Hash the Index
        serverindex = hash(self.name) % len(G.hostList)
        
        # Connect to Server and Send Packet
        self.socket.connect((G.hostList[serverindex], G.port))

        # Sends Packet with mf.close()
        mf = s.makefile()
        pickle.dump(p, mf)
        mf.close()

        # Recieve the response packet
        mf = s.makefile()
        x = pickle.load(mf)
        
        #Close Connection
        self.socket.close()
        return x

    def dread(self):
        recieved_packet = self.sendPacket('r',-1)
        
    def dread(self, parameter):
        recieved_packet = self.sendPacket('r', int(parameter))
        
    def dwrite(self):
        'Write'
        x = 0
    def dclose(self):
        'Close'
        x = 0

def main():

    dInit(['pc10.cs.ucdavis.edu'], 1338)
    f = dopen('./test.txt')
    f.dread()

if __name__ == '__main__': main()
