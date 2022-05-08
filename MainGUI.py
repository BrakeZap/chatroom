import json
import sys
import threading
import tkinter
from tkinter import *
from tkinter import ttk
import socket
import select
import _thread


class MainGUI(ttk.Frame):
    def changeChatRoom(self, event=None):
        if not self.conns[self.chatRooms.current()][0]:
            return
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(self.ipPortArray[self.chatRooms.current()])
        self.showMessages()
        _thread.start_new_thread(self.runConnection, (self.server,))

    def sendClientMessage(self, event=None):
        data1 = json.dumps({"username": self.username, "message": self.message.get()})
        self.server.send(data1.encode())
        self.messages.insert("", 'end', values=(self.chatRooms.get(), "You", self.message.get()))

    def sendServerMessage(self, username, message):
        self.messages.insert("", 'end', values=(self.chatRooms.get(), username, message))

    def runConnection(self, server):
        while True:

            # maintains a list of possible input streams
            sockets_list = [self.server]

            """ There are two possible input situations. Either the
            user wants to give manual input to send to other people,
            or the server is sending a message to be printed on the
            screen. Select returns from sockets_list, the stream that
            is reader for input. So for example, if the server wants
            to send a message, then the if condition will hold true
            below.If the user wants to send a message, the else
            condition will evaluate as true"""
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

            for socks in read_sockets:
                if socks == self.server:
                    data1 = socks.recv(2048)
                    data1 = json.loads(data1.decode())
                    self.sendServerMessage(data1.get("username"), data1.get("message"))
                else:
                    self.sendClientMessage()
        server.close()

    def showMessages(self):
        self.messages.grid(column=2, row=0)
        self.scrollBar.grid(column=3, row=0)
        self.entryMessage.grid(row=3, column=2)
        self.sendButton.grid(row=3, column=3)

    def createWidgets(self):
        # Creates a tree view element where the messages sent by users will be stored
        self.messages = ttk.Treeview(self.mainframe)
        # Creates 3 column name variables
        self.messages['columns'] = ("Chatroom", "Name", "Message")
        # There is a hidden 0th column, so set the width to 0
        self.messages.column("#0", width=0, stretch=NO)

        # Set each column to have a specific width and anchor point
        self.messages.column("Chatroom", anchor=tkinter.W, width=100)
        self.messages.column("Name", anchor=CENTER, width=160)
        self.messages.column("Message", anchor=tkinter.W, width=350)
        self.messages.heading("#0")
        # Set the top text of each column
        self.messages.heading("Chatroom", text="Chatroom")
        self.messages.heading("Name", text="Name")
        self.messages.heading("Message", text="Message")
        # Set the grid position of the tree view (Needs to be changed around to look good in the future...)
        self.messages.grid(column=2, row=0)

        # Create a scrollbar to scroll through past messages
        self.scrollBar = ttk.Scrollbar(self.mainframe, orient="vertical", command=self.messages.yview)
        self.scrollBar.grid(column=3, row=0)

        # Creates the input variable that listens to sent message
        self.message = StringVar()
        self.message.set("Type your message here: ")
        self.entryMessage = ttk.Entry(self.mainframe, textvariable=self.message)
        self.entryMessage.grid(row=3, column=2)

        # Creates the send button which fires the sendMessage function when clicked
        self.sendButton = ttk.Button(self.mainframe, text="Send", command=self.sendClientMessage)
        self.sendButton.grid(row=3, column=3)

    def hideWidgets(self):
        self.messages.grid_forget()
        self.scrollBar.grid_forget()
        self.entryMessage.grid_forget()
        self.sendButton.grid_forget()

    def checkConnections(self, conns=None):
        print(conns)
        if conns is None:
            conns = []
        if not conns:
            return

        locIp = conns[0]
        locPort = conns[1]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        code = s.connect_ex((locIp, locPort))
        if code == 0:
            byte = "123"
            s.send(byte.encode())
            receive = sys.getsizeof(int)
            locData = s.recv(receive)
            numClients = int(locData.decode())

            self.conns.append((True, numClients - 1))
        else:
            self.conns.append((False, -1))
        s.close()

    def __init__(self, parent, username):
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")
        self.server = None
        self.sendButton = None
        self.entryMessage = None
        self.message = None
        self.scrollBar = None
        self.messages = None
        self.ips = []
        with open("info.json") as file:
            locData = json.load(file)
            self.ips.append(locData["ip1"])
            self.ips.append(locData["ip2"])
            self.ips.append(locData["ip3"])
        self.username = username
        # Setup main frame of GUI
        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky="N, W, E, S")

        # Sets current chatrooms label
        label = ttk.Label(self.mainframe, text="Current chatrooms: ")
        label['font'] = "TkHeadingFont"
        label.grid(column=1, row=0, sticky="W, E")

        # Creates the dropdown menu to choose the chatroom.
        self.chatRooms = ttk.Combobox(self.mainframe, width=60, height=40)
        # Binds the event of changing chatrooms to the changeChatRoom function
        self.chatRooms.bind("<<ComboboxSelected>>", self.changeChatRoom)
        self.chatRooms.grid(column=1, row=2, sticky="W, E")
        self.chatRooms.state(["readonly"])
        self.ipPortArray = []
        for value in self.ips:
            ip = value[:value.index(':')]
            port = int(value[value.index(':') + 1:])
            self.ipPortArray.append((ip, port))
        self.conns = []
        thread1 = threading.Thread(target=self.checkConnections, args=[self.ipPortArray[0]])
        thread2 = threading.Thread(target=self.checkConnections, args=[self.ipPortArray[1]])
        thread3 = threading.Thread(target=self.checkConnections, args=[self.ipPortArray[2]])
        thread1.start()
        thread2.start()
        thread3.start()
        thread1.join()
        thread2.join()
        thread3.join()
        print(self.conns)
        chatrooma = f"Chatroom A: {self.ips[0]}. Online: {self.conns[0][0]}. {self.conns[0][1]} online currently."
        chatroomb = f"Chatroom B: {self.ips[1]}. Online: {self.conns[1][0]}. {self.conns[1][1]} online currently."
        chatroomc = f"Chatroom C: {self.ips[2]}. Online: {self.conns[2][0]}. {self.conns[2][1]} online currently."
        self.chatRooms['values'] = (chatrooma, chatroomb, chatroomc)

        self.createWidgets()
        self.hideWidgets()
