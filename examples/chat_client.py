import asyncio
import aconsole
import json


loop = asyncio.get_event_loop()
console = aconsole.AsyncConsole()


class ChatClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.cwait = asyncio.Future()
        self.writer = None
        self.reader = None
        self.username = None

        loop.create_task(self.connector())

    async def wait_close(self):
        await self.cwait

    async def handle_connection(self):
        buffer = bytearray()

        try:
            while True:
                buf = await self.reader.read(1024)
                if not buf:
                    raise ConnectionAbortedError()

                buffer.extend(buf)
                while True:
                    index = buffer.find(b'\x00')
                    if index == -1:
                        break #Packet not complete yet

                    packet = buffer[:index]
                    packet_json = json.loads(packet)

                    if packet_json['cmd'] == 'message':
                        console.print(f'[{packet_json["sender"]}]: {packet_json["message"]}')

                    del buffer[:index+1] #remove length + \x00
        except Exception as ex:
            console.print(f'ERROR: {ex}')
        finally:
            self.writer.close()

    async def connector(self):
        try:
            self.username = await console.input("Enter your username:")
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

            login_packet = {'cmd': 'username', 'username': self.username}
            login_packet_bytes = json.dumps(login_packet).encode()

            self.writer.write(login_packet_bytes)
            self.writer.write(b'\x00')

            loop.create_task(self.send_input())
            loop.create_task(self.handle_connection())

            await self.writer.wait_closed()
            console.cancel_input()
            raise ConnectionAbortedError()
        except Exception as ex:
            self.cwait.set_exception(ex)

    async def send_input(self):
        while True:
            message = await console.input('Send: ')

            if message:
                message_json = {'cmd': 'message', 'sender': self.username, 'message': message}
                message_json_bytes = json.dumps(message_json).encode()

                self.writer.write(message_json_bytes)
                self.writer.write(b'\x00')

if __name__ == '__main__':
    run_task = console.run()
    ChatClient('127.0.0.1', 8888)
    loop.run_until_complete(run_task)
