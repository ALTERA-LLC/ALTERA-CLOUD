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

    def login(self, client):
        client_id = client.recv(1024).decode('utf-8')
        if ud.is_user(client_id):
            self.connect(client, client_id)
            client.send(f'logged in to {client_id}'.encode('utf-8'))
        else:
            self.s.send(f'User {client_id} doesnt exist'.encode('utf'))
            print('user doesnt exist')
            self.login(client)

    def create(self, client):
        print('Creating id')
        crid = client.recv(1024).decode('utf-8')
        response, outcome = ud.create_id(crid)
        if outcome:
            client.send(response.encode('utf-8'))
            self.connect(client, crid)
            client.send(f'logged in to {crid}'.encode('utf-8'))
        else:
            client.send(response.encode('utf-8'))
            client.send(f'Try again'.encode('utf-8'))
            self.create(client)


    # listen for connections
    def handle(self):
        self.sock.listen(1)
        print('Listening for connections')
        while True:
            self.s, a = self.sock.accept()
            print(f'Main-Thread: {a[0]} has connected')
            choice = self.s.recv(1024).decode('utf-8')
            if choice == 'login':
                threading.Thread(target=lambda: self.login(self.s)).start()
            elif choice == 'create':
                threading.Thread(target=lambda: self.create(self.s)).start()
            else:
                print('Error')

    def connect(self, client, client_id):
        self.clients.append(client)
        self.client_ids.append(client_id)
        index = len(self.clients) - 1
        print('user logged in')
        threading.Thread(target=lambda: self.client_thread(index)).start()

    def disconnect(self, client, client_id):
        self.clients.remove(client)
        self.client_ids.remove(client_id)

    # start client thread
    def client_thread(self, index):
        print(f'Main-Thread: Number of started client threads {index + 1}')
        # get client info
        client = self.clients[index]
        client_id = self.client_ids[index]
        print(f'Client Thread({index + 1}): Started thread')
        # loop
        global running
        running = True
        while running:
            try:
                h = client.recv(1024).decode('utf-8')
                if h == '':
                    self.disconnect(client, client_id)
                    running = False
                    print(f'Client thread({index + 1}): has stopped')
                print(h)
            except:
                self.disconnect(client, client_id)
                running = False
                print(f'Client thread({index + 1}): has stopped')

if __name__ == '__main__':
    Main()
