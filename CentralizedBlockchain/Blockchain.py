import Chain.Chain as Chain
import Transaction.Hash as Hash
import Transaction.Transaction as Trade
import json, sys, re, socket, time

from threading import Thread
from time import sleep
import ast

clients = []
txnBuffer = []
timeout = 50

def threadConnection(arg):
    # print("Waiting Clients ...")
    while True :
        c, addr = arg.accept()
        # print ('New Clients : ', addr)
        print("asdas")
        clients.append({"c":c, "addr":addr, "timeout":time.time()})
        sleep(0.5)

def threadClient(arg):
    while True :
        for client in clients :
            newmsg = client.get("c").recv(1024).decode()
            if len(newmsg) != 0 :
                # print ("===========> client ", client.get("addr"), " : ", newmsg)
                try :
                    msg = ast.literal_eval(newmsg)
                    txnBuffer.append(Trade.makeRealTransaction(msg.get("price"), msg.get("pay"), msg.get("payed"), msg.get("pricepayed")))
                    client["timeout"] = time.time()
                except:
                    print("Incorrect message : ", newmsg, "\n")

            if time.time() - client.get("timeout")  > timeout :
                print("Remove client ", client.get("addr"), " Timeout ", "%.2f" % round(time.time() - client.get("timeout"), 2), " > ", timeout)
                clients.remove(client)
        # sleep(0.5)

def threadTermFunct(arg):
    while True :
        for line in sys.stdin :
            if line == 'Bal\n' :
                print("Balance : ", balance)
            if line == 'Cl\n' :
                print("Clients : ", clients)
            print("Line : ", line)
        sleep(0.5)


def main():
    # global state = {u'Pool':5000000}
    state = {u'Pool':50000000}  # Define the initial state (Give money)
    global balance
    balance = state
    genesisBlockTxns = [state]
    genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
    genesisHash = Hash.hashMe( genesisBlockContents )
    genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
    genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)
    chain = [genesisBlock]
    
    blockSizeLimit = 5  # Arbitrary number of transactions per block- 
                #  this is chosen by the block miner, and can vary between blocks!

    # Create Connection
    s = socket.socket()
    host = socket.gethostname()
    port = 4242
    s.bind((host, port))
    s.listen(5)
    print("Connection ready ", host, " At Port ", port)

    threadTerm = Thread(target = threadTermFunct, args = (s,))
    threadTerm.start()

    threadCo = Thread(target = threadConnection, args = (s,))
    threadCo.start()

    threadCl = Thread(target = threadClient, args = (s,))
    threadCl.start()


    while True :
        while len(txnBuffer) > 0:
            bufferStartSize = len(txnBuffer)
            
            ## Gather a set of valid transactions for inclusion
            txnList = []
            while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
                newTxn = txnBuffer.pop()
                validTxn = Trade.isValidTxn(newTxn,state) # This will return False if txn is invalid
                # print(validTxn)
                if validTxn:           # If we got a valid state, not 'False'
                    # print("Transaction Validate ", newTxn)
                    txnList.append(newTxn)
                    state = Trade.updateState(newTxn,state)
                else:
                    # print("Transaction Refused")
                    sys.stdout.flush()
                    continue  # This was an invalid transaction; ignore it and move on

            ## Make a block
            myBlock = Chain.makeBlock(txnList,chain)
            chain.append(myBlock)
            # print("\nState : ", state)
        balance = state
        # sleep(2)

if __name__ == '__main__':
    main()