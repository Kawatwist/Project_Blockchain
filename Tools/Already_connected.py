def IsAlreadyConnected(host, port, listSoc) :
    for check in listSoc :
        print("CHECK :", host, port, " With ", check["host"], check["port"])
        if check["host"] == host and check["port"] == port :
            return True
    print("HOST :", host, "Isnt connected")
    return False