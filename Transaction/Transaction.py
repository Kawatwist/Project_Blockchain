import random
random.seed(0)

    #Selected Transaction
def makeRealTransaction(amountpay, pay, payed, amountpayed):
    return {pay:amountpay,payed:amountpayed}

    # Random Transaction
def makeTransaction(maxValue=3):
    sign      = int(random.getrandbits(1))*2 - 1
    amount    = random.randint(1,maxValue)
    pay       = sign * amount
    receive   = -1 * pay
    return {u'Alice':pay,u'Bob':receive}

    # Update with new entry
def updateState(txn, state):
    state = state.copy() # As dictionaries are mutable, let's avoid any confusion by creating a working copy of the data.
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state

    # Check the Validity
def isValidTxn(txn,state):
    if sum(txn.values()) != 0.0:
        print(sum(txn.values()))
        return False
    for key in txn.keys():
        if key in state.keys():
            acctBalance = state[key]
        else:
            acctBalance = 0
        if (acctBalance + txn[key]) < 0:
            return False
    
    return True