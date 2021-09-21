import socket
import BlockchainClass as BC
from threading import Thread
from time import sleep

blockSizeLimit = 5

class Fullnode :
    blockchain = BC.Blockchain()
    listUser = [] # User connected to this node
    listNode = [] # Other Node connected at me
    listSoc = []  # Same as list Node but used for display
    listCo = []   # Only used for check already connected
    originNode = socket.socket()
    originNode.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mySocketNode = socket.socket()
    mySocketNode.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mySocketClient = socket.socket()
    mySocketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    join = 0
    
    def __init__(self, config) :
        self.config = config
        self.myHost = "localhost"
        self.myPort = config.node
        self.name = config.name
        self.fd = open(self.name, "wb")
        save = dict({"host":self.myHost, "port":self.myPort, "name":self.name})
        self.listCo.append(save)
        self.mySocketNode.bind(("localhost", config.node))
        self.mySocketNode.listen()
        self.mySocketClient.bind((self.myHost, config.client))
        self.mySocketClient.listen()
        if not config.first :
            try :
                save = dict({"host":"localhost", "port":config.port, "name":"Master"})
                self.listCo.append(save)
                self.connectionOrigin(config)
            except Exception as ex :
                print(ex)
                return
        # try :
        #     self.openConnection("localhost", config.client)
        # except Exception as ex :
        #     print(ex)
        #     return
        # self.config = config

    def connectionOrigin(self, config) :
        try :
            print("Connection Host ", config.host, ":", config.port)
            self.originNode.connect((config.host, config.port))
            msg = "--connection" + str({"host":config.host, "port":self.myPort, "name":self.name})
            self.originNode.send(msg.encode())
            threadReadNode = Thread(target = self.threadReaderNode, args = (self.originNode,))
            threadReadNode.start()
            print("Connection success")
        except Exception as ex :
            raise Exception(ex)

    def checkAlreadyConnected(self, host, port) :
        for elem in self.listCo :
            if elem["host"] == host and elem["port"] == port :
                print("check elem :", elem, "for", host, port, "Find !")
                return True
        print("check elem :", elem, "for", host, port, "Not found")
        return False

    def joinNewNode(self, host, port, name) :
        try :
            if not self.checkAlreadyConnected(host, port) :
                print("Connection newNode (--jo) ", host, ":", port)
                newNode = socket.socket()
                newNode.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                newNode.connect((host, port))
                self.listNode.append(newNode)
                msg = "--connection" + str({"host":self.myHost, "port":self.myPort, "name":self.name})
                newNode.send(msg.encode())
                threadReadNode = Thread(target = self.threadReaderNode, args = (newNode,))
                threadReadNode.start()
                save = dict({"host":host, "port":port,"sock":newNode})
                self.listSoc.append(save)
                save = dict({"host":host, "port":port, "name":name})
                self.listCo.append(save)
                print("Connection success")
            else :
                print("Already connected to ", host, port, " List node connected : ", self.listCo)
        except Exception as ex :
            print("Error for ", host, port)
            raise Exception(ex)

    def threadAcceptNode(self) :
        while True:
            co, addr = self.mySocketNode.accept()
            print("New client joined the socket : ", addr)
            self.listNode.append(co)
            threadReadNode = Thread(target = self.threadReaderNode, args = (co,))
            threadReadNode.start()
            sleep(0.5)

    # def openConnection(self, host, port) :
    #     try :
    #         print("Open connection", host, port)
    #         self.mySocketClient.bind((host, port))
    #         self.mySocketClient.listen()
    #         print("Open connection", host, port, " Done\n")
    #     except Exception as ex :
    #         raise Exception(ex)

    def createNewConnection(self, newmsg:str, newsoc) :
        print("New connection (--co) ", newmsg, "\n")
        write = "New connection ask : " + newmsg + "\n"
        self.fd.write(bytes(write.encode()))
        write = "Actually connected : " + str(self.listCo) + "\n"
        self.fd.write(bytes(write.encode()))
        self.fd.flush()
        addr = eval(newmsg[newmsg.find(str("{")):])
        if not self.checkAlreadyConnected(addr["host"], addr["port"]) :
            write = "~[! Connection accepted !]~ : " + newmsg + "\n"
            self.fd.write(bytes(write.encode()))
            for node in self.listSoc :
                listNodeToSend = "--join" + str(self.listCo)
                print("Send : ListSoc to ", node["host"], ":", node["port"], "SEND ", listNodeToSend)
                node["sock"].send(listNodeToSend.encode())
            save = dict({"host":addr["host"], "port":addr["port"],"sock":newsoc})
            self.listSoc.append(save)
            save = dict({"host":addr["host"], "port":addr["port"], "name":addr["name"]})
            self.listCo.append(save)

    def joinNewConnection(self, newmsg:str) :
        addr = eval(newmsg[newmsg.find("{"):-1])
        for soc in addr :
            if not type(soc) == str:
                data = eval(str(soc))
                if data["host"] and data["port"] :
                    self.joinNewNode(data["host"], data["port"], data["name"])

    def threadReaderNode(self, node) :
        while True:
            newmsgenc = node.recv(1024)
            if newmsgenc :
                newmsg = newmsgenc.decode()
                if len(newmsg) != 0 :
                    if not newmsg.find(str("--connection")) == -1 :
                        print("New connection get : ", newmsg[newmsg.find(str("{")):])
                        self.createNewConnection(newmsg, node)
                    elif not newmsg.find(str("--join")) == -1 :
                        print("Join message get : ", newmsg[newmsg.find(str("[")):])
                        self.joinNewConnection(newmsg)
                    else :
                        print("New data : ", newmsg, " from node ??")
            sleep(0.5)

    def threadClientNode(self) :
        while True:
            co, addr = self.mySocketClient.accept()
            print("New client joined the socket : ", addr)
            self.listUser.append(co)
            sleep(0.5)

    def threadClientReadNode(self) :
        while True:
            for user in self.listUser :
                newmsgenc = user.recv(1024)
                if newmsgenc :
                    newmsg = newmsgenc.decode()
                    self.blockchain.addBuffer(newmsg)

    def threadMinningNode(self) :
        while True :
            txnList = []
            size = self.blockchain.getBufferSize()
            while len(txnList) < blockSizeLimit and size > 0:
                block = self.blockchain.getBufferPop()
                size -= 1
                currState = self.blockchain.getState()
                validate = Trade.isValidTxn(block, currState)
                if validate :
                    txnList.append(block)
                    self.blockchain.updateState(block, currState)
                else:
                    continue
            self.blockchain.makeBlock(txnList)
            sleep(0.5)

    def run(self) :
        # Create Thread listen()
        threadAcptNode = Thread(target = self.threadAcceptNode, args = ())
        threadAcptNode.start()
        threadClNode = Thread(target = self.threadClientNode, args = ())
        threadClNode.start()
        threadClMsgNode = Thread(target = self.threadClientReadNode, args = ())
        threadClMsgNode.start()
        threadMineNode = Thread(target = self.threadMinningNode, args = ())
        threadMineNode.start()
