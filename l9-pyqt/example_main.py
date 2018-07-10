import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from example_form import Ui_MainWindow


class MainWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushExit.clicked.connect(self.exit)
        self.ui.pushTable.clicked.connect(lambda: self.fill_rows(40))

    def exit(self, x):
        print(self.ui.tableWidget.itemAt(13, 0).text())
        # sys.exit(1)

    def fill_rows(self, n):
        self.ui.tableWidget.setRowCount(n)
        for i in range(n+1):
            new_item = QtWidgets.QTableWidgetItem('Terminal {}'.format(i+1))
            self.ui.tableWidget.setItem(i, 0, new_item)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_win = MainWin()
    main_win.show()
    sys.exit(app.exec_())
