import socket
import threading
import tools.json.data as data

ud = data.UserData()


class Main:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.send_voice()

    def connect(self):
        try:
            # try to connect to main server
            self.sock.connect(('altera-server.ddns.net', 2288))
            print('Connecting to server on altera-server.ddns.net')
            print('Connected to global server')
        except:
            try:
                self.sock.connect(('localhost', 2288))
                print('Connecting to server on local machine')
                print('Connected to local machine')
            except:
                print('There is no local or global servers on')

    def send_voice(self):
        print('Voice')
