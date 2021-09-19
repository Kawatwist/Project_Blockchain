from FullnodeClass import Fullnode
from LightnodeClass import Lightnode
from GenesisnodeClass import Genesisnode

nodeName = {"full", "genesis", "light", "archive", "lightweight"}

handlersClass = {
    'full': Fullnode,
    'genesis': Genesisnode,
    'light':  Lightnode,
    'archive': Fullnode,
    'lightweight': Fullnode,
}

helperClass = {
    'full': "Node with a blockchain dup from the original, she can validate block",
    'genesis': "Node with blockchain recreate with every transaction, she can validate block",
    'light':  "A node without blockchain, she can only validate, she need to check from an other node for the block earlier",
    'archive': "Dup of the blockchain, this node cannot validate a block but can be use from a light node (as a fullnode/genesis)",
    'lightweight': "Block creation node, this node cannot validate a block, its only use to create a transaction"
}

class Config :
    type = "full"
    port = 4242
    host = "localhost"
    client = 4243
    listnode = []
    first = False

    def __init__(self, args) :
        if args.node :
            self.setType(args.node)
        if args.port :
            self.setPort(args.port)
        if args.host :
            self.setHost(args.host)
        if args.portCl :
            self.setPortClient(args.portCl)
        if args.new :
            self.first = args.new

    def printInfo(self) :
        print("\tType :", self.type)
        print("\tPort :", self.port)
        print("\tHost :", self.host)
        print("\tClient :", self.client)

    def setType(self, newtype) :
        self.type = newtype.lower()
    def setPort(self, newport) :
        self.port = newport
    def setHost(self, newhost) :
        self.host = newhost
    def setPortClient(self, newportclient) :
        self.client = newportclient
    def setFirstNode(self, first) :
        self.first = first

    def createNode(self) :
        if self.type in nodeName :
            print("Creation node : ")
            self.printInfo()
            self.node = handlersClass[self.type.lower()](self)
        elif self.type == "help" :
            print("Possible choice :", nodeName, "\n")
            for node in helperClass :
                print(node, " : ", helperClass[node])
        else :
            print("Invalid node, possible choice :", nodeName)
            exit
        # Call the right node constructor