import asyncio
import aconsole
import json


loop = asyncio.get_event_loop()
console = aconsole.AsyncConsole()


class ChatServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.forever = asyncio.Future()
        self.clients = []

        loop.create_task(self.accepter())
        loop.create_task(self.broadcast_input())

    async def serve_forever(self):
        await self.forever

    def on_client(self, reader, writer):
        async def run_client(reader, writer):
            username = "unknown"
            buffer = bytearray()

            try:
                while True:
                    buf = await reader.read(1024)
                    if not buf:
                        raise ConnectionAbortedError('Connection lost')

                    buffer.extend(buf)
                    while True:
                        index = buffer.find(b'\x00')
                        if index == -1:
                            break #Packet not complete yet

                        packet = buffer[:index]
                        packet_json = json.loads(packet)

                        #console.print(packet_json)

                        if packet_json['cmd'] == 'message':
                            message_json = {'cmd': 'message', 'sender': username, 'message': packet_json['message']}
                            message_json_bytes = json.dumps(message_json).encode()

                            for client in self.clients:
                                client.write(message_json_bytes)
                                client.write(b'\x00')

                        elif packet_json['cmd'] == 'username':
                            if packet_json['username'] == 'SERVER':
                                raise Exception('INVALID USERNAME')
                                
                            username = packet_json['username']

                        del buffer[:index+1] #remove length + \x00
            except Exception as ex:
                console.print(f'{username} has left the server. {ex}')

                message_json = {'cmd': 'message', 'sender': 'SERVER', 'message': f'{username} has left the server. {ex}'}
                message_json_bytes = json.dumps(message_json).encode()
                for client in self.clients:
                    client.write(message_json_bytes)
                    client.write(b'\x00')
            finally:
                self.clients.remove(writer)
                writer.close()

        self.clients.append(writer)
        loop.create_task(run_client(reader, writer))

    async def accepter(self):
        try:
            server = await asyncio.start_server(self.on_client, self.host, self.port)
            async with server:
                await server.serve_forever()
        except Exception as ex:
            self.forever.set_exception(ex)

    async def broadcast_input(self):
        while True:
            message = await console.input('Broadcast: ')
            message_json = {'cmd': 'message', 'sender': 'SERVER', 'message': message}
            message_json_bytes = json.dumps(message_json).encode()
            message_sent_count = 0

            for client in self.clients:
                client.write(message_json_bytes)
                client.write(b'\x00')
                message_sent_count += 1

            console.print('Sent', message_sent_count, 'messages.')

if __name__ == '__main__':
    run_task = console.run()

    server = ChatServer('0.0.0.0', 8888)
    loop.create_task(server.serve_forever())

    loop.run_until_complete(run_task)
