import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from admin_template import Ui_AdminWindow


class MainWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_AdminWindow()

        self.ui.setupUi(self)
        self.ui.actionExit.triggered.connect(self.exit)
        self.setGeometry(QtCore.QRect(250, 150, self.geometry().width(), self.geometry().height()))

    def exit(self):
        sys.exit(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())