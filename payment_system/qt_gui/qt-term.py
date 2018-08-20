import sys
import threading
from PyQt5 import QtWidgets, QtCore, QtGui

# my modules
import sql
from terminal_template import Ui_TerminalMainWindow
from display import Display
from bill_acceptor import BillAcceptor

sys.path.append('..')
from terminal import Terminal, TerminalException


class QTermWin(Terminal, QtWidgets.QMainWindow):
    def __init__(self, _id, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_TerminalMainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Terminal № {}'.format(_id))
        self.available = True
        self.bill_acceptor = BillAcceptor(self)
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

    @staticmethod
    def not_impemented(self):
        print('Not implemented yet')

    def activate_bill_acceptor(self):
        bill_acceptor_thread = threading.Thread(target=self.run_bill_acceptor, daemon=True)
        bill_acceptor_thread.start()

    def run_bill_acceptor(self):
        self.bill_acceptor.activate()

    def deactivate_bill_acceptor(self):
        self.bill_acceptor.deactivate()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QTermWin(1049)
    with win:
        win.show()
        sys.exit(app.exec_())

