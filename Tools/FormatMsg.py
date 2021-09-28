headersz = 11
head = ["--co","--jo","--bl","--tx"]

def createHeaderPackage(typeask, size) :
    header = head[typeask] + "["+ str(size).zfill(5) + "]"
    return (header)

def createPackage(type, msg, sock) :
    headmsg = createHeaderPackage(type, len(msg))
    sock.send(headmsg.encode())
    sock.send(msg.encode())

