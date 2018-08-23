import sys
import time
import threading
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

from terminal_template import Ui_TerminalMainWindow
from display import Display
from bill_acceptor import BillAcceptor
from strongbox import StrongBox
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
        self.display = Display(self)
        self.bill_acceptor = BillAcceptor(self)
        self.check_printer = CheckPrinter(self)
        self.strongbox = StrongBox(self)
        self.ui.pushButton_settings.setMouseTracking(True)
        self.ui.pushButton_settings.enterEvent = self.settings_button_enter
        self.ui.pushButton_settings.leaveEvent = self.settings_button_leave
        self.ui.pushButton_settings.clicked.connect(self.settings_button_clicked)
        try:
            Terminal.__init__(self, _id)
        except TerminalException:
            self.available = False
        self.display.load_main_screen()

    @property
    def is_available(self):
        try:
            self.check_block()
            if self.available:
                return True
            return False
        except TerminalException:
            return False

    def activate_strongbox(self, cash):
        thread_strongbox = threading.Thread(target=self.strongbox_thread, args=(cash, ), daemon=True)
        thread_strongbox.start()

    def strongbox_thread(self, cash):
        self.strongbox.activate(cash)

    def settings_button_enter(self, event):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))

    def settings_button_leave(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()

    def settings_button_clicked(self):
        self.display.settings_auth_page()
        self.deactivate_bill_acceptor()
        self.deactivate_check_printer()

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

    def restart(self):
        self.close()
        win = QTermWin(self._id, self.app)
        with win:
            win.show()
        self = None

    def shutdown(self):
        self.app.exit(-100)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QTermWin(1049, app)
    with win:
        win.show()
        app.exec_()