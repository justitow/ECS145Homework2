import os, socket, sys

class packet:
    def __init__(self, name, command, data):
        self.filename = name
        self.cmd = command
        self.data = data


path = './ECS145/HW2/'

class Manager:

    def __init__(self):
        'Default Constructor \
        Creates a listening Socket'
        self.port = 0

    def sysStart(self, hostList, portNum):
        self.port = portNum

        for host in hostList:
            os.system("ssh " + host + " 'nohup python " + path + ' server.py ' + str(portNum) + "  >&- &'")

    def sysStop(self, hostList):
        # Create a Socket to Kill server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for host in hostList:
            s.connect((host, self.port))
            
            
            mf = s.makefile()
            pickle.dump(packet('', 'k', ''), mf)
            mf.close()
            s.close()


def main():
    m = Manager()
    hostList = ['pc8.cs.ucdavis.edu','pc10.cs.ucdavis.edu']
    m.sysStart(hostList, 1337)


if __name__ == "__main__":
    main()
