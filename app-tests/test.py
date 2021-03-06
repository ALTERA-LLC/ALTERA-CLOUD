from tkinter import *
import socket
import threading
import os
from time import sleep


class Main:
    def __init__(self):
        self.root = Tk()
        self.sock = Socket(self.root)
        self.root.resizable(0, 0)
        self.root.geometry('600x400')
        threading.Thread(target=self.sock.start).start()
        threading.Thread(target=self.sockcheck).start()

    def sockcheck(self):
        while not self.sock.loggedin:
            pass

        print('Completed')



class Socket:
    def __init__(self, root):
        self.loggedin = False
        self.root = root
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.entry = Entry(root)
        self.text = Label(root)
        self.createw = Button(text='Create', command=self.create)
        self.loginw = Button(text='Login', command=self.login)

    def start(self):
        print('start')
        self.loginw.pack()
        self.createw.pack()

    def remove(self):
        self.createw.place(x=1000, y=1000)
        self.loginw.place(x=1000, y=1000)
        self.text.place(x=1000, y=1000)
        self.entry.place(x=1000, y=1000)

    def create(self):
        print('creating')
        self.remove()
        self.text.config(text='Create ID')
        self.text.pack()
        self.entry.pack()

        def run(event):
            self.remove()
            threading.Thread(target=create).start()

        def create():
            self.text.config(text='Connecting')
            self.text.pack()
            if self.connect():
                self.remove()
                self.sock.send('create'.encode('utf-8'))
                sleep(0.1)
                self.sock.send(self.entry.get().encode('utf-8'))
                self.text.config(text=self.sock.recv(1024).decode('utf-8'))
                self.text.pack()
                sleep(1)
                self.remove()
                self.text.config(text=self.sock.recv(1024).decode('utf-8'))
                self.text.pack()
                sleep(1)
                self.remove()
                self.loggedin = True
            else:
                self.remove()
                self.text.config(text='Server not online\nplease try again later')
                self.text.pack()

        self.root.bind('<Return>', run)

    def login(self):
        print('logging in')

        def run(event):
            self.remove()
            threading.Thread(target=login).start()

        def init():
            self.remove()
            self.text.config(text='Enter your ALTERA-ID')
            self.text.pack()
            self.entry.pack()

        def login():
            self.text.config(text='Connecting')
            self.text.pack()
            if self.connect():
                self.remove()
                self.sock.send('login'.encode('utf-8'))
                sleep(0.1)
                def run(event):
                    threading.Thread(target=restart).start()

                def restart():
                    self.remove()
                    self.sock.send(self.entry.get().encode('utf-8'))
                    rep = self.sock.recv(1024).decode('utf-8')
                    if not 'User' in rep:
                        self.text.config(text=rep)
                        self.text.pack()
                        sleep(1)
                        self.remove()
                        self.loggedin = True
                    else:
                        print(rep)
                        print('failed to login')
                        self.text.config(text=rep)
                        self.text.pack()
                        sleep(2)
                        init()
                        self.root.bind('<Return>', run)

                restart()

            else:
                self.remove()
                self.text.config(text='Server not online\nplease try again later')
                self.text.pack()

        init()
        self.root.bind('<Return>', run)

    def connect(self):
        try:
            self.sock.send('t'.encode())
            return True
        except:
            try:
                # try to connect to main server
                self.sock.connect(('altera-server.ddns.net', 2288))
                print('Connecting to server on altera-server.ddns.net')
                print('Connected to global server')
                return True
            except:
                try:
                    self.sock.connect(('localhost', 2288))
                    print('Connecting to server on local machine')
                    print('Connected to local machine')
                    return True
                except:
                    print('There is no local or global servers on')
                    return False



if __name__ == '__main__':
    main = Main()
    main.root.mainloop()
