import Tools.Hash as Hash

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
        # if info["data"] : # data ? Only for first ?
        #     self.data = info["data"]
        if info["contents"] :
            self.contents = info["contents"]

    def getinfo(self) :
        info = {}
        info["prev"] = self.prev_hash
        info["curr_hash"] = self.curr_hash
        # info["data"] = self.data
        info["contents"] = self.contents
        return info

    def getLastHash(self) :
        return self.curr_hash

    def getBlockNumb(self) :
        return self.contents["contents"]["blockNumber"]

class Blockchain :
    data = {u'Pool':500000}
    txnBuffer = []
    blockBuffer = []
    lastBlock = Block()
    lastHash = 0x0

    def __init__(self) :
        info = {}
        info["prev"] = 0x0
        info["txns"] = [self.data]
        data = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':info["txns"]}
        info["curr_hash"] = Hash.hashMe( data )
        info["contents"] = {u'hash':info["curr_hash"],u'contents':data}
        genesisBlock = Block()
        genesisBlock.setinfo(info)
        lastBlock = genesisBlock
        self.lastHash = None
        self.chain = []
        self.chain.append(genesisBlock)

    def getChain(self) :
        return self.chain

    def addBlockBuffer(self, msg) :
        self.blockBuffer.append(msg)
    
    def getBlockBufferPop(self) :
        return self.blockBuffer.pop()

    def addBuffer(self, msg) :
        self.txnBuffer.append(msg)
    
    def getBlockBufferSize(self) :
        return len(self.blockBuffer)

    def getBufferSize(self) :
        return len(self.txnBuffer)
    
    def getBufferPop(self) :
        return self.txnBuffer.pop()

    def getState(self) :
        return self.data

    def setState(self, state) :
        self.data = state

    def tryAddBlock(self, block) :
        self.makeBlock(block["contents"]["txns"])
        return True

    def makeBlock(self, txnList) :
        if len(self.chain) is 0 :
            print("Chain Empty ?!", self.chain)
            return
        saveinfo = {}
        for block in self.chain:
            if type(block) is type(Block()) :
                saveinfo = block.getinfo()
        saveBlock = Block()
        saveBlock.setinfo(saveinfo)
        info = {}
        info["prev"] = saveBlock.getLastHash()
        info["txns"] = [ txnList ] # Should be hashed
        data = {u'blockNumber':(saveBlock.getBlockNumb() + 1),u'parentHash':info["prev"],u'txnCount':len(txnList),'txns':txnList}
        info["curr_hash"] = Hash.hashMe(data)
        info["contents"] = {u'hash':info["curr_hash"],u'contents':data}
        newBlock = Block()
        self.lastHash = info["curr_hash"]
        newBlock.setinfo(info)
        self.chain.append(newBlock)
        for block in self.chain:
            if type(block) is type(Block()) :
                # print("Info block", block.getinfo()["contents"]["contents"]["blockNumber"], " : Nb txn :", block.getinfo()["contents"]["contents"]["txnCount"])
                saveinfo = block.getinfo()
        return newBlock
    
class ShareBc(object):
    blockchain = Blockchain()
        