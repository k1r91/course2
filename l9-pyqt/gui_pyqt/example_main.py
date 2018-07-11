
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from example_form import *


class MainWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.ui.pushOk.clicked.connect(lambda: self.test(555))
        self.ui.pushTable.clicked.connect(lambda: self.fill_rows(40))

    def test(self, x):
        print('Hello, что ли?!', self.ui.pushOk.text())  
        item = self.ui.tableWidget.itemAt(13, 0)
        print(item.text())
        print(self.ui.dateEdit.date().toString("d.M.yyyy"))

    def fill_rows(self, n):
        self.ui.tableWidget.setRowCount(n) 
        for i in range(n+1):
            new_item = QtWidgets.QTableWidgetItem("Терминал {}".format(i+1))
            self.ui.tableWidget.setItem(i, 0, new_item)            


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_win = MainWin()
    main_win.show()
    sys.exit(app.exec_())



# Перерыв до 17:20 по Мск (7 минут)