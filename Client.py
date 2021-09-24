import socket
import datetime
from time import sleep
import sys

def main():
    port = 4243
    pay = 'Bob'
    price = 5
    payed = 'Alice'
    newclient = ''
    pricepayed = 5
    i = 0
    while i < len(sys.argv) :
        if sys.argv[i] == '-p' and len(sys.argv) > i :
            port = int(sys.argv[i + 1])
        elif sys.argv[i] == 'pay' and len(sys.argv) > i :
            payed = sys.argv[i + 1]
        elif sys.argv[i] == 'payed' and len(sys.argv) > i :
            pay = sys.argv[i + 1]
        elif sys.argv[i] == 'price' and len(sys.argv) > i :
            price = float(sys.argv[i + 1])
        i+=1

    pricepayed = -price
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = "localhost"
    s.connect((host, port))

    msg = str(dict({"pay":pay, "price":price, "payed":payed, "pricepayed":pricepayed}))
    print(msg)
    s.send(msg.encode())
    s.close()

if __name__ == '__main__':
    main()