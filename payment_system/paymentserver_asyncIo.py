import os
import hmac
import asyncio
import struct

from paymentserver import PaymentServerSkeleton
from transaction import Transaction, ServiceTransaction, PaymentTransaction, EncashmentTransaction


class PaymentServerAsync:

    @staticmethod
    async def verify_signature(reader, writer, key):
        message = os.urandom(32)
        writer.write(message)
        await writer.drain()
        hash = hmac.new(key, message)
        digest = hash.hexdigest()
        response = await reader.read(len(digest))
        return hmac.compare_digest(digest.encode(), response)

    @staticmethod
    async def handle(reader, writer):

        parent = PaymentServerSkeleton()
        errors = []

        signed = await PaymentServerAsync.verify_signature(reader, writer, parent.key)

        if not signed:
            errors.append(410)
            writer.write(bytes('410', 'utf-8'))
            writer.close()
            return False

        parent.initialize_bases()
        parent.update_bill()
        pad_len = await reader.read(struct.calcsize('B'))
        pad_len = struct.unpack('B', pad_len)[0]
        cipher = await reader.read(1024)
        data = PaymentServerSkeleton._decrypt(cipher, pad_len)

        tr_type = Transaction.get_type(data)
        tr = None

        # ***** process payment transaction *****

        if tr_type == 1:
            tr = PaymentTransaction.deserialize(data)
            if not parent.check_valid_organization(tr.org_id):  # if organization id not in database
                writer.write(bytes('402', 'utf-8'))
                await writer.drain()
                writer.close()
                return False
            if parent.send_pay(tr.org_id, tr.p_acc, tr.amount, tr.commission):
                writer.write(bytes('200', 'utf-8'))
                await writer.drain()
                writer.close()
            else:
                writer.write(bytes('404', 'utf-8'))
                await writer.drain()
                writer.close()
                errors.append(404)

        # **** process encashment transaction *****

        elif tr_type == 2:
            tr = EncashmentTransaction.deserialize(data)
            if parent.check_collector_requisites(tr.collector_id, tr.secret):
                parent.bill += tr.amount
                writer.write(bytes('200', 'utf-8'))
                await writer.drain()
                writer.close()
            else:
                writer.write(bytes('406', 'utf-8'))
                await writer.drain()
                writer.close()
                errors.append('406')

        # **** process service transaction *****

        elif tr_type == 0:
            tr = ServiceTransaction.deserialize(data)
            if tr.action == 0:  # terminal power on
                # check terminal for registration in our database
                if parent.check_terminal_registration(tr):
                    writer.write(bytes('200', 'utf-8'))
                    await writer.drain()
                    writer.close()
                else:
                    writer.write(bytes('401', 'utf-8'))
                    await writer.drain()
                    writer.close()
                    errors.append('401')
            elif tr.action == 2:  # terminal save config action (shutdown)
                writer.write(bytes('200', 'utf-8'))
                await writer.drain()
                writer.close()
                parent.write_terminal_config(tr)
        # save transaction in database if no errors occurred
        if not errors:
            parent.save_transaction(tr)

        # TODO: log file instead of this
        print('Client says: {}'.format(data))
        print('Deserialized data: {}'.format(tr))

    @staticmethod
    def run():
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(PaymentServerAsync.handle, PaymentServerSkeleton.host,
                                    PaymentServerSkeleton.port, loop=loop)
        server = loop.run_until_complete(coro)
        print('Async server started on {}'.format(server.sockets[0].getsockname()))
        loop.run_forever()
        server.close()
        loop.run_until_complete(server.wait_closed)
        loop.close()

if __name__ == '__main__':
    async_server = PaymentServerAsync()
    async_server.run()