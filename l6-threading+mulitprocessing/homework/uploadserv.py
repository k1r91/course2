import os
import struct
import asyncio
import datetime

HOST, PORT = '192.168.10.123', 5555
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'upload')
async def write(file, data):
    file.write(data)

async def handle_request(reader, writer):
    header = await reader.read(struct.calcsize('BBQ'))
    header, length, size = struct.unpack('BBQ', header)
    if header != 0x06:  # Upload file
        return
    upload_name_binary = await reader.read(length)
    upload_name = upload_name_binary.decode('utf-8')
    upload_path = os.path.join(UPLOAD_DIR, upload_name)
    i = 0
    if os.path.exists(upload_path):
        os.remove(upload_path)
    print('Uploading... {} started at {}'.format(upload_name, datetime.datetime.now()))
    while True:
        data = await reader.read(1024)
        if not data:
            break
        with open(upload_path, 'ab') as fup:
            fup.write(data)
        uploaded_size = i * 1024
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
