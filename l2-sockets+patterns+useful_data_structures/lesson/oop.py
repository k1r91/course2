class BusinessLogic:

    def make_transaction(self):
        print('Business logic transaction')


class BaseProtocol:
    pass

    def make_connection(self):
        print('Base TCP connection')


class MagicProtocol:

    def make_connection(self):
        print('Magic connection (courier)')


class FtpProtocol(BaseProtocol):
    # def make_connection(self):
    #     print('FTP connection')
    pass


class HttpProtocol(BaseProtocol):
    pass
    # def make_connection(self):
    #     print('HTTP connection')


class HttpsProtocol(HttpProtocol):
    # def make_connection(self):
    #     print('HTTPS connection')
    pass


class SftpProtocol(FtpProtocol):
    pass
    # def make_connection(self):
    #     print('SFTP connection')


class BusinessExchange(BusinessLogic, HttpsProtocol, SftpProtocol, MagicProtocol):
    pass

    # def make_connection(self):
    #     print('Business exchange connection')

be = BusinessExchange()
be.make_connection()
be.make_transaction()

# print method resolution order (mro)
print(BusinessExchange.__mro__)


class XConnection(BaseProtocol):
    def make_connection(self):
        print('x-connection')


class YConnection(BaseProtocol):
    def make_connection(self):
        print('y-connection')


class Zconnection(XConnection, YConnection):
    def make_connection(self):
        print('z-connection')


class QConnection(YConnection, XConnection):
    def make_connection(self):
        print('q-connection')

print(QConnection.__mro__)


class MixedConnection(Zconnection, QConnection):
    def make_connection(self):
        print('mixed connection')