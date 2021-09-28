import socket

def initConnectionListen(host, port, name) :
    print("Create connection for :", name, " ", host, ":",port)
    newSocket = socket.socket()
    newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    newSocket.bind((host, port))
    newSocket.listen()
    dictSocket = dict({"host":host, "port":port, "name":name, "socket":newSocket})
    return (dictSocket)

def initConnection(host, port, name) :
    print("Create connection for :", name, " ", host, ":",port)
    newSocket = socket.socket()
    newSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    newSocket.connect((host, port))
    dictSocket = dict({"host":host, "port":port, "name":name, "socket":newSocket})
    return (dictSocket)