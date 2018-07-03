import os
import asyncio

HOST, PORT = 'localhost', 5555
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'upload')
test_fname = os.path.join(UPLOAD_DIR, 'test.jpeg')
async def write(file, data):
    file.write(data)

async def handle_request(reader, writer):
    i = 0
    while True:
        data = await reader.read(1024)
        if not data:
            break
        with open(test_fname, 'ab') as fup:
            fup.write(data)
        writer.write('{}'.format(i).encode())
        i += 1
        await writer.drain()
    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_request, HOST, PORT, loop=loop)
server = loop.run_until_complete(coro)
print('Server started on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
