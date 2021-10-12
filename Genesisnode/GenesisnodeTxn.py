from Tools.FormatMsg import *
from Tools.Connection import *
from Tools.Already_connected import *
from Genesisnode.GenesisnodeThread import *

import Tools.BlockchainClass as bc
import Tools.Transaction as Trade

from threading import Thread
from time import sleep
import ast

blockSizeLimit = 25

def ThreadMempoll(GN) :
    while True:
        sizeBlockBuff = GN.bc.getBlockBufferSize()
        while sizeBlockBuff > 0 :
            block = GN.bc.getBlockBufferPop()
            print(sizeBlockBuff, "Block Receive by master : ", block)
            for txn in block["contents"]["txns"] :
                currState = GN.bc.getState()
                # print("\n", block["contents"]["txnCount"] ,"Transaction : ", txn)
                validate = Trade.isValidTxn(txn, currState)
                print("txn valide :", validate)
                if validate == True :
                    GN.bc.setState(Trade.updateState(txn, currState))
            GN.bc.tryAddBlock(block)
            print(GN.bc.getState())
            sizeBlockBuff = GN.bc.getBlockBufferSize()
            
        txnList = []
        size = GN.bc.getBufferSize()
        if size > 0 :
            while len(txnList) < blockSizeLimit:
                if GN.bc.getBufferSize() > 0 :
                    block = GN.bc.getBufferPop()
                    size -= 1
                    currState = GN.bc.getState()
                    validate = Trade.isValidTxn(block, currState)
                    if validate :
                        txnList.append(block)
                        GN.bc.setState(Trade.updateState(block, currState))
                        print("New state : ", GN.bc.getState())
                    else:
                        continue
                else:
                    break
            newBlock = GN.bc.makeBlock(txnList)
            #Send it to everyone !
            for node in GN.listSoc :
                if node["name"] == "NodeOrigin" :
                    continue
                if newBlock.getinfo()["contents"]["contents"]["blockNumber"] :
                    createPackage(2, str(newBlock.getinfo()), node["socket"])
                    # nextblock = "--newBlock" + str(newBlock.getinfo()["contents"])
                    # print("Send :", newBlock.getinfo()["contents"])
                    # node["sock"].send(nextblock.encode())
            print("New state : ", GN.bc.getState())
        sleep(2)
