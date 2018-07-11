import os
import sys
import sql
import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from admin_template import Ui_AdminWindow


class MainWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_AdminWindow()
        self.ui.setupUi(self)
        self.setGeometry(QtCore.QRect(250, 150, self.geometry().width(), self.geometry().height()))
        self.fill_table('terminal')
        self.init_connections()

    def exit(self):
        sys.exit(1)

    def fill_table(self, table):
        self.flush_table()
        headers, data = sql.get_headers(table), sql.get_data(table)
        self.ui.tableWidget.setColumnCount(len(headers) + 1)
        self.ui.tableWidget.setRowCount(len(data))
        header = self.ui.tableWidget.horizontalHeader()
        for i, title in enumerate(headers):
            item = QtWidgets.QTableWidgetItem()
            item.setText('{} ({})'.format(title[1], title[2]))
            self.ui.tableWidget.setHorizontalHeaderItem(i, item)
            header.setSectionResizeMode(i, header.Stretch)
        for i, line in enumerate(data):
            for j, record in enumerate(line):
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                item.setText(str(record))
                item.setBackground(QtGui.QBrush(QtGui.QColor(255, 0, 0, 16)))
                self.ui.tableWidget.setItem(i, j, item)
            manage_btns = ManageButtons(i, self)
            self.ui.tableWidget.setCellWidget(i, len(headers), manage_btns)
            self.ui.tableWidget.setColumnWidth(len(headers), 70)

    def flush_table(self):
        for i in range(self.ui.tableWidget.rowCount()):
            for j in range(self.ui.tableWidget.columnCount()):
                # print(type(self.ui.tableWidget.itemAt(i, j)))
                self.ui.tableWidget.takeItem(i, j)

    def init_connections(self):
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionTerminals.triggered.connect(lambda: self.fill_table('terminal'))
        self.ui.actionOrganizations.triggered.connect(lambda: self.fill_table('organization'))
        self.ui.actionOrganization_Types.triggered.connect(lambda: self.fill_table('org_type'))
        self.ui.pushExit.clicked.connect(self.exit)


class ManageButtons(QtWidgets.QWidget):

    def __init__(self, id, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.parent = parent
        self.btn_edit = QtWidgets.QPushButton()
        self.btn_edit.setFixedWidth(30)
        self.btn_edit.setFixedHeight(30)
        self.btn_edit.clicked.connect(self.action_edit)
        self.btn_delete = QtWidgets.QPushButton()
        self.btn_delete.setFixedWidth(30)
        self.btn_delete.setFixedHeight(30)
        self.btn_delete.clicked.connect(self.action_delete)
        image_edit_path = os.path.join(os.path.dirname(__file__), 'img', 'admin', 'edit.png')
        bicon_edit = QtGui.QIcon()
        bicon_edit.addPixmap(QtGui.QPixmap(image_edit_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_edit.setIcon(bicon_edit)
        self.btn_edit.setIconSize(QtCore.QSize(23, 23))
        image_delete_path = os.path.join(os.path.dirname(__file__), 'img', 'admin', 'delete.png')
        bicon_delete = QtGui.QIcon()
        bicon_delete.addPixmap(QtGui.QPixmap(image_delete_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete.setIcon(bicon_delete)
        self.btn_delete.setIconSize(QtCore.QSize(23, 23))
        pLayout = QtWidgets.QGridLayout(self)
        pLayout.addWidget(self.btn_edit, 0, 0, 1, 1)
        pLayout.addWidget(self.btn_delete, 0, 1, 1, 1)
        pLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(pLayout)

    def handle(self):
        self.action()

    def action_edit(self):
        print('edit id: {} from table'.format(self.id))

    def action_delete(self):
        print('delete id: {} form table'.format(self.id))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())