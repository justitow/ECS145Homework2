import os, socket, sys

hostList = []

def sysStart(hostList, portNum):
    for host in hostList:
        os.system("ssh " + host + " 'nohup python pythontest.py " + str(portNum) + "  >&- &'")

#def sysStop(hostList):
#    for host in hostList:

def sendHostList(hostList , portNum):
    global ls
    for host in hostList:
        ls.connect((host, portNum))





def getHostList():
    global ls, hostList
    ls.listen(1)
    (clientsocket, address) = ls.accept()
    flo = clientsocket.makefile('r', 0)
    for i in flo:
        hostList.append(i)
    flo.close()
    clientsocket.close()


def initSocket(port):
    global ls
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.bind(('', port))


def main():
    initSocket(int(argv[1]))


if __name__ == "__main__":
    main()
