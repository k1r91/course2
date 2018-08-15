import os
import sys
import datetime
import calendar
import threading
import csv
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
        self.start = self.start_date.dateTime().toPyDateTime()
        self.end = self.end_date.dateTime().toPyDateTime()
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
        self.terminals = [str(x[0]) for x in sql.get_terminals()]
        self.combo_terminal.addItems(['All'] + self.terminals)
        self.grid.addWidget(self.combo_terminal, 1, 1, 1, 2)
        self.grid.addWidget(self.label_terminal, 1, 0, 1, 1, QtCore.Qt.AlignRight)

    def form(self):
        super().form()
        term_id = self.combo_terminal.currentText()
        if term_id == 'All':
            data = reports.select_all_transactions(self.start, self.end)
            header = 'Summary transaction information from {} to {}'.format(self.start, self.end)
            report = Paginator(data, header, self)
            report.setWindowTitle('Summary transaction information')
        else:
            data = reports.select_transactions_by_term(term_id, self.start, self.end)
            header = 'Transaction report for terminal {} from {} to {}.'.format(data[0][0], data[0][1], data[0][2])
            report = Paginator(data[1:], header, self)
            report.setWindowTitle('Transactions by terminal')
        report.show()


class TimeSpanReportDialog(TransactionReportDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Timespan report dialog')

    def build_ui(self):
        super().build_ui()
        self.spans = QtWidgets.QComboBox()
        spans = [(0, 6, 12, 18, 24),
                 (0, 3, 6, 9, 12, 15, 18, 21, 24),
                 (0, 12, 24)]
        for i, span in enumerate(spans):
            self.spans.addItem(str(span))
            self.spans.setItemData(i, span)
        self.grid.addWidget(self.spans, 1, 3, 1, 1)
        span_l = QtWidgets.QLabel()
        span_l.setText('Choose timespan')
        self.grid.addWidget(span_l, 0, 3, 1, 1)

    def form(self):
        CommonReportDialog.form(self)
        current_span = self.spans.itemData(self.spans.currentIndex())
        if self.combo_terminal.currentText() == 'All':
            data = reports.timespan_report_v2(self.terminals[0], current_span , self.start, self.end)
            for i, term in enumerate(self.terminals[1:]):
                sqld = reports.timespan_report_v2(term, current_span, self.start, self.end)
                for item in sqld[1:]:
                    data.append(item)
            header = 'Timespan report for all terminals from {} to {} with span: {}'.format(self.start, self.end,
                                                                                            current_span)
        else:
            data = reports.timespan_report_v2(self.combo_terminal.currentText(), current_span,
                                              self.start, self.end)
            header = 'Timespan report for terminal {} from {} to {} with span {}.'.format(
                self.combo_terminal.currentText(), self.start, self.end, current_span)
        report = Paginator(data, header, self)
        report.setWindowTitle('Timespan report')
        report.show()


class IndebtednessReportDialog(CommonReportDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Indebtedness to organizations')
        self.build_ui()

    def build_ui(self):
        super().build_ui()
        self.org_l = QtWidgets.QLabel()
        self.org_l.setText('Choose organization:')
        self.combo_org = QtWidgets.QComboBox()
        self.combo_org.addItem('All')
        for i, org in enumerate(sql.get_org_and_types()):
            self.combo_org.addItem('{} ({})'.format(org[1], org[2]))
            self.combo_org.setItemData(i+1, org[0])
        self.grid.addWidget(self.combo_org, 0, 1, 1, 2)
        self.grid.addWidget(self.org_l, 0, 0, 1, 1)

    def form(self):
        super().form()
        if self.combo_org.currentText() == 'All':
            data = reports.total_calculate_sum_v2(start=self.start, end=self.end)
            header = 'Summary indebtedness report for all organizations from {} to {}.'.format(self.start, self.end)
        else:
            data = reports.total_calculate_sum_v2(self.combo_org.itemData(self.combo_org.currentIndex()), self.start,
                                                  self.end)
            header = 'Summary indebtedness report for {} from {} to {}.'.format(
                self.combo_org.currentText(),
                self.start,
                self.end
            )
        report = Paginator(data, header, self)
        report.setWindowTitle('Indebtedness report')
        report.show()


class SummaryByTermReportDialog(CommonReportDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Summary report for all terminals')
        self.build_ui()

    def form(self):
        super().form()
        data = reports.calculate_sum_by_all_terms(self.start, self.end)
        header = 'Summary report for all terminals from {} to {}.'.format(self.start, self.end)
        report = Paginator(data, header, self)
        report.setWindowTitle('Summary report for all terminals')
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
        self.table_headers = self.data[0]
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
        if self.export_dropdown.currentIndex() == 0:
            return
        export_format = self.export_dropdown.currentText()
        export_window = QtWidgets.QDialog(self)
        grid = QtWidgets.QGridLayout(export_window)
        export_window.setWindowTitle('Export to {}'.format(export_format))
        ex_label = QtWidgets.QLabel()
        ex_label.setText('Insert file path:')
        ex_path = QtWidgets.QLineEdit()
        ex_path.setText(os.getcwd() + '/data.{}'.format(export_format))
        ex_path.setMinimumWidth(350)
        ex_ok = QtWidgets.QPushButton()
        ex_ok.setText('Export')
        ex_ok.clicked.connect(lambda: self.export_thread(export_format, ex_path.text()))
        ex_cancel = QtWidgets.QPushButton()
        ex_cancel.setText('Cancel')
        ex_cancel.clicked.connect(export_window.close)
        self.ex_progress_bar = QtWidgets.QProgressBar()
        grid.addWidget(ex_label, 0, 0, 1, 1)
        grid.addWidget(ex_path, 0, 1, 1, 1)
        grid.addWidget(ex_ok, 0, 2, 1, 1)
        grid.addWidget(ex_cancel, 0, 3, 1, 1)
        grid.addWidget(self.ex_progress_bar, 1, 0, 1, 4)
        export_window.show()

    def export_thread(self, ex_format, path):
        task = threading.Thread(target=self.make_export, args=(ex_format, path), daemon=True)
        task.start()

    def make_export(self, ex_format, path):
        tsize = len(self.data)
        if ex_format == 'txt':
            with open(path, 'w', encoding='utf-8') as ex_file:
                ex_file.write(self.header + os.linesep)
                ex_file.write(' '.join(self.table_headers) + os.linesep)
                for i, record in enumerate(self.data):
                    self.ex_progress_bar.setValue(i/tsize*100)
                    ex_file.write(''.join([' '.join([str(x) for x in record]), os.linesep]))
        elif ex_format == 'csv':
            with open(path, 'w', encoding='utf-8') as ex_file:
                csv_writer = csv.writer(ex_file)
                csv_writer.writerow([self.header])
                csv_writer.writerow(self.table_headers)
                for i, record in enumerate(self.data):
                    self.ex_progress_bar.setValue(i/tsize*100)
                    csv_writer.writerow(record)
        self.ex_progress_bar.setValue(100)

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
