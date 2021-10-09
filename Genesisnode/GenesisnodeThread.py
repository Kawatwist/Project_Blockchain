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

def ThreadListenNodePort(node, info, GN, dictSock) :
    while True:
        headerEnc = node.recv(headersz)
        if headerEnc :
            header = headerEnc.decode()
            typemsg = str(header[0 : 4])
            lenmsg = int(header[header.find('[') +1:header.find(']')])
            newmsgEnc = node.recv(lenmsg)
        else :
            print("Message empty we close connection to ", info)
            GN.listSoc.remove(dictSock)
            exit()
            continue
        if newmsgEnc :
            msg = newmsgEnc.decode()
            if len(msg) != 0 :
                print("Message connection :", typemsg, " For ", msg)
                if typemsg == str(head[1]) :
                    print("Join connection")
                    dmsg = eval(msg)
                    if not IsAlreadyConnected(dmsg["host"], dmsg["port"], GN.listSoc) :
                        JoinSocket = joinConnection(msg, GN)
                        GN.listSoc.append(JoinSocket)
                        GN.threadId.append(CreateThread(ThreadListenNodePort, JoinSocket["name"], (JoinSocket["socket"], JoinSocket["host"], JoinSocket["port"], GN)))
                elif typemsg == str(head[2]) :
                    print("Block")
                elif typemsg == str(head[4]) :
                    print("MSG :", msg)
                else :
                    print("Invalid Type")
        sleep(0.5)

def ThreadListenNode(node, host, hostport, GN) :
    while True:
        co, addr = node.accept()
        GN.threadId.append(CreateThread(ThreadAccept, addr, (co, GN)))

def ThreadAccept(node, GN) :
    HeaderConnection = node.recv(headersz)
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
        print("Connection failed")
        return
    dictSocket = dict({"host":msgdict["host"], "port":msgdict["port"], "name":msgdict["name"], "socket":node})
    sendSocket = dict({"host":msgdict["host"], "port":msgdict["port"], "name":msgdict["name"]})
    if len(GN.listSoc) > 1 :
        #Send to everyone connection
        for soc in GN.listSoc :
            if soc["name"] == "NodeOrigin" :
                continue
            print("Send to : ", soc["name"])
            createPackage(1, str(sendSocket), soc["socket"])
    GN.listSoc.append(dictSocket)
    ThreadGenesis(node, msg, GN, dictSocket)

def ThreadGenesis(node, info, GN, dictSock) :
    while True:
        headerEnc = node.recv(headersz)
        if headerEnc :
            header = headerEnc.decode()
            typemsg = str(header[0 : 4])
            lenmsg = int(header[header.find('[') +1:header.find(']')])
            newmsgEnc = node.recv(lenmsg)
        else :
            print("Message empty we close connection to ", info)
            GN.listSoc.remove(dictSock)
            exit()
            continue
        if newmsgEnc :
            msg = newmsgEnc.decode()
            if len(msg) != 0 :
                print("Message connection :", typemsg, " For ", msg)
                if typemsg == str(head[1]) :
                    print("Join connection")
                    dmsg = eval(msg)
                    if not IsAlreadyConnected(dmsg["host"], dmsg["port"], GN.listSoc) :
                        JoinSocket = joinConnection(msg, GN)
                        GN.listSoc.append(JoinSocket)
                        JoinClearSocket = dict({"host":JoinSocket["host"], "port":JoinSocket["port"], "name":JoinSocket["name"]})
                        GN.threadId.append(CreateThread(ThreadListenNodePort, JoinSocket["name"], (JoinSocket["socket"], JoinClearSocket, GN, JoinSocket)))
                elif typemsg == str(head[2]) :
                    print("Block")
                elif typemsg == str(head[4]) :
                    print("MSG :", msg)
                else :
                    print("Invalid Type")
        sleep(0.5)
