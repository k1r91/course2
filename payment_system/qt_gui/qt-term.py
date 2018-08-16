import sys

from PyQt5 import QtWidgets, QtCore, QtGui

from terminal_template import Ui_TerminalMainWindow


class QTermWin(QtWidgets.QMainWindow):
    def __init__(self, _id, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_TerminalMainWindow()
        self.ui.setupUi(self)
        self.id = _id
        self.setWindowTitle('Terminal № {}'.format(self.id))

    def not_impemented(self):
        print('Not implemented yet')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = QTermWin(1049)
    win.show()
    sys.exit(app.exec_())

