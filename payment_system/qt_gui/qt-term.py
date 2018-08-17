import sys
import multiprocessing as mp
from PyQt5 import QtWidgets, QtCore, QtGui

# my modules
import sql
from terminal_template import Ui_TerminalMainWindow
from display import Display

sys.path.append('..')
from terminal import Terminal, TerminalException


class QTermWin(Terminal, QtWidgets.QMainWindow):
    def __init__(self, _id, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_TerminalMainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Terminal № {}'.format(_id))
        self.available = True
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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QTermWin(1049)
    with win:
        win.show()
        sys.exit(app.exec_())

