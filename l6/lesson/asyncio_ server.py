import asyncio

# Python <= 3.4


@asyncio.coroutine
def my_coro():
    yield from func()   # yield from generator


# Python >= 3.5
async def my_coro():
    await func()

print(type(my_coro))

async def handle_echo(reader, writer):
    data = await reader.read(1024)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print('Received {} from {}'.format(message, addr))
    print('Send: {}'.format(message))
    writer.write(b'200')
    await writer.drain()
    print('Closing client socket')
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, 'localhost', 8888, loop=loop)
server = loop.run_until_complete(coro)

print('Server started on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()