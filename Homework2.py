import os, socket, sys

hostList = []

def sysStart(hostList, portNum):
    for host in hostList:
        os.system("ssh " + host + " 'nohup python pythontest.py " + str(portNum) + "  >&- &'")

#def sysStop(hostList):
#    for host in hostList:


# get and send host list are not needed, host nodes don't need to be aware of eachother
def sendHostList(hostList , portNum):
    global ls

    ls.connect((host, portNum))



def recieveConnection():
    global ls, hostList
    ls.listen(1)
    (clientsocket, address) = ls.accept()

    return (clientsocket, address)


def initSocket(port):
    global ls
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ls.bind(('', port))


def main():
    initSocket(int(argv[1]))
    (clientsocket, address)  = recieveConnection()

if __name__ == "__main__":
    main()
