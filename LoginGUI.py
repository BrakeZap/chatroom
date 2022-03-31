from tkinter import *
from tkinter import ttk

class LoginGUI:
    def __init__(self):
        root = Tk()
        root.title("Login Screen")
        container = Frame(root)
        container.pack()
        frame = LoginFrame(container)
        frame.grid(row=0, column=0, sticky=(N, W, E, S))
        frames = {}
        frames["default"] = frame
        frame2 = CreateAccountFrame(container)
        frames["createAccount"] = frame2
        frame.setFrames(frames)
        frame2.setFrames(frames)
        root.mainloop()

class LoginFrame(ttk.Frame):

    def changeFrame(self):
        frame = self.frames["createAccount"]
        frame.grid(row=0, column=0)
        frame.tkraise()

    def setFrames(self,frames):
        self.frames = frames

    def __init__(self, parent):
        ttk.Frame.__init__(self,parent, padding="3 3 12 12")
        self.frames = {}
        usernameLabel = ttk.Label(self, text="Username:")
        usernameLabel.grid(row=0, column=0, sticky="W")
        username = StringVar()
        usernameEntry = ttk.Entry(self, textvariable=username)
        usernameEntry.grid(row=0, column=1)

        passwordLabel = ttk.Label(self, text="Password:")
        passwordLabel.grid(row=1, column=0, sticky="W")
        password = StringVar()
        passwordEntry = ttk.Entry(self, textvariable=password)
        passwordEntry.grid(row=1, column=1)

        createAccountButton = ttk.Button(self, text="Create an account", command=lambda: self.changeFrame())
        createAccountButton.grid(row=2, column=0, stick="W")


class CreateAccountFrame(ttk.Frame):

    def createAccount(self, entry1, entry2):
        if (self.password.get() != self.confirmPassword.get()):
            entry1.delete(0, END)
            entry2.delete(0, END)
            self.nonMatchingPassLabel = Label(self, text="Passwords do not match!")
            self.nonMatchingPassLabel.config(fg="red")
            self.nonMatchingPassLabel.grid(row=4, column=0)
        else:
            #self.nonMatchingPassLabel.forget()
            frame = self.frames["default"]
            frame.grid(row=0, column=0)
            frame.tkraise()

    def setFrames(self,frames):
        self.frames = frames

    def __init__(self,parent):
        ttk.Frame.__init__(self,parent, padding="3 3 12 12")
        self.frames = {}
        usernameLabel = ttk.Label(self, text="Username:")
        usernameLabel.grid(row=0, column=0,sticky="W")
        username = StringVar()
        usernameEntry = ttk.Entry(self, textvariable=username)
        usernameEntry.grid(row=0, column=1)

        passwordLabel = ttk.Label(self, text="Password:")
        passwordLabel.grid(row=1, column=0,sticky="W")
        self.password = StringVar()
        passwordEntry = ttk.Entry(self, textvariable=self.password)
        passwordEntry.grid(row=1, column=1)

        confirmPasswordLabel = ttk.Label(self, text="Confirm Password:")
        confirmPasswordLabel.grid(row=2, column=0,sticky="W")
        self.confirmPassword = StringVar()
        confirmPasswordEntry = ttk.Entry(self, textvariable=self.confirmPassword)
        confirmPasswordEntry.grid(row=2, column=1)

        createAccountButton = ttk.Button(self, text="Click to Create An Account!", command=lambda: self.createAccount(passwordEntry, confirmPasswordEntry))
        createAccountButton.grid(row=3, column=0)       




LoginGUI()