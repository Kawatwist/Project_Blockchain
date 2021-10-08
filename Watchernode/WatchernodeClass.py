import Tools.Transaction as Trade
import socket

from Tools.FormatMsg import *
from Tools.Connection import *
from Watchernode.WatchernodeThread import *
from threading import Thread
from time import sleep
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPalette
import os
blockSizeLimit = 5

class Watchernode :
    listUser = [] # User connected to this node
    # listNode = [] # Node info (without socket for sending)
    listSoc = []  # Node with Socket
    threadId = [] # Dict {Thread, Name}
    quit = False

    def __init__(self, config) :
        self.app = QApplication([])
        self.config = config
        self.Host = config.host
        self.HostPort = config.hostPort
        self.NodePort = config.nodePort
        self.ClientPort = config.clientPort
        self.Name = config.name                        

    def run(self) :
        # Create my connection to the Genesis / First Node
        Me = dict({"host":self.Host, "port":self.NodePort, "name":self.Name})
        GenesisSocket = initConnection(self.Host, self.HostPort, "Genesis")
        self.listSoc.append(GenesisSocket)
        self.threadId.append(CreateThread(ThreadToGenesis, "Genesis", (GenesisSocket["socket"], Me, self)))

        # Create my connection for the Client
        # /!\ self.Host (should be myIP for this one) /!\ #
        ClientSocket = initConnectionListen(self.Host, self.ClientPort, "ClientOrigin")
        self.listSoc.append(ClientSocket)
        self.listUser.append(ClientSocket)
        self.threadId.append(CreateThread(ThreadListenClient, "Client", (ClientSocket["socket"], self)))

        # Manage new node connection
        OwnSocket = initConnectionListen(self.Host, self.NodePort, "NodeOrigin")
        self.listSoc.append(OwnSocket)
        self.threadId.append(CreateThread(ThreadListenNode, "Me", (OwnSocket["socket"], self)))
        
        self.app.setStyle('Fusion')
        window = QWidget()
        layout = QVBoxLayout(window)
        window.show()
        while True :
            display = "User connected :\n"
            for user in self.listSoc:
                display += "\t" + str(user["name"]) + "\n"
            display += "Thread :\n"
            layout.addWidget(QLabel(str(display)))
            Button = []
            i = 0;
            for thread in self.threadId:
                i += 1;
                palette = QPalette()
                if thread["ThreadId"].is_alive():
                    palette.setColor(QPalette.ButtonText, Qt.green)
                else :
                    palette.setColor(QPalette.ButtonText, Qt.red)
                self.app.setPalette(palette)
                Button = QPushButton(str(thread["name"]))
                Button.clicked.connect(lambda:self.KillThread(Button))
                layout.addWidget(Button)
            window.setLayout(layout)
            window.update()
            self.app.exec()
            if self.app.aboutToQuit :
                self.app.quit()
                self.quit = True
                for user in self.listSoc:
                    user["socket"].close()
                for thread in self.threadId:
                    if thread["ThreadId"].is_alive() :
                        print("Thread join :", thread["name"])
                        thread["ThreadId"].join()
                print("Closing apps")
                break;
            sleep(2)

    def KillThread(self,Button) :
        print("Thread button pressed :", Button.text())
