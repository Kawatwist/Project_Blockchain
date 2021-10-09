from Fullnode.FullnodeClass import Fullnode
from Genesisnode.GenesisnodeClass import Genesisnode

import pkg_resources
installed = {pkg.key for pkg in pkg_resources.working_set}
if 'pyqt5' in installed :
    from Watchernode.WatchernodeClass import Watchernode
else :
    Watchernode = "NotDefined"

nodeName = {"full", "genesis", "light", "archive", "lightweight", "watcher"}

handlersClass = {
    'full':Fullnode,
    'genesis': Genesisnode,
    'watcher': Watchernode,
    'light':  Fullnode,# ! OLD VERSION !
    'archive': Fullnode, # ! OLD VERSION !
    'lightweight': Fullnode, # ! OLD VERSION !
}

helperClass = {
    'full': "Node with a blockchain dup from the original, she can validate block",
    'genesis': "Node with blockchain recreate with every transaction, she can validate block",
    'light':  "A node without blockchain, she can only validate, she need to check from an other node for the block earlier",
    'archive': "Dup of the blockchain, this node cannot validate a block but can be use from a light node (as a fullnode/genesis)",
    'lightweight': "Block creation node, this node cannot validate a block, its only use to create a transaction"
}

class Config :
    typenode = "Nothing"
    hostPort = 4242
    host = "localhost"
    nodePort = 4243
    clientPort = 4343
    name = ""
    master = False

    def __init__(self, args, wallet) :
        self.wallet = wallet
        if args.nodeType :
            self.setType(args.nodeType)
        if args.hostPort :
            self.setPort(args.hostPort)
        if args.host :
            self.setHost(args.host)
        if args.nodePort :
            self.setPortNode(args.nodePort)
        if args.clientPort :
            self.setPortClient(args.clientPort)
        if args.name :
            self.name = args.name

    def printInfo(self) :
        print("\tType :", self.typenode)
        print("\tPort :", self.hostPort)
        print("\tHost :", self.host)
        print("\tPortNode :", self.nodePort)
        print("\tClient :", self.clientPort)

    def setType(self, newtype) :
        self.typenode = newtype.lower()
    def setPort(self, newport) :
        self.hostPort = newport
    def setHost(self, newhost) :
        self.host = newhost
    def setPortNode(self, newportnode) :
        self.nodePort = newportnode
    def setPortClient(self, newportclient) :
        self.clientPort = newportclient
    def setFirstNode(self, first) :
        self.master = first

    def createNode(self) :
        if self.typenode in nodeName :
            print("Creation node : ")
            self.printInfo()
            if self.typenode.lower() == "watcher" and Watchernode == "NotDefined" :
                print("PyQt5 is requiered to start in watcher mode")
                self.node = False
            else :
                self.node = handlersClass[self.typenode.lower()](self)

        elif self.typenode == "help" :
            print("Possible choice :", nodeName, "\n")
            for node in helperClass :
                print(node, " : ", helperClass[node])
        else :
            print("Invalid node, possible choice :", nodeName)
        # Call the right node constructor