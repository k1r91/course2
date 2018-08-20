import threading
import datetime
from PyQt5 import QtWidgets, QtCore, QtGui


class Display(QtCore.QObject):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.ui = parent.ui
        self.layout_top = self.ui.horizontal_display_top_layout
        self.grid_bottom = self.ui.grid_bottom
        self.config_error_page()
        self.parent.refresh_org_db()
        self.current_page = 0
        self.load_status_string()
        self.header_buttons = list()
        self.org_buttons = list()

    def flush_screen(self):
        elems = self.header_buttons + self.org_buttons
        for elem in elems:
            elem.close()

    def load_main_screen(self):
        self.org_buttons = list()
        self.header_buttons = list()
        self.parent.refresh_org_db()
        for i, t in enumerate(self.parent.types):
            btn = DisplayButton(None, None, 120, 30, text=t[1])
            self.layout_top.addWidget(btn, QtCore.Qt.AlignLeft)
            self.header_buttons.append(btn)
            btn.clicked.connect(self.change_main_screen_page(i))
        self.make_active_header_buttons()
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.layout_top.addItem(spacerItem)
        row = 0
        col = 0
        for org in self.get_current_page_organizations():
            btn = DisplayButton(None, org[4], 195, 130)
            self.org_buttons.append(btn)
            self.grid_bottom.addWidget(btn, row, col, 1, 1, QtCore.Qt.AlignTop)
            col += 1
            if col % 5 == 0:
                row += 1
                col = 0
        self.load_organization_info()

    def load_organization_info(self):
        self.make_active_header_buttons()
        for i, org in enumerate(self.get_current_page_organizations()):
            # -----------------------------
            print(org)
            # -----------------------------
            self.org_buttons[i].change_icon(org[4])
            self.org_buttons[i].id = org[0]
            if self.org_buttons[i].connected:
                self.org_buttons[i].clicked.disconnect(self.org_buttons[i].not_implemented)
            self.org_buttons[i].clicked.connect(self.org_buttons[i].not_implemented)
            self.org_buttons[i].connected = True

    def change_main_screen_page(self, page):
        def change_page():
            def single_change():
                self.current_page = page
                self.load_organization_info()
            single_change()
        return change_page

    def make_active_header_buttons(self):
        for btn in self.header_buttons:
            btn.setStyleSheet('color: black;')
        self.header_buttons[self.current_page].setStyleSheet('color: red;')

    def load_status_string(self):
        self.update_status_label()
        self.status_timer = QtCore.QTimer()
        self.status_timer.timeout.connect(self.update_status_label)
        self.status_timer.start(1000)

    def update_status_label(self):
        now = datetime.datetime.now()
        text = 'Payment system inc. All rights reserved.  {}'.format(now.strftime('%H:%M:%S %d.%m.%Y'))
        self.ui.label_status.setText(text)

    def get_current_page_organizations(self):
        result = list()
        for org in self.parent.organizations:
            if org[3] == self.parent.types[self.current_page][0]:
                result.append(org)
        return result

    def config_error_page(self):
        self.error_label = QtWidgets.QLabel('Sorry, current terminal is under maintenance.')
        self.error_label.setStyleSheet("font-weight: bold; color: red; border-image: none; font-size: 36px;")

    def load_error_screen(self):
        self.ui.label_status.hide()
        self.grid_bottom.addWidget(self.error_label, 0, 0, 1, 1, QtCore.Qt.AlignCenter)


class DisplayButton(QtWidgets.QPushButton):
    def __init__(self, org_id, icon_path, w, h, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = w
        self.height = h
        self.setFixedWidth(w)
        self.setFixedHeight(h)
        self.setStyleSheet('border-image: none; background-color: white;')
        self.id = org_id
        self.change_icon(icon_path)
        self.connected = False

    def change_icon(self, icon_path):
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(self.icon)
        i_size = QtCore.QSize(self.width-5, self.height-5)
        self.setIconSize(i_size)

    def not_implemented(self):
        print(self.id)