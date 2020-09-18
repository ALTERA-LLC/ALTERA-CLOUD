import socket
from threading import Thread


class Main:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.client_ids = []
        try:
            self.sock.bind(('192.168.0.69', 2288))
            print('Running server on altera-server.ddns.net')
        except:
            self.sock.bind(('localhost', 2288))
            print('Running server on local machine')
        finally:
            print('Starting server')
            self.handle()

# listen for connections
    def handle(self):
        self.sock.listen(1)
        print('Listening for connections')
        while True:
            s, a = self.sock.accept()
            client_id = s.recv(1024).decode('utf-8')
            self.clients.append(s)
            self.client_ids.append(client_id)
            index = str(len(self.clients) - 1)
            print(self.clients)
            print(self.client_ids)
            Thread(target=lambda: self.client_thread(index))

# start client thread
    def client_thread(self, index):
        client = self.clients[index]
        client_id = self.client_ids[index]
        print(f'{client_id}: Started clients thread {index}')
        running = True
        while running:
            msg = client.recv(1024).decode('utf-8')
            print(msg)

if __name__ == '__main__':
    Main()
