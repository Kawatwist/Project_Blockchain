def IsAlreadyConnected(host, port, listSoc) :
    for check in listSoc :
        if check["host"] == host && check["port"] == port :
            return True
    return False