headersz = 11
head = ["--co","--jo","--bl","--tx", "test"]

def createHeaderPackage(typeask, size) :
    header = head[typeask] + "["+ str(size).zfill(5) + "]"
    return (header)

def createPackage(typeask, msg, sock) :
    headmsg = createHeaderPackage(typeask, len(msg))
    print("Head :", headmsg)
    headenc = headmsg.encode()
    print("Headenc :", headenc)
    sock.send(headenc)
    sock.send(msg.encode())

