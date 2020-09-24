import socket
from threading import Thread


class Main:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Would you like to login or create an account')
        choose = input(':')
        if choose.lower() == 'login':
            print('You are logging in')
            self.alteraid = input('ALTERA ID: ')
            self.connect()
        elif choose.lower() == 'create':
            print('hello')
            h = input('enter id\n:')
        else:
            print(f'Unknown option: {choose}')


# listen for connections
    def connect(self):
        try:
            self.sock.connect(('altera-server.ddns.net', 2288))
            print('Connecting to server on altera-server.ddns.net')
        except:
            try:
                self.sock.connect(('localhost', 2288))
                print('Connecting to server on local machine')
            except:
                pass

        finally:
            try:
                self.sock.send(self.alteraid.encode('utf-8'))
                print('You have connected to the server')
                self.send()
            except:
                print('No server is currently online')


# send
    def send(self):
        while True:
            h = input('command: ')
            self.sock.send(h.encode('utf-8'))


if __name__ == '__main__':
    Main()
