"""
This module is used to admin databases of project
"""
import os
import sys
import datetime
import threading
import time
import sqlite3
sys.path.append('..')
import sql
import reports_ui
from PyQt5 import QtWidgets, QtCore, QtGui
from admin_template import Ui_AdminWindow


class MainWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_AdminWindow()
        self.ui.setupUi(self)
        self.setGeometry(QtCore.QRect(250, 150, self.geometry().width(), self.geometry().height()))
        self.change_table('organization')
        self.update_info_label()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_info_label)
        self.timer.start(1000)
        self.init_connections()

    def update_info_label(self):
        t = datetime.datetime.now()
        self.ui.labelInfo.setText('Current table: {}. {}'.format(self.table, t.strftime('%d.%m.%Y %H:%M:%S')))

    def update_ui(self, table):
        """updates table, labels, and buttons according to current page and table
        """
        self.fill_table(table)
        self.update_labels()
        self.set_next_prev_button_states()

    def change_table(self, table):
        """Handler for top menu
        """
        self.table = table
        self.total_records = sql.get_count(table)
        self.change_rpp()
        self.update_labels()
        self.update_ui(self.table)

    def fill_table(self, table):
        """fill main table with data according to current table
        """
        self.flush_table()
        headers, data = sql.get_headers(table), sql.get_data(table, self.current_page*self.rpp, self.rpp)
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setRowCount(len(data))
        header = self.ui.tableWidget.horizontalHeader()
        for i, title in enumerate(headers):
            item = QtWidgets.QTableWidgetItem()
            item.setText('{} {}'.format(title[1], title[2]))
            self.ui.tableWidget.setHorizontalHeaderItem(i, item)
        for i, line in enumerate(data):
            for j, record in enumerate(line):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(record))
                self.ui.tableWidget.setItem(i, j, item)
            if self.table != 'ps_transaction':
                self.ui.tableWidget.setColumnCount(len(headers) + 1)
                row = i + self.rpp * self.current_page + 1
                manage_btns = ManageButtons(i, row, line, self)
                self.ui.tableWidget.setCellWidget(i, len(headers), manage_btns)
                self.ui.tableWidget.setColumnWidth(len(headers), 70)
                last_item = QtWidgets.QTableWidgetItem()
                last_item.setText('Action')
                self.ui.tableWidget.setHorizontalHeaderItem(len(headers), last_item)
                header.setSectionResizeMode(len(headers), header.Interactive)
            self.set_row_disabled(i)
        self.ui.tableWidget.resizeColumnsToContents()

    def set_row_editable(self, row):
        for i in range(self.ui.tableWidget.columnCount()-1):
            self.ui.tableWidget.item(row, i).setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255, 255)))
            self.ui.tableWidget.item(row, i).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |
                                                      QtCore.Qt.ItemIsEditable)

    def set_row_disabled(self, row):
        for i in range(self.ui.tableWidget.columnCount()-1):
            self.ui.tableWidget.item(row, i).setBackground(QtGui.QBrush(QtGui.QColor(255, 0, 0, 40)))
            self.ui.tableWidget.item(row, i).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def get_row_values(self, row):
        result = []
        for i in range(self.ui.tableWidget.columnCount() - 1):
            result.append(self.ui.tableWidget.item(row, i).text())
        return result

    def restore_row(self, row, data):
        for i in range(self.ui.tableWidget.columnCount() - 1):
            self.ui.tableWidget.item(row, i).setText(data[i])

    def flush_table(self):
        """
        delete and remove widgets and items from table
        :return:
        """
        header = self.ui.tableWidget.horizontalHeader()
        for i in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.takeHorizontalHeaderItem(i)
            for j in range(self.ui.tableWidget.columnCount()):
                # print(type(self.ui.tableWidget.itemAt(i, j)))
                self.ui.tableWidget.takeItem(i, j)
                self.ui.tableWidget.removeCellWidget(i, j)

    def change_rpp(self):
        """
        changes records per page when according combobox changed
        :return:
        """
        self.rpp = int(self.ui.comboBoxPerPage.currentText())
        self.total_pages = self.total_records // self.rpp
        if self.total_records % self.rpp:
            self.total_pages += 1
        self.current_page = 0
        self.update_ui(self.table)

    def exit(self):
        sys.exit(1)

    def update_labels(self):
        """Update information labels"""
        end_value = (self.current_page +1) * self.rpp
        if end_value > self.total_records:
            end_value = self.total_records
        self.ui.labelRecordInfo.setText('Records  from {} to {}. Total: {}'.format(
            self.current_page * self.rpp,
            end_value,
            self.total_records
        ))
        self.ui.labelPage.setText('{} of {}'.format(self.current_page+1, self.total_pages))

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
        self.update_ui(self.table)

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
        self.update_ui(self.table)

    def set_next_prev_button_states(self):
        """
        Disable or enable previous, next page buttons according to current page
        :return: None
        """
        self.ui.pushNextPage.setDisabled(False)
        self.ui.pushPreviousPage.setDisabled(False)
        if self.current_page < 1:
            self.ui.pushPreviousPage.setDisabled(True)
        if self.current_page == self.total_pages - 1:
            self.ui.pushNextPage.setDisabled(True)

    def go_to_page(self, page):
        """handler for go to page button"""
        try:
            page = int(self.ui.lineEditPage.text()) - 1
        except ValueError:
            return
        if page > self.total_pages - 1:
            page = self.total_pages - 1
        if page < 0:
            page = 0
        self.current_page = page
        self.update_ui(self.table)
        self.ui.lineEditPage.setText(str(page+1))

    def init_connections(self):
        """
        Menu and buttons clicked events
        :return:
        """
        self.ui.actionExit.triggered.connect(self.exit)
        self.ui.actionTerminals.triggered.connect(lambda: self.change_table('terminal'))
        self.ui.actionTransactions.triggered.connect(lambda: self.change_table('ps_transaction'))
        self.ui.actionOrganizations.triggered.connect(lambda: self.change_table('organization'))
        self.ui.actionOrganization_Types.triggered.connect(lambda: self.change_table('org_type'))
        self.ui.actionCollectors.triggered.connect(lambda: self.change_table('collector'))
        self.ui.actionTransactionsReport.triggered.connect(
            lambda: self.show_report_dialog(reports_ui.TransactionReportDialog))
        self.ui.comboBoxPerPage.currentIndexChanged.connect(self.change_rpp)
        self.ui.pushExit.clicked.connect(self.exit)
        self.ui.pushNextPage.clicked.connect(self.next_page)
        self.ui.pushPreviousPage.clicked.connect(self.previous_page)
        self.ui.pushGoToPage.clicked.connect(self.go_to_page)
        self.ui.pushButton_add_record.clicked.connect(self.add_record_form)

    def show_report_dialog(self, dialog):
        window = dialog(self)
        window.show()

    def add_record_form(self):
        self.add_values = []
        add_window = QtWidgets.QDialog(self)
        add_window.setWindowTitle('Add record')
        grid = QtWidgets.QGridLayout(add_window)
        btn_ok = QtWidgets.QPushButton()
        btn_ok.setText('OK')
        btn_cancel = QtWidgets.QPushButton()
        btn_cancel.setText('Cancel')
        btn_cancel.clicked.connect(add_window.close)
        btn_ok.clicked.connect(self.add_record)
        headers = sql.get_headers(self.table)
        for i, head in enumerate(headers):
            label = QtWidgets.QLabel()
            label.setText('{} ({}):'.format(head[1], head[2]))
            add_value = QtWidgets.QLineEdit()
            self.add_values.append(add_value)
            grid.addWidget(label, i, 0, 1, 1)
            grid.addWidget(add_value, i, 1, 1, 1)
        self.add_error = QtWidgets.QLabel()
        grid.addWidget(self.add_error, len(headers), 0, 1, 2, QtCore.Qt.AlignCenter)
        grid.addWidget(btn_ok, len(headers)+1, 0, 1, 1)
        grid.addWidget(btn_cancel, len(headers)+1, 1, 1, 1)
        self.add_window = add_window
        add_window.exec_()

    def add_record(self):
        values = []
        for line in self.add_values:
            values.append(line.text())
        try:
            sql.insert(self.table, values)
            self.add_window.close()
            self.change_table(self.table)
        except sqlite3.IntegrityError:
            self.add_error.setText("<font color='red'>Was errors!</font>")


class ManageButtons(QtWidgets.QWidget):
    """
    Edit/Update and delete buttons right of the every record
    """
    img_dir = os.path.join(os.path.dirname(__file__), 'img', 'admin')

    def __init__(self, tpos, row, line,  parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tpos = tpos
        self.row = row
        self.row_data = line
        # print(self.row, self.tpos)
        self.parent = parent
        self.edit_status = True
        self.btn_undo = QtWidgets.QPushButton()
        self.btn_undo.setFixedWidth(30)
        self.btn_undo.setFixedHeight(30)
        self.btn_undo.setDisabled(True)
        self.btn_edit = QtWidgets.QPushButton()
        self.btn_edit.setFixedWidth(30)
        self.btn_edit.setFixedHeight(30)
        self.btn_delete = QtWidgets.QPushButton()
        self.btn_delete.setFixedWidth(30)
        self.btn_delete.setFixedHeight(30)
        self.set_bgr_image(self.btn_edit, 'edit.png')
        self.set_bgr_image(self.btn_delete, 'delete.png')
        self.set_bgr_image(self.btn_undo, 'cancel.jpg')
        self.btn_delete.clicked.connect(self.action_delete)
        self.btn_edit.clicked.connect(self.action_edit)
        self.btn_undo.clicked.connect(self.action_undo)
        pLayout = QtWidgets.QGridLayout(self)
        pLayout.addWidget(self.btn_edit, 0, 0, 1, 1)
        pLayout.addWidget(self.btn_undo, 0, 1, 1, 1)
        pLayout.addWidget(self.btn_delete, 0, 2, 1, 1)
        pLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(pLayout)

    def action_undo(self):
        self.edit_status = True
        self.btn_undo.setDisabled(True)
        self.set_bgr_image(self.btn_edit, 'edit.png')
        self.parent.set_row_disabled(self.tpos)
        self.parent.restore_row(self.tpos, self.prev_data)

    def action_edit(self):
        """
        edit and save data to database
        :return:
        """
        if self.edit_status:
            # make row editable
            self.edit_status = False
            self.btn_undo.setDisabled(False)
            self.set_bgr_image(self.btn_edit, 'apply.jpg')
            self.parent.set_row_editable(self.tpos)
            self.prev_data = self.parent.get_row_values(self.tpos)
        else:
            # saving to database, make row disabled
            self.edit_status = True
            self.btn_undo.setDisabled(True)
            self.set_bgr_image(self.btn_edit, 'edit.png')
            self.parent.set_row_disabled(self.tpos)
            self.row_data = self.parent.get_row_values(self.tpos)
            if not sql.update(self.parent.table, self.row_data, self.prev_data[0]):
                self.parent.restore_row(self.tpos, self.prev_data)

    def set_bgr_image(self, btn, img):
        path = os.path.join(self.img_dir, img)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        btn.setIcon(icon)
        btn.setIconSize(QtCore.QSize(23, 23))

    def action_delete(self, event):
        cursor = QtGui.QCursor()
        x = cursor.pos().x()
        y = cursor.pos().y()
        reqWindow = QtWidgets.QDialog(self.parent)
        reqWindow.setGeometry(QtCore.QRect(x, y, 300, 100))
        reqWindow.setWindowTitle('Deleting record')
        gridLayout = QtWidgets.QGridLayout(reqWindow)
        pushDelete = QtWidgets.QPushButton()
        pushDelete.setText('Delete')
        pushCancel = QtWidgets.QPushButton('Cancel')
        pushCancel.setText('Cancel')
        pushCancel.clicked.connect(reqWindow.close)
        pushDelete.clicked.connect(self.delete_row)
        deleteHeader = QtWidgets.QLabel()
        deleteHeader.setText('Are you sure you want to delete {} row?'.format(self.row))
        gridLayout.addWidget(deleteHeader, 0, 0, 2, 2, QtCore.Qt.AlignCenter)
        gridLayout.addWidget(pushDelete, 2, 0, 1, 1)
        gridLayout.addWidget(pushCancel, 2, 1, 1, 1)
        self.reqWindow = reqWindow
        reqWindow.exec_()

    def delete_row(self):
        sql.delete(self.parent.table, self.row_data)
        self.parent.change_table(self.parent.table)
        self.reqWindow.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())