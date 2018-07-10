import os
import sys
import sql
from PyQt5 import QtWidgets, QtCore, QtGui
from admin_template import Ui_AdminWindow


class MainWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_AdminWindow()

        self.ui.setupUi(self)
        self.ui.actionExit.triggered.connect(self.exit)
        self.setGeometry(QtCore.QRect(250, 150, self.geometry().width(), self.geometry().height()))
        self.fill_table(sql.get_terminals(), ('Termianl ID', 'Last transaction id', 'Cash', 'State'), 'terminal')

    def exit(self):
        sys.exit(1)

    def fill_table(self, data, headers, table):
        self.ui.tableWidget.setColumnCount(len(headers) + 2)
        self.ui.tableWidget.setRowCount(len(data))
        for i, title in enumerate(headers):
            item = QtWidgets.QTableWidgetItem()
            item.setText(title)
            self.ui.tableWidget.setHorizontalHeaderItem(i, item)
        for i, line in enumerate(data):
            for j, record in enumerate(line):
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                item.setText(str(record))
                item.setBackground(QtGui.QBrush(QtGui.QColor(255, 0, 0, 16)))
                self.ui.tableWidget.setItem(i, j, item)
            edit_btn = ManageButton(i, 'edit', self)
            del_btn = ManageButton(i, 'delete', self)
            self.ui.tableWidget.setCellWidget(i, len(headers), edit_btn)
            self.ui.tableWidget.setCellWidget(i, len(headers)+1, del_btn)


class ManageButton(QtWidgets.QWidget):

    def __init__(self, id, action, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.btn = QtWidgets.QPushButton()
        self.btn.setFixedWidth(20)
        self.btn.setFixedHeight(20)
        self.btn.clicked.connect(self.handle)
        # self.btn.setText(action)
        if action == 'edit':
            image_file = 'edit.png'
        elif action == 'delete':
            image_file = 'delete.png'
        image_url = os.path.join(os.path.dirname(__file__), 'img', 'admin', image_file)
        self.btn.setStyleSheet('border-image:url({});'.format(image_url))
        pLayout = QtWidgets.QHBoxLayout(self)
        pLayout.addWidget(self.btn)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(pLayout)
        self.id = id
        self.parent = parent
        self.action = getattr(self, action)

    def handle(self):
        self.action()

    def edit(self):
        print('edit id: {} from table {}'.format(self.id, self.parent.table))

    def delete(self):
        print('delete id: {} form table {}'.format(self.id, self.parent.table))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())