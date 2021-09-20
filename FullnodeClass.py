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
            print("New client joined the socket : ", co, " | ", addr)
            # newSoc = socket.socket()
            # if not co.getsockname in self.listNode :
            #     newSoc.connect(co.getsockname())
            #     self.listSoc.append(newSoc)
            #     self.listNode.append(co.getsockname)
            #     if not self.config.first :
            #         msg = str(self.listSoc)
            #         self.listSoc[-1].send(msg.encode())
            sleep(0.5)

    def threadReaderNode(self) :
        while True:
            for soc in self.listSoc :
                print("Node send msg\n")
                newmsg = soc.recv(1024).decode()
                if len(newmsg) != 0 :
                    print("New data : ", newmsg)
            sleep(0.5)
        

    def run(self) :
        # Create Thread listen()
        threadAcptNode = Thread(target = self.threadAcceptNode, args = ())
        threadAcptNode.start()
        threadReadNode = Thread(target = self.threadReaderNode, args = ())
        threadReadNode.start()
