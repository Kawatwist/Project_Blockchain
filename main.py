import Chain.Chain as Chain
import Transaction.Hash as Hash
import Transaction.Transaction as Trade
import json

def main():
    txnBuffer = [Trade.makeTransaction() for i in range(30)]
    state = {u'Alice':50, u'Bob':50}  # Define the initial state (Give money)
    genesisBlockTxns = [state]
    genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
    genesisHash = Hash.hashMe( genesisBlockContents )
    genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
    genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)
    chain = [genesisBlock]
    
    blockSizeLimit = 5  # Arbitrary number of transactions per block- 
                #  this is chosen by the block miner, and can vary between blocks!

    while len(txnBuffer) > 0:
        bufferStartSize = len(txnBuffer)
        
        ## Gather a set of valid transactions for inclusion
        txnList = []
        while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
            newTxn = txnBuffer.pop()
            validTxn = Trade.isValidTxn(newTxn,state) # This will return False if txn is invalid
            
            if validTxn:           # If we got a valid state, not 'False'
                txnList.append(newTxn)
                state = Trade.updateState(newTxn,state)
            else:
                print("Transaction Refused")
                sys.stdout.flush()
                continue  # This was an invalid transaction; ignore it and move on

        ## Make a block
        myBlock = Chain.makeBlock(txnList,chain)
        chain.append(myBlock)
        for CChain in chain:
            print(CChain)

if __name__ == '__main__':
    main()