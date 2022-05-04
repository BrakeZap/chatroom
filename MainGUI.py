import json
from tkinter import *
from tkinter import ttk
import socket
import select
import _thread

with open('info.json') as jsonFile:
    data = json.load(jsonFile)
IP_address = data["ip"]
port = 8080  # TODO: Change to actual values


class MainGUI(ttk.Frame):
    # TODO: Disconnect from current chat room and enter another
    def changeChatRoom(self, event=None):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((IP_address, port))
        self.showMessages()
        _thread.start_new_thread(self.runConnection, (self.server,))

    def sendClientMessage(self, event=None):
        data = json.dumps({"username": self.username, "message": self.message.get()})
        self.server.send(data.encode())
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
                    data = socks.recv(2048)
                    data = json.loads(data.decode())
                    self.sendServerMessage(data.get("username"), data.get("message"))
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
        self.messages.column("Chatroom", anchor=CENTER, width=20)
        self.messages.column("Name", anchor=CENTER, width=80)
        self.messages.column("Message", anchor=CENTER, width=180)
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

    def __init__(self, parent, username):
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")
        self.server = None
        self.sendButton = None
        self.entryMessage = None
        self.message = None
        self.scrollBar = None
        self.messages = None
        self.username = username
        # Setup main frame of GUI
        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky="N, W, E, S")

        # Sets current chatrooms label
        label = ttk.Label(self.mainframe, text="Current chatrooms: ")
        label['font'] = "TkHeadingFont"
        label.grid(column=1, row=0, sticky="W, E")

        # Creates the dropdown menu to choose the chatroom.
        self.chatRooms = ttk.Combobox(self.mainframe)
        # Binds the event of changing chatrooms to the changeChatRoom function
        self.chatRooms.bind("<<ComboboxSelected>>", self.changeChatRoom)
        self.chatRooms.grid(column=1, row=2, sticky="W, E")
        self.chatRooms.state(["readonly"])
        # TODO: Change chatroom values to the actual available chatrooms
        self.chatRooms['values'] = ('Chatroom A', 'Chatroom B', 'Chatroom C')

        self.createWidgets()
        self.hideWidgets()
