import Tools.Transaction as Trade
import socket

from Tools.FormatMsg import *
from Tools.Connection import *
from Fullnode.FullnodeThread import *
from threading import Thread
from time import sleep

blockSizeLimit = 5

class Fullnode :
    listUser = [] # User connected to this node
    # listNode = [] # Node info (without socket for sending)
    listSoc = []  # Node with Socket
    threadId = [] # Dict {Thread, Name}

    def __init__(self, config) :
        self.config = config
        self.Host = config.host
        self.HostPort = config.hostPort
        self.NodePort = config.nodePort
        self.ClientPort = config.clientPort
        self.Name = config.name                        

    def run(self) :
        # Create my connection to the Genesis / First Node
        GenesisSocket = initConnection(self.Host, self.HostPort, "Genesis")
        self.listSoc.append(GenesisSocket)
        self.threadId.append(CreateThread(ThreadToGenesis, "Genesis", (GenesisSocket["socket"],)))

        # Create my connection for the Client
        # /!\ self.Host (should be myIP for this one) /!\ #
        ClientSocket = initConnectionListen(self.Host, self.ClientPort, "ClientOrigin")
        self.listUser.append(ClientSocket)
        self.threadId.append(CreateThread(ThreadListenClient, "Client", (ClientSocket["socket"],)))