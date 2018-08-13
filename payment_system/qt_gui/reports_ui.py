import sys
import datetime
import calendar
from PyQt5 import QtWidgets, QtCore, QtGui
sys.path.append('..')
import reports
import sql


class CommonReportDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_ui(self):
        self.grid = QtWidgets.QGridLayout(self)
        self.btn_ok = QtWidgets.QPushButton()
        self.btn_ok.setText('Form')
        self.btn_cancel = QtWidgets.QPushButton()
        self.btn_ok.clicked.connect(self.form)
        self.btn_cancel.clicked.connect(self.close)
        self.btn_cancel.setText('Cancel')
        self.header = QtWidgets.QLabel()
        self.start_date = QtWidgets.QDateTimeEdit()
        self.end_date = QtWidgets.QDateTimeEdit()
        self.from_label = QtWidgets.QLabel()
        self.from_label.setText('From: ')
        self.to_label = QtWidgets.QLabel()
        self.to_label.setText('To: ')
        self.grid.addWidget(self.header, 0, 0, 1, 4)
        self.grid.addWidget(self.from_label, 3, 0, 1, 1)
        self.grid.addWidget(self.start_date, 3, 1, 1, 1)
        self.grid.addWidget(self.to_label, 3, 2, 1, 1)
        self.grid.addWidget(self.end_date, 3, 3, 1, 1)
        self.grid.addWidget(self.btn_ok, 4, 0, 1, 2)
        self.grid.addWidget(self.btn_cancel, 4, 2, 1, 2)
        self.set_default_time_widgets()

    def set_default_time_widgets(self):
        t = datetime.datetime.now()
        start = datetime.datetime(year=t.year, month=t.month-2, day=1)
        days = calendar.monthrange(t.year, t.month)[1]
        end = datetime.datetime(year=t.year, month=t.month, day=days)
        self.start_date.setDate(start)
        self.end_date.setDate(end)

    def form(self):
        self.close()


class TransactionReportDialog(CommonReportDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build_ui()
        self.setWindowTitle('Transactions report dialog')
        self.header.setText('Choose terminal, start and end date.')

    def build_ui(self):
        super().build_ui()
        self.label_terminal = QtWidgets.QLabel()
        self.label_terminal.setText('Terminal: ')
        self.combo_terminal = QtWidgets.QComboBox()
        self.combo_terminal.addItems(['All'] + [str(x[0]) for x in sql.get_terminals()])
        self.grid.addWidget(self.combo_terminal, 1, 1, 1, 2)
        self.grid.addWidget(self.label_terminal, 1, 0, 1, 1, QtCore.Qt.AlignRight)

    def form(self):
        term_id = self.combo_terminal.currentText()
        start = self.start_date.dateTime().toPyDateTime()
        end = self.end_date.dateTime().toPyDateTime()
        if term_id == 'All':
            data = reports.select_all_transactions(start, end)
            header = 'Summary transaction information from {} to {}'.format(start, end)
            report = Paginator(data, header, self)
            report.setWindowTitle('Summary transaction information')
        else:
            data = reports.select_transactions_by_term(term_id, start, end)
            header = 'Transaction report for terminal {} from {} to {}.'.format(data[0][0], data[0][1], data[0][2])
            report = Paginator(data[1:], header, self)
            report.setWindowTitle('Transactions by terminal')
        super().form()
        report.show()


class Paginator(QtWidgets.QDialog):
    def __init__(self, data, header, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(QtCore.QRect(300, 300, 400, 600))
        self.header = header
        self.data = data
        self.rpp = 100
        self.tr = len(self.data[1:])
        self.tp = self.tr // self.rpp
        if not self.tr % self.rpp:
            self.tp -= 1
        self.page = 0
        self.build_ui()
        self.setStyleSheet("background-color: white;")

    def build_ui(self):
        self.grid = QtWidgets.QGridLayout(self)
        self.head_label = RLabel()
        self.head_label.setStyleSheet("font-weight: bold;")
        self.head_label.setText(self.header)
        self.export_dropdown = QtWidgets.QComboBox()
        self.export_dropdown.addItems(['export', 'txt', 'csv'])
        self.export_dropdown.currentIndexChanged.connect(self.export)
        self.grid.addWidget(self.export_dropdown, 0, 0, 1, 1)
        self.grid.addWidget(self.head_label, 0, 1, 1, 6, QtCore.Qt.AlignCenter)
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(self.rpp)
        self.table.setColumnCount(len(self.data[0]))
        self.grid.addWidget(self.table, 1, 0, 1, 7)
        for i, h in enumerate(self.data[0]):
            q = QtWidgets.QTableWidgetItem()
            # q.setStyleSheet("font-weight: bold; margin-bottom: 50px;")
            q.setText(h)
            self.table.setHorizontalHeaderItem(i, q)
        self.data = self.data[1:]
        self.prev_btn = QtWidgets.QPushButton()
        self.prev_btn.setText('<<')
        self.grid.addWidget(self.prev_btn, 2, 0, 1, 1)
        self.next_btn = QtWidgets.QPushButton()
        self.next_btn.setText('>>')
        self.grid.addWidget(self.next_btn, 2, 2, 1, 1)
        self.cur_page_label = QtWidgets.QLabel()
        self.grid.addWidget(self.cur_page_label, 2, 1, 1, 1)
        self.goto_label = QtWidgets.QLabel()
        self.goto_label.setText('Go to page: ')
        self.grid.addWidget(self.goto_label, 2, 3, 1, 1)
        self.goto_value = QtWidgets.QLineEdit()
        self.goto_value.setText('0')
        self.grid.addWidget(self.goto_value, 2, 4, 1, 1)
        self.goto_btn = QtWidgets.QPushButton()
        self.goto_btn.setText('GO')
        self.grid.addWidget(self.goto_btn, 2, 5, 1, 1)
        self.status_label = QtWidgets.QLabel()
        self.grid.addWidget(self.status_label, 2, 6, 1, 1)
        self.next_btn.clicked.connect(self.next_page)
        self.prev_btn.clicked.connect(self.prev_page)
        self.goto_btn.clicked.connect(self.goto_page)
        self.build_page()

    def prev_page(self):
        self.page -= 1
        self.build_page()

    def next_page(self):
        self.page += 1
        self.build_page()

    def goto_page(self):
        try:
            page = int(self.goto_value.text())
        except ValueError:
            return
        if page > self.tp:
            page = self.tp
        if page < 0:
            page = 0
        self.page = page
        self.build_page()

    def update_btn_status(self):
        self.next_btn.setDisabled(False)
        self.prev_btn.setDisabled(False)
        if self.page == self.tp:
            self.next_btn.setDisabled(True)
        if self.page == 0:
            self.prev_btn.setDisabled(True)

    def export(self):
        print('Exporting to {}'.format(self.export_dropdown.currentIndex()))

    def get_status_text(self):
        lp = (self.page+1) * self.rpp
        if lp > self.tr:
            lp = self.tr
        text = "Page {} of {}. Records {}-{} of {}.".format(
            self.page,
            self.tp,
            self.page * self.rpp,
            lp,
            self.tr,
        )
        return text

    def build_page(self):
        self.update_btn_status()
        self.cur_page_label.setText(str(self.page))

        self.status_label.setText(self.get_status_text())
        working_data = self.data[self.rpp*self.page: self.rpp*(self.page+1)]
        for j, record in enumerate(working_data):
            for i, item in enumerate(record):
                ins = QtWidgets.QTableWidgetItem()
                ins.setText(str(item))
                self.table.setItem(j, i, ins)
        if len(working_data) < self.rpp:
            for i in range(len(working_data), self.rpp):
                for j in range(len(working_data[0])):
                    self.table.takeItem(i, j)
                    self.table.removeCellWidget(i, j)


class RLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
