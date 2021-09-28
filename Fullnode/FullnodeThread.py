from Tools.FormatMsg import *
from Tools.Connection import *
from Tools.BlockchainClass import ShareBc as bck
from threading import Thread
from time import sleep
import Tools.BlockchainClass as bc
import Tools.Transaction as Trade
import ast

def CreateThread(ThreadFunction, name, args) :
    threadId = Thread(target = ThreadFunction, args = args)
    threadId.start()
    return (dict({"ThreadId":threadId, "name":name}))

def ThreadListenNode(node) :
    while True:
        co, addr = node.accept()
        print("New Node joined the socket : ", addr)
        NodeSocket = initConnection(self.Host, self.HostPort, "Genesis")
        CreateThread(ThreadToGenesis, "Genesis", (NodeSocket["socket"],))

def ThreadToGenesis(node) :
    while True:
        headerEnc = node.recv(headersz)
        if headerEnc :
            header = headerEnc.decode()
            typemsg = str(header[2 : 4])
            lenmsg = int(header[header.find('[') +1:header.find(']')])
            newmsgEnc = node.recv(lenmsg)
        else :
            print("Message empty we close connection")
            exit()
            continue
        if newmsgEnc :
            msg = newmsgEnc.decode()
            if len(msg) != 0 :
                print("Message connection :", typemsg, " For ", msg)
                if typemsg == str(head[0]) :
                    print("New connection")
                elif typemsg == str(head[1]) :
                    print("Join connection")
                elif typemsg == str(head[2]) :
                    print("Block")
                else :
                    print("Invalid Type")
        sleep(0.5)

def ThreadListenClient(node) :
    while True:
        co, addr = node.accept()
        print("New client joined the socket : ", addr)
        CreateThread(ThreadParseClient, "Client", (co,))

def ThreadParseClient(node) :
    while True:
        newmsgenc = node.recv(1024)
        if newmsgenc :
            newmsg = newmsgenc.decode()
            msg = ast.literal_eval(newmsg)
            bck.blockchain.addBuffer(Trade.makeRealTransaction(msg.get("price"), msg.get("pay"), msg.get("payed"), msg.get("pricepayed")))

