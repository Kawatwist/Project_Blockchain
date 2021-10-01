import Tools.Transaction as Trade
import socket

from Tools.FormatMsg import *
from Tools.Connection import *
from Genesisnode.GenesisnodeThread import *
from threading import Thread
from time import sleep

blockSizeLimit = 5

class Genesisnode :
    listUser = [] # User connected to this node
    # listNode = [] # Node info (without socket for sending)
    listSoc = []  # Node with Socket
    threadId = [] # Dict {Thread, Name}

    def __init__(self, config) :
        self.config = config
        self.NodePort = config.nodePort
        self.ClientPort = config.clientPort
        self.Name = config.name
        self.hostname = socket.gethostname()
        self.local_ip = socket.gethostbyname(self.hostname)
        print("MyIP :", self.hostname, " ", self.local_ip)
        self.hostname = "localhost"
        print("Change Hostname to ", self.hostname)

    def run(self) :
        # Create my connection for the Client
        # /!\ self.Host (should be myIP for this one) /!\ #
        ClientSocket = initConnectionListen(self.hostname, self.ClientPort, "ClientOrigin")
        self.listUser.append(ClientSocket)
        self.threadId.append(CreateThread(ThreadListenClient, "Client", (ClientSocket["socket"],)))

        # Thread Validate / Add new Block to Blockchain

        # Manage new node connection
        OwnSocket = initConnectionListen(self.hostname, self.NodePort, "NodeOrigin")
        self.listSoc.append(OwnSocket)
        self.threadId.append(CreateThread(ThreadListenNode, "Me", (OwnSocket["socket"], self.hostname, self.NodePort, self)))
        while True :
            print("\n")
            for connected in self.listSoc :
                print("=>", connected["name"])
            sleep(5)