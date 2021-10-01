from Tools.FormatMsg import *
from Tools.Connection import *
from Tools.BlockchainClass import ShareBc as bck

import Tools.BlockchainClass as bc
import Tools.Transaction as Trade

from threading import Thread
from time import sleep
import ast

def CreateThread(ThreadFunction, name, args) :
    threadId = Thread(target = ThreadFunction, args = args)
    threadId.start()
    return (dict({"ThreadId":threadId, "name":name}))

def ThreadListenNode(node) :
    while True:
        co, addr = node.accept()
        CreateThread(ThreadAcceptNode, "Im a fake Genesis", (co,))

def ThreadAcceptNode(node) :
    HeaderConnection = node.recv(headersz)
    if not HeaderConnection :
        print("Connection failed")
        return
    else :
        Header = HeaderConnection.decode()
        typemsg = str(Header[0 : 4])
        lenmsg = int(Header[Header.find('[') +1:Header.find(']')])
        ConnectionEnc = node.recv(lenmsg)
        if ConnectionEnc :
            msg = ConnectionEnc.decode()
        else :
            print("Connection failed on message :", Header)
            return
        if not typemsg == str(head[0]) :
            print("Incorrect Head :", typemsg, "!=", str(head[0]));
            print("Connection failed :", msg)
            return
        print("Welcome to ", msg)
    ThreadNode(node, msg)

def ThreadNode(node, me) :
    while True:
        headerEnc = node.recv(headersz)
        if headerEnc :
            header = headerEnc.decode()
            typemsg = str(header[0 : 4])
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
                    print("New connection (Node should be impossible)")
                elif typemsg == str(head[1]) :
                    print("Join connection")
                elif typemsg == str(head[2]) :
                    print("Block")
                else :
                    print("Invalid Type")
        sleep(0.5)

def ThreadToGenesis(node, me) :
    createPackage(0, str(me), node)
    while True:
        headerEnc = node.recv(headersz)
        if headerEnc :
            header = headerEnc.decode()
            typemsg = str(header[0 : 4])
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
                    print("New connection (Genesis should be impossible)")
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

