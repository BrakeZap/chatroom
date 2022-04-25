import tkinter
from tkinter import *
from tkinter import ttk


class MainGUI(ttk.Frame):
    # TODO: Disconnect from current chat room and enter another
    def changeChatRoom(self, event=None):
        pass

    # TODO: Change "Kyle" to client's actual name
    def sendMessage(self, event=None):
        self.messages.insert("", 'end', values=(self.chatRooms.get(), self.username, self.message.get()))

    def __init__(self, parent, username):
        ttk.Frame.__init__(self, parent, padding="3 3 12 12")
        self.username = username
        # Setup main frame of GUI
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky="N, W, E, S")

        # Sets current chatrooms label
        label = ttk.Label(mainframe, text="Current chatrooms: ")
        label['font'] = "TkHeadingFont"
        label.grid(column=1, row=0, sticky="W, E")

        # Creates the dropdown menu to choose the chatroom.
        self.chatRooms = ttk.Combobox(mainframe)
        # Binds the event of changing chatrooms to the changeChatRoom function
        self.chatRooms.bind("<<ComboboxSelected>>", self.changeChatRoom)
        self.chatRooms.grid(column=1, row=2, sticky="W, E")
        self.chatRooms.state(["readonly"])
        # TODO: Change chatroom values to the acutal avaliable chatrooms
        self.chatRooms['values'] = ('Chatroom A', 'Chatroom B', 'Chatroom C')

        # Creates the input variable that listens to sent message
        self.message = StringVar()
        self.message.set("Type your message here: ")
        entryMessage = ttk.Entry(mainframe, textvariable=self.message)
        entryMessage.grid(row=3, column=2)

        # Creates the send button which fires the sendMessage function when clicked
        sendButton = ttk.Button(mainframe, text="Send", command=self.sendMessage)
        sendButton.grid(row=3, column=3)

        # Creates a tree view element where the messages sent by users will be stored
        self.messages = ttk.Treeview(mainframe)
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
        # Insert a fake value into the messages
        self.messages.insert('', 'end', values=(self.chatRooms.get(), "Kyle", "Hi there!"))

        # Create a scrollbar to scroll through past messages
        scrollBar = ttk.Scrollbar(mainframe, orient="vertical", command=self.messages.yview)
        scrollBar.grid(column=3, row=0)
