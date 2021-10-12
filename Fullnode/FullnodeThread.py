from Tools.FormatMsg import *
from Tools.Connection import *
from Tools.Already_connected import *
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

def ThreadListenNode(node, FN) :
    while True:
        co, addr = node.accept()
        FN.threadId.append(CreateThread(ThreadAcceptNode, addr, (co, FN)))
        #SEND TO EVERYONE A TESTMSG
        for soc in FN.listSoc :
            if soc["name"] == "NodeOrigin" :
                continue
            createPackage(4, "POG TEST", soc["socket"])

def ThreadAcceptNode(node, FN) :
    HeaderConnection = node.recv(headersz)
    print("RECV :", HeaderConnection)
    if HeaderConnection :
        Header = HeaderConnection.decode()
        typemsg = str(Header[0 : 4])
        lenmsg = int(Header[Header.find('[') +1:Header.find(']')])
        ConnectionEnc = node.recv(lenmsg)
        if ConnectionEnc :
            msg = ConnectionEnc.decode()
            msgdict = eval(msg)
        else :
            print("Connection failed on message :", Header)
            return
        if not typemsg == str(head[0]) :
            print("Incorrect Head :", typemsg, "!=", str(head[0]));
        print("Welcome to ", msgdict["name"])
    else :
        print("Connection failed (Header in AcceptNode)")
        return
    dictSocket = dict({"host":msgdict["host"], "port":msgdict["port"], "name":msgdict["name"], "socket":node})
    sendSocket = dict({"host":msgdict["host"], "port":msgdict["port"], "name":msgdict["name"]})
    if len(FN.listSoc) > 1 :
        #Send to everyone connection
        for soc in FN.listSoc :
            if soc["name"] == "NodeOrigin" :
                continue
            print("Send to : ", soc["name"])
            createPackage(1, str(sendSocket), soc["socket"])
    FN.listSoc.append(dictSocket)
    ThreadNode(node, msg, dictSocket, FN)

def ThreadNode(node, me, dictSocket, FN) :
    while True:
        headerEnc = node.recv(headersz)
        if headerEnc :
            header = headerEnc.decode()
            typemsg = str(header[0 : 4])
            lenmsg = int(header[header.find('[') +1:header.find(']')])
            newmsgEnc = node.recv(lenmsg)
        else :
            print("Message empty we close connection")
            FN.listSoc.remove(dictSocket)
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
                    dmsg = eval(msg)
                    if not IsAlreadyConnected(dmsg["host"], dmsg["port"], FN.listSoc) :
                        JoinSocket = joinConnection(msg, FN)
                        JoinClearSocket = dict({"host":JoinSocket["host"], "port":JoinSocket["port"], "name":JoinSocket["name"]})
                        FN.threadId.append(CreateThread(ThreadNode, JoinSocket["name"], (JoinSocket["socket"], JoinClearSocket, JoinSocket, FN)))
                        #SEND TO EVERYONE A TESTMSG
                        for soc in FN.listSoc :
                            if soc["name"] == "NodeOrigin" :
                                continue
                            print("Send to :", soc["name"])
                            createPackage(4, "POGZZ", soc["socket"])
                elif typemsg == str(head[2]) :
                    dmsg = eval(msg)
                    FN.bc.tryAddBlock2(dmsg)
                    print("New state : ", FN.bc.getState())
                    print("Block")
                elif typemsg == str(head[4]) :
                    print("MSG : ", msg)
                else :
                    print("Invalid Type")
        sleep(0.5)

def ThreadToGenesis(node, me, FN, dictSocket) :
    createPackage(0, str(me), node)
    while True:
        headerEnc = node.recv(headersz)
        if headerEnc :
            header = headerEnc.decode()
            typemsg = str(header[0 : 4])
            lenmsg = int(header[header.find('[') +1:header.find(']')])
            newmsgEnc = node.recv(lenmsg)
        else :
            print("Message empty we close connection (ToGenesisFunction)")
            FN.listSoc.remove(dictSocket)
            exit()
            continue
        if newmsgEnc :
            msg = newmsgEnc.decode()
            if len(msg) != 0 :
                print("Message connection :", typemsg, " For ", msg)
                if typemsg == str(head[1]) :
                    print("Join connection")
                    dmsg = eval(msg)
                    if not IsAlreadyConnected(dmsg["host"], dmsg["port"], FN.listSoc) :
                        JoinSocket = joinConnection(msg, FN)
                        FN.listSoc.append(JoinSocket)
                        JoinClearSocket = dict({"host":JoinSocket["host"], "port":JoinSocket["port"], "name":JoinSocket["name"]})
                        FN.threadId.append(CreateThread(ThreadNode, JoinSocket["name"], (JoinSocket["socket"], JoinClearSocket, JoinSocket, FN)))
                        #SEND TO EVERYONE A TESTMSG
                        for soc in FN.listSoc :
                            if soc["name"] == "NodeOrigin" :
                                continue
                            createPackage(4, "POG TEST", soc["socket"])
                elif typemsg == str(head[2]) :
                    dmsg = eval(msg)
                    FN.bc.tryAddBlock2(dmsg)
                    print("New state : ", FN.bc.getState())
                    print("Block")
                elif typemsg == str(head[4]) :
                    print("MSG :", msg)
                else :
                    print("Invalid Type")
        sleep(0.5)

def ThreadListenClient(node, FN) :
    while True:
        co, addr = node.accept()
        print("New client joined the socket : ", addr)
        FN.threadId.append(CreateThread(ThreadParseClient, "User :" + addr, (co,)))

def ThreadParseClient(node) :
    while True:
        newmsgenc = node.recv(1024)
        if newmsgenc :
            newmsg = newmsgenc.decode()
            msg = ast.literal_eval(newmsg)
            bck.blockchain.addBuffer(Trade.makeRealTransaction(msg.get("price"), msg.get("pay"), msg.get("payed"), msg.get("pricepayed")))

