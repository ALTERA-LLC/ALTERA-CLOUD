import socket
import threading
import tools.json.data as data

ud = data.UserData()


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

    def login(self):
        client_id = self.s.recv(1024).decode('utf-8')
        if ud.is_user(client_id):
            self.clients.append(self.s)
            self.client_ids.append(client_id)
            index = len(self.clients) - 1
            print('user logged in')
            threading.Thread(target=lambda: self.client_thread(index)).start()
            self.s.send(f'logged in to {client_id}'.encode('utf-8'))
        else:
            self.s.send(f'User {client_id} doesnt exist'.encode('utf'))
            print('user doesnt exist')

    def create(self):
        print('Creating id')
        crid = self.s.recv(1024).decode('utf-8')
        print(crid)
        self.s.send(ud.create_id(crid).encode('utf-8'))
        self.clients.append(self.s)
        self.client_ids.append(crid)
        index = len(self.clients) - 1
        print('user logged in')
        threading.Thread(target=lambda: self.client_thread(index)).start()
        self.s.send(f'logged in to {crid}'.encode('utf-8'))

    # listen for connections
    def handle(self):
        self.sock.listen(1)
        print('Listening for connections')
        while True:
            self.s, a = self.sock.accept()
            print(f'Main-Thread: {a[0]} has connected')
            choice = self.s.recv(1024).decode('utf-8')
            if choice == 'login':
                threading.Thread(target=self.login).start()
            elif choice == 'create':
                threading.Thread(target=self.create).start()
            else:
                print('Error')

    def disconnect(self, client, client_id, index):
        self.clients.remove(client)
        self.client_ids.remove(client_id)
        running = False
        print(f'Client thread({index + 1}): has stopped')

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
                if client.recv(1024).decode('utf-8') == '':
                    self.disconnect(client, client_id, index)
            except:
                self.disconnect(client, client_id, index)


if __name__ == '__main__':
    Main()
