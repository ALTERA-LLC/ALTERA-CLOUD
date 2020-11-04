from tkinter import *
from tkinter.ttk import Progressbar
from threading import Thread
from PIL import Image, ImageTk
import socket
import time


class load:
    def __init__(self):
        self.root = Tk()
        self.root.resizable(0, 0)
        self.root.overrideredirect(1)
        # set center screen window with following coordination
        self.root.geometry("%dx%d+%d+%d" % (
            550, 300, (self.root.winfo_screenwidth() - 500) / 2, (self.root.winfo_screenheight() - 300) / 2))
        image = ImageTk.PhotoImage(Image.open('assets/images/l_bg1.png'))
        hh = Label(self.root, image=image)
        hh.place(x=0, y=0, relwidth=1, relheight=1)
        Thread(target=lambda: self.setup()).start()
        self.root.mainloop()

    def setup(self):
        progress = Progressbar(self.root, orient=HORIZONTAL, length=250, mode='determinate')
        progress.place(x=50, y=235)

        def progressset(num):
            progress['value'] = num

        def setup_app():
            def run():
                Thread(target=Main_app).start()
            # progress stuff
            print('good stuff')
            # start app
            Thread(target=run).start()
            self.root.quit()
        setup_app()


class Main_app:
    def __init__(self):
        self.root = Tk()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root.resizable(0, 0)
        self.root.title('ALTERA CHAT')
        self.root.geometry('800x600')
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        Thread(target=lambda: self.build()).start()
        self.root.mainloop()

    def exit(self):
        sys.exit()

    def join(self):
        self.label.pack()
        if self.connect():
            e = Entry(width=10, font='consolas 19 bold')
            e.pack()
            self.root.bind('<Return>', lambda: self.sock.send(str(e).encode('utf-8')))
        else:
            self.label.place(x=1000, y=1000)
            self.label.config(text='Couldnt connect to server\nPlease try again later')
            self.label.pack()
            self.root.destroy()

            



    def connect(self):
        try:
            self.sock.connect(('altera-server.ddns.net', 2288))
            return True
        except:
            try:
                self.sock.connect(('localhost', 2288))
                return True
            except:
                print('No servers are available')
                return False

    def create_widgets(self):
        self.label = Label(self.root, text='Connecting', font='consolas 19 bold')

    def build(self):
        self.create_widgets()
        self.join()



m = Main_app()
