import os
import struct
import asyncio
import datetime

HOST, PORT = 'localhost', 5555
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'upload')
test_fname = os.path.join(UPLOAD_DIR, 'test.jpeg')
async def write(file, data):
    file.write(data)

async def handle_request(reader, writer):
    header = await reader.read(struct.calcsize('BBQQ'))
    header, length, read_sz, size = struct.unpack('BBQQ', header)
    if header == 0x06:  # Upload file
        upload_name_binary = await reader.read(length)
        upload_name = upload_name_binary.decode('utf-8')
        upload_path = os.path.join(UPLOAD_DIR, upload_name)
    i = 0
    if os.path.exists(upload_path):
        os.remove(upload_path)
    print('Uploading... {} started at {}'.format(upload_name, datetime.datetime.now()))
    while True:
        data = await reader.read(read_sz)
        if not data:
            break
        with open(upload_path, 'ab') as fup:
            fup.write(data)
        uploaded_size = i * read_sz
        upload_percentage = struct.pack('f', uploaded_size / size * 100)
        writer.write(upload_percentage)
        await writer.drain()
        i += 1
    writer.close()
    print('Upload of {} complete at {}'.format(upload_name, datetime.datetime.now()))


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_request, HOST, PORT, loop=loop)
server = loop.run_until_complete(coro)
print('Server started on {}'.format(server.sockets[0].getsockname()))
loop.run_forever()
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
