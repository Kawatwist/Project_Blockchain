from Tools.FormatMsg import *
from Tools.Connection import *
from Tools.Already_connected import *
from Genesisnode.GenesisnodeThread import *

import Tools.BlockchainClass as bc
import Tools.Transaction as Trade

from threading import Thread
from time import sleep
import ast

def ThreadListenClient(node, GN) :
    while True:
        co, addr = node.accept()
        print("New client joined the socket : ", addr)
        GN.threadId.append(CreateThread(ThreadParseClient, "Client", (co, GN)))

def ThreadParseClient(node, GN) :
    while True:
        newmsgenc = node.recv(1024)
        if newmsgenc :
            newmsg = newmsgenc.decode()
            msg = ast.literal_eval(newmsg)
            GN.bc.addBuffer(Trade.makeRealTransaction(msg.get("price"), msg.get("pay"), msg.get("payed"), msg.get("pricepayed")))
        else :
            break
