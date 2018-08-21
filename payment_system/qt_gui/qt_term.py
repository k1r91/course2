import sys
import time
import threading
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

from terminal_template import Ui_TerminalMainWindow
from display import Display
from bill_acceptor import BillAcceptor
from check_printer import CheckPrinter

sys.path.append('..')
from terminal import Terminal, TerminalException


class QTermWin(Terminal, QtWidgets.QMainWindow):
    def __init__(self, _id, app, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.app = app
        self.ui = Ui_TerminalMainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Terminal № {}'.format(_id))
        self.available = True
        self.bill_acceptor = BillAcceptor(self)
        self.check_printer = CheckPrinter(self)
        try:
            Terminal.__init__(self, _id)
        except TerminalException:
            self.available = False
        self.load_display()

    def load_display(self):
        self.display = Display(self)
        if self.available:
            self.display.load_main_screen()
        else:
            self.display.load_error_screen()

    def activate_bill_acceptor(self):
        bill_acceptor_thread = threading.Thread(target=self.bill_acceptor_thread, daemon=True)
        bill_acceptor_thread.start()

    def bill_acceptor_thread(self):
        self.bill_acceptor.activate()

    def deactivate_bill_acceptor(self):
        self.bill_acceptor.deactivate()

    def activate_check_printer(self, data):
        data.update({'last_transaction_id': self.last_transaction_id, 'terminal_id': self._id})
        check_printer_thread = threading.Thread(target=self.check_printer_thread, args=(data, ),
                                                daemon=True)
        check_printer_thread.start()

    def deactivate_check_printer(self):
        self.check_printer.deactivate()

    def check_printer_thread(self, data):
        self.check_printer.activate(data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QTermWin(1049, app)
    with win:
        win.show()
        sys.exit(app.exec_())



