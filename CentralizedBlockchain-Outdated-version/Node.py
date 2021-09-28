import argparse
from threading import Thread
import socket
from time import sleep
import time
import Chain.Chain as Chain
import Transaction.Hash as Hash
import Transaction.Transaction as Trade
import ast

clients = []
msg = []
timeout = 50

def connectionUser(arg):
    print("Waiting Clients ...")
    while True :
        c, addr = arg.accept()
        print ('New Clients : ', addr)
        clients.append({"c":c, "addr":addr, "timeout":time.time()})
        # sleep(0.5)

def commsUser(arg):
    while True :
        for client in clients :
            newmsg = client.get("c").recv(1024).decode()
            if len(newmsg) != 0 :
                print ("===========> client ", client.get("addr"), " : ", newmsg)
                try :
                    print("MSG : ", newmsg)
                    msgUser = ast.literal_eval(newmsg)
                    print("2\n")
                    msg.append(msgUser)
                    # msg.append(Trade.makeRealTransaction(msgUser.get("price"), msgUser.get("pay"), msgUser.get("payed"), msgUser.get("pricepayed")))
                    client["timeout"] = time.time()
                except Exception as e:
                    print(e)
                    print("Incorrect message : ", newmsg, "\n")

            if time.time() - client.get("timeout")  > timeout :
                print("Remove client ", client.get("addr"), " Timeout ", "%.2f" % round(time.time() - client.get("timeout"), 2), " > ", timeout)
                clients.remove(client)
        # sleep(0.5)

def connectionBlockchain(host, port):
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, port))
    while True:
        if msg and msg[0] :
            print(msg[0])
            send = msg[0]
            s.send(str(send).encode())
            msg.remove(msg[0])
        # else :
        #     print("Waiting Block")
        # sleep(5)
    s.close()

def main():
    parser = argparse.ArgumentParser(description='Blockchain basic node.')
    parser.add_argument('--port', required=False, type=int, help='Port on which connect the BC.')
    parser.add_argument('--host', required=False, type=str, help='Host ip')
    parser.add_argument('--portClient', required=False, type=int, help='Port on which run the node.')

    args = parser.parse_args()
    port = args.port if args.port else 4242
    host = args.host if args.host else "127.0.0.1"
    portClient = args.portClient if args.portClient else 4243

    s = socket.socket()
    hostClient = socket.gethostname()
    s.bind((hostClient, portClient))
    s.listen(5)
    print("Node up for client connection : ", hostClient, " At Port ", portClient)

    threadUser = Thread(target = connectionUser, args = (s,))
    threadUser.start()

    threadUser = Thread(target = commsUser, args = (s,))
    threadUser.start()

    connectionBlockchain(host, port)


if __name__ == '__main__':
    main()