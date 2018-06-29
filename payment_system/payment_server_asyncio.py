import asyncio

from paymentserver import PaymentServerSkeleton
from transaction import Transaction, ServiceTransaction, PaymentTransaction, EncashmentTransaction

class PaymentServerAsync():

    @staticmethod
    async def handle(reader, writer):
        parent = PaymentServerSkeleton()
        parent.initialize_bases()
        bill = parent.update_bill()
        data = await reader.read(1024)

        tr_type = Transaction.get_type(data)
        tr = None
        errors = []

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
            if parent.check_collector_requisites(tr.collector_id):
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
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        server.close()
        loop.run_until_complete(server.wait_closed)
        loop.close()

if __name__ == '__main__':
    async_server = PaymentServerAsync()
    async_server.run()