import socket
from threading import Thread
from time import sleep

class Fullnode :
    listBlock = []
    listUser = []
    listNode = []
    listSoc = []
    originNode = socket.socket()
    originNode.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mySocket = socket.socket()
    
    def __init__(self, config) :
        if not config.first :
            self.connectionOrigin(config)
        self.openConnection(config)
        self.config = config

    def connectionOrigin(self, config) :
        # Create the connection to the host
        try :
            print("Connection Host ", config.host, ":", config.port)
            self.originNode.connect((config.host, config.port))
            print("Connection success")
        except Exception as ex :
            print(ex)

    def openConnection(self, config) :
        try :
            print("Open connection", "localhost", config.client)
            self.mySocket.bind(("localhost", config.client))
            self.mySocket.listen(5)
        except Exception as ex :
            print(ex)

    def threadAcceptNode(self) :
        while True:
            co, addr = self.mySocket.accept()
            print("New client joined the socket : ", addr)
            print("\n\n", co.getsockname(), "\n\n")
            newSoc = socket.socket()
            newSoc.connect(co.getsockname())
            self.listSoc.append(newSoc)
            self.listNode.append({"c":co, "addr":addr})
            if not self.config.first :
                msg = str(listSoc)
                self.listNode[-1].send(msg.encode())

    def threadReaderNode(self) :
        while True:
            for node in self.listNode :
                newmsg = node.get("c").recv(1024).decode()
                if len(newmsg) != 0 :
                    print("New data : ", newmsg)
            sleep(0.5)
        

    def run(self) :
        # Create Thread listen()
        threadAcptNode = Thread(target = self.threadAcceptNode, args = ())
        threadAcptNode.start()
        threadReadNode = Thread(target = self.threadReaderNode, args = ())
        threadReadNode.start()
