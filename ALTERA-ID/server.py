import socket
import threading


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
            print(f'Main-Thread: {a[0]} has connected')
            client_id = s.recv(1024).decode('utf-8')
            self.clients.append(s)
            self.client_ids.append(client_id)
            index = len(self.clients) - 1
            threading.Thread(target=lambda: self.client_thread(index)).start()

    # start client thread
    def client_thread(self, index):
        print(f'Main-Thread: Number of started client threads {index + 1}')
        # get client info
        client = self.clients[index]
        client_id = self.client_ids[index]
        print(f'Client Thread({index + 1}): Started thread')
        # loop
        running = True
        while running:
            try:
                msg = client.recv(1024).decode('utf-8')
                print(msg)
            except:
                self.clients.remove(client)
                self.client_ids.remove(client_id)
                running = False
                print(f'Client thread: {client_id} (Index: {index + 1}) has stopped')


if __name__ == '__main__':
    Main()
