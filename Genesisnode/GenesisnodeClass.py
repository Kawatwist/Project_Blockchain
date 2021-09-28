import socket
from Tools.FormatMsg import *
import Tools.Transaction as Trade
import Tools.BlockchainClass as BC
from threading import Thread
from time import sleep
import ast

blockSizeLimit = 5

class Genesisnode :
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
        self.myPort = config.nodePort
        self.name = config.name
        save = dict({"host":self.myHost, "port":self.myPort, "name":self.name})
        self.listCo.append(save)
        self.mySocketNode.bind(("localhost", config.nodePort))
        self.mySocketNode.listen()
        self.mySocketClient.bind((self.myHost, config.clientPort))
        self.mySocketClient.listen()

    def connectionOrigin(self, config) :
        try :
            print("Connection Host ", config.host, ":", config.hostPort)
            self.originNode.connect((config.host, config.hostPort))
            # createPackage(0, str({"host":config.host, "port":self.myPort, "name":self.name}), newNode)
            save = dict({"host":config.host, "port":config.hostPort, "sock":self.originNode})
            self.listSoc.append(save)
            save = dict({"host":config.host, "port":config.hostPort, "name":"Genesis"})
            self.listCo.append(save)
            threadReadNode = Thread(target = self.threadReaderNode, args = (self.originNode,))
            threadReadNode.start()
            print("Connection success")
        except Exception as ex :
            raise Exception(ex)

    def checkAlreadyConnected(self, host, port) :
        for elem in self.listCo :
            if elem["host"] == host and elem["port"] == port :
                return True
        return False

    def joinNewNode(self, host, port, name) :
        try :
            if not self.checkAlreadyConnected(host, port) :
                print("Connection newNode (--jo) ", host, ":", port)
                newNode = socket.socket()
                newNode.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                newNode.connect((host, port))
                self.listNode.append(newNode)
                createPackage(0, str({"host":self.myHost, "port":self.myPort, "name":self.name}), newNode)
                threadReadNode = Thread(target = self.threadReaderNode, args = (newNode,))
                threadReadNode.start()
                save = dict({"host":host, "port":port,"sock":newNode})
                self.listSoc.append(save)
                save = dict({"host":host, "port":port, "name":name})
                self.listCo.append(save)
                print("Connection success")
        except Exception as ex :
            print("Error for ", host, port)
            raise Exception(ex)

    def threadAcceptNode(self) :
        while True:
            co, addr = self.mySocketNode.accept()
            print("New Node joined the socket : ", addr)
            #SEND TO EVERYONE HERE
            self.listNode.append(co)
            threadReadNode = Thread(target = self.threadReaderNode, args = (co,))
            threadReadNode.start()
            sleep(0.5)

    def sendBlockchain(self, newsoc) :
        if self.blockchain :
            chain = self.blockchain.getChain()
            if chain :
                for block in chain :
                    if block.getinfo()["contents"]["contents"]["blockNumber"] :
                        createPackage(2, str(block.getinfo()["contents"]), newsoc)

    def createNewConnection(self, newmsg:str, newsoc) :
        print("New connection found")
        addr = eval(newmsg[newmsg.find(str("{")):])
        if not self.checkAlreadyConnected(addr["host"], addr["port"]) :
            print("Check not found")
            save = dict({"host":addr["host"], "port":addr["port"],"sock":newsoc})
            self.listSoc.append(save)
            save = dict({"host":addr["host"], "port":addr["port"], "name":addr["name"]})
            self.listCo.append(save)
            for node in self.listSoc :
                print("Send to :", node["host"], ":", node["port"])
                createPackage(1, str(self.listCo), node["sock"])
            self.sendBlockchain(newsoc)

    def joinNewConnection(self, newmsg:str) :
        addr = eval(newmsg[newmsg.find("{"):newmsg.find("]")])
        for soc in addr :
            if not type(soc) == str:
                data = eval(str(soc))
                if data["host"] and data["port"] :
                    self.joinNewNode(data["host"], data["port"], data["name"])
        if not newmsg.find("--newBlock") == -1 :
            truncmsg = newmsg[newmsg.find("--newBlock") + 10:]
            while True :
                if not truncmsg.find(str("--newBlock")) == -1:
                    self.blockchain.addBlockBuffer(eval(truncmsg[:truncmsg.find("--newBlock")]))
                    truncmsg = newmsg[newmsg.find("--newBlock") + 10:]
                else :
                    self.blockchain.addBlockBuffer(eval(truncmsg))
                    break

    def threadReaderNode(self, node) :
        print("New Node reader created")
        while True:
            newmsghdenc = node.recv(headersz)
            print("Msg :", newmsghdenc)
            if newmsghdenc :
                newmsgdec = newmsghdenc.decode()
                lenmsg = int(newmsgdec[newmsgdec.find('[') +1:newmsgdec.find(']')])
                print("Lenmsg : ", lenmsg)
                newmsgenc = node.recv(lenmsg)
            else :
                exit()
                continue
            if newmsgenc :
                newmsg = newmsgenc.decode()
                if len(newmsg) != 0 :
                    if not newmsgdec.find(str(head[0])) == -1 :
                        value = eval(newmsg[newmsg.find(str("{")):])
                        print("New connection get : ", value["name"])
                        self.createNewConnection(newmsg, node)
                    elif not newmsgdec.find(head[1]) == -1 :
                        value = eval(newmsg[newmsg.find(str("{")):newmsg.find(str("}"))+1])
                        print("Join message get : ", value["name"])
                        self.joinNewConnection(newmsg)
                    elif not newmsgdec.find(head[2]) == -1 :
                        print("Block : ", newmsgdec)
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
                    msg = ast.literal_eval(newmsg)
                    self.blockchain.addBuffer(Trade.makeRealTransaction(msg.get("price"), msg.get("pay"), msg.get("payed"), msg.get("pricepayed")))

    def threadMinningNode(self) :
        while True :
            sizeBlockBuff = self.blockchain.getBlockBufferSize()
            while sizeBlockBuff > 0 :
                block = self.blockchain.getBlockBufferPop()
                print(sizeBlockBuff, "Block Receive by master : ", block)
                for txn in block["contents"]["txns"] :
                    currState = self.blockchain.getState()
                    # print("\n", block["contents"]["txnCount"] ,"Transaction : ", txn)
                    validate = Trade.isValidTxn(txn, currState)
                    print("txn valide :", validate)
                    if validate == True :
                        self.blockchain.setState(Trade.updateState(txn, currState))
                self.blockchain.tryAddBlock(block)
                print(self.blockchain.getState())
                sizeBlockBuff = self.blockchain.getBlockBufferSize()
                
            txnList = []
            size = self.blockchain.getBufferSize()
            if size > 0 :
                while len(txnList) < blockSizeLimit:
                    if self.blockchain.getBufferSize() > 0 :
                        block = self.blockchain.getBufferPop()
                        size -= 1
                        currState = self.blockchain.getState()
                        validate = Trade.isValidTxn(block, currState)
                        if validate :
                            txnList.append(block)
                            self.blockchain.setState(Trade.updateState(block, currState))
                            print("New state : ", self.blockchain.getState())
                        else:
                            continue
                    else:
                        break
                newBlock = self.blockchain.makeBlock(txnList)
                #Send it to everyone !
                for node in self.listSoc :
                    if newBlock.getinfo()["contents"]["contents"]["blockNumber"] :
                        createPackage(2, str(newBlock.getinfo()["contents"]), node["sock"])
            sleep(2)

    def run(self) :
        threadAcptNode = Thread(target = self.threadAcceptNode, args = ())
        threadAcptNode.start()
        threadClNode = Thread(target = self.threadClientNode, args = ())
        threadClNode.start()
        threadClMsgNode = Thread(target = self.threadClientReadNode, args = ())
        threadClMsgNode.start()
        threadMineNode = Thread(target = self.threadMinningNode, args = ())
        threadMineNode.start()
