import os
import datetime
import time
import fpdf
from PyQt5 import QtGui, QtCore


class CheckPrinter:

    def __init__(self, parent, *args, **kwargs):
        self.terminal = parent
        self.ui = parent.ui
        self.main_button = self.ui.pushCheckPrinter
        self.state = 0
        self.active = False
        self.main_button.clicked.connect(self.print_check)
        self.data = dict()

    def activate(self, data):
        self.data = data
        self.active = True
        self.main_button.setEnabled(True)
        while self.active:
            time.sleep(.5)
            self.change_image()

    def deactivate(self):
        self.active = False
        self.main_button.setEnabled(False)

    def change_image(self):
        if self.state:
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap("img/terminal/check_printer_2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.main_button.setIcon(icon8)
            self.main_button.setIconSize(QtCore.QSize(200, 200))
            self.state = 0
        else:
            icon8 = QtGui.QIcon()
            icon8.addPixmap(QtGui.QPixmap("img/terminal/check_printer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.main_button.setIcon(icon8)
            self.main_button.setIconSize(QtCore.QSize(200, 200))
            self.state = 1

    def print_check(self):
        self.print_skeleton(self.data['terminal_id'], self.data['org'][1], self.data['org_type'], self.data['account'],
                            self.data['amount'], self.data['last_transaction_id']-1)
        self.deactivate()

    @staticmethod
    def print_skeleton(term_id, org, org_type, account, amount, transaction_id):
        '''
        Print check according to parameters
        :return:
        '''
        for file in os.scandir('checks'):
            os.remove(file.path)
        check_name = str(time.time()).replace('.', '') + '.pdf'
        check_path = os.path.join('checks', check_name)
        pdf = fpdf.FPDF()
        pdf.add_font('dejavu', '', os.path.join(os.getcwd(), 'fonts', 'dejavu.ttf'),  uni=True)
        pdf.add_font('dejavu', 'B', os.path.join(os.getcwd(), 'fonts', 'dejavu_bold.ttf'), uni=True)
        pdf.add_page()
        font = 'dejavu'
        pdf.set_font(font, 'B', size=24)
        pdf.cell(0, 10, '', 0, 1)
        pdf.cell(0, 0, 'Payment System Inc.', 0, 1, 'C')
        pdf.set_font(font, '', 12)
        pdf.cell(0, 15, 'All rights reserved.', 0, 1, 'C')
        pdf.set_font('Arial', '', 20)
        pdf.cell(0, 30, 'Terminal #{}'.format(term_id), 0, 1, 'C')
        font_left = (font, 'B', 16)
        font_right = (font, '', 16)
        pdf.set_font(*font_left)
        x_offset = 70
        x_margin = 50
        x_big_offset = x_offset + x_margin
        pdf.set_x(x_offset)
        pdf.cell(0, 10, 'Organization')
        pdf.set_font(*font_right)
        pdf.set_x(x_big_offset)
        pdf.cell(0, 10, u'{} ({})'.format(org, org_type))
        pdf.set_font(*font_left)
        pdf.set_xy(x_offset, 75)
        pdf.cell(0, 10, 'Account')
        pdf.set_font(*font_right)
        pdf.set_xy(x_big_offset, 75)
        pdf.cell(0, 10, str(account))
        pdf.set_font(*font_left)
        pdf.set_xy(x_offset, 85)
        pdf.cell(0, 10, 'Amount')
        pdf.set_font(*font_right)
        pdf.set_xy(x_big_offset, 85)
        pdf.cell(0, 10, '{} rub.'.format(amount))
        pdf.set_font(*font_left)
        pdf.set_xy(x_offset, 95)
        pdf.cell(0, 10, 'Date')
        pdf.set_font(*font_right)
        pdf.set_xy(x_big_offset, 95)
        pdf.cell(0, 10, datetime.datetime.now().strftime(' %H:%M:%S  %d.%m.%Y'))
        pdf.set_font(*font_left)
        pdf.set_xy(x_offset, 105)
        pdf.cell(0, 10, 'Transaction')
        pdf.set_font(*font_right)
        pdf.set_xy(x_big_offset, 105)
        pdf.cell(0, 10, str(transaction_id))

        pdf.set_font(*font_left)
        pdf.set_y(120)
        pdf.cell(0, 10, 'Thank you for using Payment System inc.', 0, 1, 'C')
        pdf.set_y(130)
        pdf.cell(0, 10, 'See you soon!', 0, 1, 'C')

        pdf.output(check_path, 'F')
        full_path = os.path.join(os.getcwd(), check_path)
        if os.name == 'posix':
            os.system('/usr/bin/xdg-open ' + full_path)
        elif os.name == 'nt':
            os.startfile(full_path)

if __name__ == '__main__':
    CheckPrinter.print_skeleton(1049, 'Билайн', 'Телефония', 89049864438, 1000, 4085)