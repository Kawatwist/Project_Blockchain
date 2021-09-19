from socket import socket
from threading import Thread
from time import sleep

class Genesisnode :
    listBlock = []
    listUser = []
    listNode = []
    listSoc = []
    
    def __init__(self, config) :
        self.clientHost = True
        self.nodeSoc = socket()
        try :
            self.nodeSoc.bind((config.host, config.port))
            self.nodeSoc.listen(5)
        except :
            print("Connection already used")
            exit

        # Open connection client

    def threadNodeConnection(self, arg) :
        while True :
            connect, addr = arg.accept()
            newsoc = socket()
            print(connect)
            newsoc.connect(addr)
            self.listSoc.append(newsoc)
            msg = str(self.listNode)
            self.listNode.append({"c":connect, "addr":addr})
            self.listSoc[-1].send(msg.encode())
            # New node added send him connection
            sleep(0.1)

    def threadNode(self, arg) :
        NodeConnection = Thread(target = self.threadNodeConnection, args = (self.nodeSoc,))
        NodeConnection.start()
        while True :
            # print("Waiting node data")
            for node in self.listNode :
                newmsg = node.get("c").recv(1024).decode()
                if len(newmsg) != 0 :
                    print("New data : ", newmsg)
            sleep(0.5)

    def run(self) :
        # Start thread node
        node = Thread(target = self.threadNode, args = (self.nodeSoc,))
        node.start()
