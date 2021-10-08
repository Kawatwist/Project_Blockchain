import Tools.Transaction as Trade
import socket

from Tools.FormatMsg import *
from Tools.Connection import *
from Tools.BlockchainClass import *
from Genesisnode.GenesisnodeThread import *
from Genesisnode.GenesisnodeUser import *
from Genesisnode.GenesisnodeTxn import *
from threading import Thread
from time import sleep

blockSizeLimit = 5

class Genesisnode :
    listUser = [] # User connected to this node
    listSoc = []  # Node with Socket
    threadId = [] # Dict {Thread, Name}
    bc = Blockchain()

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
        self.threadId.append(CreateThread(ThreadListenClient, "ThreadUser", (ClientSocket["socket"], self)))

        # Thread Validate / Add new Block to Blockchain
        self.threadId.append(CreateThread(ThreadMempoll, "ThreadMempoll", (self,)))

        # Manage new node connection
        OwnSocket = initConnectionListen(self.hostname, self.NodePort, "NodeOrigin")
        self.listSoc.append(OwnSocket)
        self.threadId.append(CreateThread(ThreadListenNode, "GenesisThread", (OwnSocket["socket"], self.hostname, self.NodePort, self)))
        while True :
            print("\n")
            for connected in self.listSoc :
                print("=>", connected["name"])
            for threadId in self.threadId :
                print("Thread :", str(threadId["name"]).ljust(25), "state :", threadId["ThreadId"].is_alive())
                if not threadId["ThreadId"].is_alive() :
                    self.threadId.remove(threadId)
            sleep(5)
