"""
Names: Zack Dowling & Matthew Norloff
File: phonebookclient.py
Module 6 Phonebook Assignment
Client for a phone book application.
ADDS name and number to AddressBook.txt.
FINDS name and number in AddressBook.txt.
Updates table as new numbers are added.
"""

import socket
from codecs import decode
from breezypythongui import EasyFrame
import re
import os

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 8888
BUFSIZE = 1024
ADDRESS = (HOST, PORT)
CODE = "ascii"


class PhonebookClient(EasyFrame):
    """GUI for the client app."""

    def __init__(self):
        """Initialize the frame and widgets."""
        EasyFrame.__init__(self, title="Phone Book")
        # Add the labels, fields, and button
        self.statusLabel = self.addLabel(text="Do you want to connect to the Phonebook?",
                                         row=0,
                                         column=0,
                                         columnspan=3)

        self.find = self.addButton(row=1,
                                      column=0,
                                      text="Find",
                                      command=self.find,
                                      state="disabled")

        self.addTo = self.addButton(row=1,
                                     column=1,
                                     text="Add",
                                     command=self.add,
                                     state="disabled")

        self.connect = self.addButton(row=11,
                                      column=1,
                                      text="Connect",
                                      command=self.connect,
                                      state="active")

        self.disconnect = self.addButton(row=11,
                                      column=2,
                                      text="Disconnect",
                                      command=self.disconnect,
                                      state="disabled")

        self.update = self.addButton(row=1,
                                     column=2,
                                     text="Update",
                                     command=self.update,
                                     state="disabled")

        self.Results = self.addTextArea("",row=2,
                                        column=0,
                                        rowspan=8,
                                        columnspan=4)

    def find(self):
        """Looks up a name in the phone book."""
        name = self.prompterBox(promptString="Enter the name (EX: ZDowling).")
        if name == "": return
        self.server.send(bytes("FIND " + name, CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        if not reply:
            self.messageBox(message="Server disconnected")
            self.disconnect()
        else:
            self.statusLabel["text"] = reply

    def add(self):
        """Adds a name and number to the phone book."""
        name = self.prompterBox(promptString="Enter first initial followed by last name (EX: ZDowling).")
        if name == "": return
        number = self.prompterBox(promptString="Enter the phone number.")
        if number == "": return
        self.server.send(bytes("ADD " + name + " " + number, CODE))
        reply = decode(self.server.recv(BUFSIZE), CODE)
        if not reply:
            self.messageBox(message="Server disconnected")
            self.disconnect()
        else:
            self.statusLabel["text"] = reply

    def update(self):
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(ADDRESS)
        start_book = self.server.recv(BUFSIZE).decode()
        self.Results.setText(start_book)
        self.statusLabel["text"] = "Welcome back to your updated phonebook!"

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(ADDRESS)
        start_book = self.server.recv(BUFSIZE).decode()
        self.Results.setText(start_book)
        self.statusLabel["text"] = decode(self.server.recv(BUFSIZE), CODE)
        self.find["state"] = "active"
        self.addTo["state"] = "active"
        self.update["state"] = "active"
        self.disconnect["state"] = "active"
        self.connect["state"] = "disabled"

    def disconnect(self):
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        self.statusLabel["text"] = "Want to connect?"
        self.connect["state"] = "active"
        self.disconnect["state"] = "disabled"
        self.update["state"] = "disabled"
        self.find["state"] = "disabled"
        self.addTo["state"] = "disabled"
        self.Results.setText("")


def main():
    """Instantiate and pop up the window."""
    PhonebookClient().mainloop()


if __name__ == "__main__":
    main()