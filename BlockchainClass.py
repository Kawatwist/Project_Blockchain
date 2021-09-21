import Transaction.Hash as Hash

blockSizeLimit = 5

class Block :
    info = {}
    contents = ""
    prev_hash = 0
    curr_hash = 0
    nonce = 0

    def __init__(self):
        self.contents = ""
        self.prev_hash = 0
        self.curr_hash = 0
        self.nonce = 0

    def setinfo(self, info) :
        if info["prev"] :
            self.prev_hash = info["prev"]
        if info["curr_hash"] :
            self.curr_hash = info["curr_hash"]
        if info["data"] : # data ? Only for first ?
            self.data = info["data"]
        if info["contents"] :
            self.contents = info["contents"]

    def getinfo(self) :
        self.info["prev"] = self.prev_hash
        self.info["curr_hash"] = self.curr_hash
        self.info["data"] = self.data
        self.info["contents"] = self.contents
        return self.info

    def getLastHash(self) :
        return self.curr_hash

    def getBlockNumb(self) :
        return self.data["blockNumber"]

class Blockchain :
    data = {u'Pool':500000}
    txnBuffer = []
    lastBlock = Block()
    
    def __init__(self) :
        info = {}
        info["prev"] = 0x0
        info["txns"] = [self.data]
        info["data"] = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':info["txns"]}
        info["curr_hash"] = Hash.hashMe( info["data"] )
        info["contents"] = {u'hash':info["curr_hash"],u'contents':info["data"]}
        genesisBlock = Block()
        genesisBlock.setinfo(info)
        self.chain = []
        self.chain.append(genesisBlock)

    def addBuffer(self, msg) :
        self.txnBuffer.append(msg)
    
    def getBufferSize(self) :
        return len(self.txnBuffer)
    
    def getBufferPop(self) :
        return self.txnBuffer.pop()

    def getState(self) :
        return self.data

    def getState(self, state) :
        self.data = state

    def makeBlock(self, txnList) :
        if len(self.chain) is 0 :
            print("Chain Empty ?!", self.chain)
            return
        for block in self.chain:
            self.lastBlock.setinfo(block.getinfo)
        info = {}
        info["prev"] = lastBlock.getLastHash()
        info["txns"] = [ txnList ] # Should be hashed
        info["data"] = {u'blockNumber':(lastBlock.getBlockNumb() + 1),u'parentHash':info["prev"],u'txnCount':len(txnList),'txns':txnList}
        info["curr_hash"] = Hash.hashMe(info["data"])
        info["contents"] = {u'hash':info["curr_hash"],u'contents':info["data"]}
        self.chain.append(info)
    
