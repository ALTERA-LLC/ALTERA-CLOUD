import socket
from threading import Thread
from time import sleep

class Main:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Would you like to login or create an account')
        choose = input(':')
        if choose.lower() == 'login':
            print('You are logging in')
            self.alteraid = input('ALTERA ID: ')
            self.login()
        elif choose.lower() == 'create':
            print('create id')
            self.h = input('enter the id you want\n:')
            self.create()
        else:
            print(f'Unknown option: {choose}')

    def login(self):
        if self.connect():
            def retart():
                self.sock.send('login'.encode('utf-8'))
                sleep(0.1)
                self.sock.send(self.alteraid.encode('utf-8'))
                rep = self.sock.recv(1024).decode('utf-8')
                if 'User' in rep:
                    print(rep)
                    print('failed to login')
                    retart()
                else:
                    print(rep)
                    self.send()
            retart()

    def create(self):
        print('hi')
        if self.connect():
            self.sock.send('create'.encode('utf-8'))
            sleep(0.1)
            self.sock.send(self.h.encode('utf-8'))
            print(self.sock.recv(1024).decode('utf-8'))
            self.send()





# listen for connections
    def connect(self):
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




# send
    def send(self):
        while True:
            h = input('command: ')
            self.sock.send(h.encode('utf-8'))


if __name__ == '__main__':
    Main()
