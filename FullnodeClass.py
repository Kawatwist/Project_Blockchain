from socket import socket
from threading import Thread
from time import sleep

class Fullnode :
    listBlock = []
    listUser = []
    listNode = []
    listSoc = []
    
    def __init__(self, config) :
        self.clientHost = True
        listenSoc = socket()
        listenSoc.bind((config.host, 4246))
        listenSoc.listen(5)
        self.listSoc.append(listenSoc)
        firstSoc = socket()
        firstSoc.connect((config.host, config.port))
        self.listSoc.append(firstSoc)

        # try :
            # self.nodeSoc.bind((config.host, config.port + 2))
            # self.nodeSoc.listen(5)
        # except Exception as ex :
        #     print(ex)
        #     print("a Node port already exist")
        #     self.nodeSoc.connect((config.host, config.port))

        # Open connection client
        self.clientSoc = socket()
        try :
            self.clientSoc.bind((config.host, config.client))
            self.clientSoc.listen(5)
        except Exception as ex :
            print(ex)
            print("a Client port already exist")
            self.clientHost = False
            self.clientSoc.connect((config.host, config.client))

    def threadNodeConnection(self, arg) :
        while True :
            connect, addr = arg.accept()
            self.listNode.append({"c":connect, "addr":addr})
            print("New client joinned : ", addr)
            print("Actual client : ", self.listNode)
            sleep(0.1)

    def threadNode(self, arg) :
        # if self.nodeHost :
        #     NodeConnection = Thread(target = self.threadNodeConnection, args = (self.nodeSoc,))
        #     NodeConnection.start()
        while True :
            print("Waiting node data ", self.listNode)
            for node in self.listNode :
                newmsg = node.get("c").recv(1024).decode()
                if len(newmsg) != 0 :
                    print("New data : ", newmsg)
            sleep(0.5)

    def threadClientConnection(self, arg) :
        while True :
            sleep(0.1)

    def threadClient(self, arg) :
        if self.clientHost :
            ClientConnection = Thread(target = self.threadClientConnection, args = (self.clientSoc,))
            ClientConnection.start()
        while True :
            sleep(0.1)

    def run(self) :
        # Start thread node & thread client
        node = Thread(target = self.threadNode, args = (self.listSoc,))
        node.start()
        client = Thread(target = self.threadClient, args = (self.clientSoc,))
        client.start()
