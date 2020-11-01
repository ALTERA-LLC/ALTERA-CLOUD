import socket
import asyncio
from time import sleep
from threading import Thread


class Main:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.task = None
        self.clients = []

    async def handle(self):
        try:
            self.sock.bind(('192.168.0.69', 2288))
        except:
            self.sock.bind(('localhost', 2288))
        self.sock.listen(1)
        print('Main-thread: Listening for connections')
        while True:
            self.s, a = self.sock.accept()
            print(f'Main-thread: {a[0]} has connected')
            self.username = self.s.recv(1024).decode('utf-8')
            await self.connect()

    async def connect(self):
        self.clients.append({'name':self.username, 'client':self.s})
        self.index = len(self.clients) - 1
        if self.task in asyncio.all_tasks():
            await asyncio.wait_for(self.task, 100)
        self.task = asyncio.create_task(self.broadcast(self.username + " has joined the chat"))
        await self.task
        # start new client thread
        Thread(target=lambda:asyncio.run(self.client_thread())).start()

    async def disconnect(self, client):
        self.clients.remove(client)
        if self.task in asyncio.all_tasks():
            await asyncio.wait_for(self.task, 100)
        self.task = asyncio.create_task(self.broadcast(self.username + " has left the chat"))
        await self.task

    async def broadcast(self, msg):
        if not len(self.clients):
            print('Main-thread: No one is in the chat')
            return
        for client in self.clients:
            client['client'].send(msg.encode('utf-8'))

    async def client_thread(self, running=True):
        client = self.s
        username = self.username
        index = self.clients[self.index]
        print(f'{username}-thread: Started Thread')
        while running:
            try:
                msg = client.recv(1024).decode('utf-8')
                if self.task in asyncio.all_tasks():
                    await asyncio.wait_for(self.task, 100)
                self.task = asyncio.create_task(self.broadcast(f'{username}: {msg}'))
                await self.task


            except:
                print(f'{username}-thread: Disconnected')
                print(f'{username}-thread: Removing from client list')
                await self.disconnect(index)
                running = False
        print(f'{username}-thread: Thread has stopped')


if __name__ == '__main__':
    server = Main()
    asyncio.run(server.handle())
