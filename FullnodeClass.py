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
    mySocketNode = socket.socket()
    mySocketClient = socket.socket()
    join = 0
    
    def __init__(self, config) :
        self.openConnection("localhost", config.node)
        if not config.first :
            try :
                self.connectionOrigin(config)
            except Exception as ex :
                print(ex)
                return
        # try :
        #     self.mySocketClient = self.openConnection(config, self.mySocketClient, "localhost", config.client)
        # except Exception as ex :
        #     print(ex)
        #     return
        self.config = config

    def connectionOrigin(self, config) :
        # Create the connection to the host
        try :
            print("Connection Host ", config.host, ":", config.port)
            self.originNode.connect((config.host, config.port))
            msg = str({config.host, config.node})
            self.originNode.send(msg.encode())
            print("Connection success")
        except Exception as ex :
            raise Exception(ex)

    def openConnection(self, host, port) :
        try :
            print("Open connection", host, port)
            self.mySocketNode.bind((host, port))
            self.mySocketNode.listen(5)
            print("Open connection", host, port, " Done\n")
        except Exception as ex :
            raise Exception(ex)

    def threadAcceptNode(self) :
        while True:
            co, addr = self.mySocketNode.accept()
            print("New client joined the socket : ", co, " | ", addr)
            self.join = 1;
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
            if self.join :
                newmsgenc = self.mySocketNode.recv(1024)
                if newmsgenc :
                    newmsg = newmsgenc.decode()
                    if len(newmsg) != 0 :
                        if not newmsg.find(str("connection : ")) == -1 :
                            print("New connection get : ", newmsg[newmsg.find(str("connection : "))])
                        print("New data : ", newmsg)
            sleep(0.5)
        

    def run(self) :
        # Create Thread listen()
        threadAcptNode = Thread(target = self.threadAcceptNode, args = ())
        threadAcptNode.start()
        threadReadNode = Thread(target = self.threadReaderNode, args = ())
        threadReadNode.start()
