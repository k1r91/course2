import datetime
import calendar
from collections import OrderedDict
from tkinter import *
sys.path.append('..')
import reports
import sql


def report_transactions(parent):
    report = TrReportDialog(parent)
    report.mainloop()


def report_one_org(parent):
    report = OneOrgDialogReport(parent)
    report.mainloop()

def report_all_org(parent):
    report = AllOrgReportDialog(parent)
    report.mainloop()


class CommonReportDialog(Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        ws, hs = parent.winfo_screenwidth(), parent.winfo_screenheight()
        self.geometry('{}x{}+{}+{}'.format(350, 350, ws // 4, hs // 5))
        self.dialog = CommonReportFrame(self)
        self.dialog.grid(row=1, columnspan=2)
        self.dialog.button_form.config(command=self.generate)

    def check_dates(self):
        self.dialog.span_error.config(text='')
        self.start = self.get_start_date()
        self.end = self.get_end_date()
        if self.end < self.start:
            self.dialog.span_error.config(text='Start date must be lower than end')
            return False
        return True

    def generate(self):
        raise NotImplementedError('Have to generate this function')

    def get_start_date(self):
        return self.dialog.start_date.get_values()

    def get_end_date(self):
        return self.dialog.end_date.get_values()


class AllOrgReportDialog(CommonReportDialog):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title('All organizations report')

    def generate(self):
        if not self.check_dates():
            return
        data = reports.total_calculate_sum(self.start, self.end)
        report = AllOrgReportWindow(self, data)
        report.mainloop()


class AllOrgReportWindow(Toplevel):
    def __init__(self, parent, data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ws, hs = parent.winfo_screenwidth(), parent.winfo_screenheight()
        self.geometry('{}x{}+{}+{}'.format(650, 600, ws // 4 + 50, hs // 5 + 50))
        self.title('All organizations report data')
        Label(self, text='Report for all organizations from {} to {}'.format(data[0][0], data[0][1])).\
            grid(row=0, column=0)
        self.display_data = Paginator(self, data[1:], cell_width=17, psize=16)
        self.display_data.grid(row=1, column=0)


class OneOrgDialogReport(CommonReportDialog):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title('One organization report')
        self.organizations = sql.get_org_and_types()
        Label(self, text='  Choose organization: ').grid(row=0, column=0)
        self.var = StringVar()
        self.var.set(self.organizations[0])
        self.options = OptionMenu(self, self.var, *self.organizations)
        self.options.config(width=28)
        self.options.grid(row=0, column=1)

    def generate(self):
        if not self.check_dates():
            return
        report = Toplevel(self)
        ws, hs = self.parent.winfo_screenwidth(), self.parent.winfo_screenheight()
        report.geometry('{}x{}+{}+{}'.format(650, 600, ws // 4 + 50, hs // 5 + 50))
        org_id = int([var.lstrip() for var in self.var.get()[1:-1].split(',')][0])
        Label(report, text=reports.calculate_sum(org_id, self.start, self.end)).pack(side=TOP)
        report.mainloop()


class TrReportDialog(CommonReportDialog):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title('Transaction report')
        Label(self, text='Terminal id: ').grid(row=0, column=0, sticky='e')
        self.terminal_id = StringVar()
        self.terminal_id.set('1049')
        self.terminal_id_cell = Entry(self, textvariable=self.terminal_id, width=5)
        self.terminal_id_cell.grid(row=0, column=1, sticky='w')

    def get_terminal_id(self):
        return self.terminal_id.get()

    def generate(self):
        if not self.check_dates():
            return
        try:
            t_id = int(self.get_terminal_id())
            if t_id < 0:
                self.dialog.span_error.config(text='Terminal id must be positive integer')
                return
        except ValueError:
            self.dialog.span_error.config(text='Terminal id must be integer')
            return
        report = TransactionReportWindow(self, reports.select_transactions_by_term(t_id, self.start, self.end))
        report.mainloop()


class CommonReportFrame(Frame):
    """
    class to display dialog box of report for transactions
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.start_date = DateEntry(self, 'Start date')
        self.end_date = DateEntry(self, 'End date', start=False)
        self.start_date.grid(row=0, column=0)
        self.end_date.grid(row=0, column=1)
        self.grid_buttons()
        self.span_error = Label(self, fg='red')
        self.span_error.grid(row=1, columnspan=2)

    def grid_buttons(self):
        bw = 15
        self.button_form = Button(self, text='Generate', width=bw)
        self.button_form.grid(row=2, column=0)
        self.button_cancel = Button(self, text='Cancel', command=self.parent.destroy, width=bw)
        self.button_cancel.grid(row=2, column=1)


class TransactionReportWindow(Toplevel):
    """
    class to display transaction report data
    """

    def __init__(self, parent, data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ws, hs = parent.winfo_screenwidth(), parent.winfo_screenheight()
        self.geometry('{}x{}+{}+{}'.format(650, 600, ws // 4 + 50, hs // 5 + 50))
        self.title('Transaction report data')
        if data[1] is None:
            Label(self, text='There are no information for terminal №{} in database'.format(data[0][0])).grid(
                row=0, column=0)
            return
        self.data = data
        Label(self, text='Transactions for terminal №{} from {} to {}'.format(
            self.data[0][0], self.data[0][1], self.data[0][2]
        )).grid(row=0, column=0)
        self.display_data = Paginator(self, data[1:], cell_width=17, psize=25)
        self.display_data.grid(row=1, column=0)


class Paginator(Frame):

    def __init__(self, parent, data, psize=20, cell_width=12, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.cw = cell_width
        self.psize = psize
        self.page = 0
        for i, item in enumerate(data[0]):
            Label(self, text=item, width=self.cw, anchor='w').grid(row=0, column=i, sticky='w')
        self.total_pages = len(data[1:]) // self.psize
        self.data = data[1:]
        self.bottom = Frame(self)
        self.bottom.grid(row=1+len(data), columnspan=len(data[0]))
        self.btn_left = Button(self.bottom, text='<', command=self.go_left)
        self.btn_left.grid(row=0, column=0)
        self.label_page = Label(self.bottom, text='Page {} of {}'.format(self.page, self.total_pages))
        self.label_page.grid(row=0, column=1)
        self.btn_right = Button(self.bottom, text='>', command=self.go_right)
        self.btn_right.grid(row=0, column=2)

        self.display_records = []
        self.display_data()
        self.button_state_config()
        Label(self.bottom, text='   Go to page: ').grid(row=0, column=3)
        self.gotopage = StringVar()
        self.gotopage.set(self.total_pages)
        self.gotopage_entry = Entry(self.bottom, textvariable=self.gotopage, width=6)
        self.gotopage_entry.grid(row=0, column=4)
        self.goto_btn = Button(self.bottom, text='go', command=self.goto)
        self.goto_btn.grid(row=0, column=5)

    def goto(self):
        page = self.gotopage.get()
        try:
            page = int(page)
        except TypeError:
            return
        if page > self.total_pages:
            self.page = self.total_pages
        elif page < 0:
            self.page = 0
        else:
            self.page = page
        self.display_data()

    def display_data(self):
        self.label_page.config(text='   Page {} of {}   '.format(self.page, self.total_pages))
        piece = self.data[self.page * self.psize: (self.page+1) * self.psize]
        for i, record in enumerate(piece):
            try:
                rowls = self.display_records[i]
            except IndexError:
                self.display_records.append([])
            for j, item in enumerate(record):
                try:
                    cell = self.display_records[i][j]
                    cell.config(text=item)
                except IndexError:
                    label = Label(self, text=item, anchor='w', width=self.cw)
                    label.grid(row=i+1, column=j, sticky='w')
                    self.display_records[i].append(label)
        if len(piece) < self.psize:
            for line in self.display_records[len(piece): self.psize]:
                for label in line:
                    label.config(text='')
        self.button_state_config()

    def button_state_config(self):
        self.btn_left.config(state=NORMAL)
        self.btn_right.config(state=NORMAL)
        if self.page == self.total_pages:
            self.btn_right.config(state=DISABLED)
        if self.page == 0:
            self.btn_left.config(state=DISABLED)


    def go_left(self):
        if self.page == 0:
            return
        else:
            self.page -= 1
            self.display_data()

    def go_right(self):
        if self.page >= self.total_pages:
            return
        self.page += 1
        self.display_data()


class DateEntry(Frame):

    def __init__(self, parent, dtitle, start=True, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.start = start
        if dtitle is not None:
            self.dtitle = Label(self, text=dtitle)
            self.dtitle.grid(row=0, columnspan=3)
        self.day, self.month, self.year = Label(self, text='day'), Label(self, text='month'), Label(self, text='year')
        self.hour, self.minute, self.second = Label(self, text='hour'), Label(self, text='min'), Label(self, text='sec')
        en_w = 5
        self.dates = OrderedDict()
        self.times = OrderedDict()
        self.dates[self.day] = Entry(self, width=en_w)
        self.dates[self.month] = Entry(self, width=en_w)
        self.dates[self.year] = Entry(self, width=en_w)
        self.times[self.hour] = Entry(self, width=en_w)
        self.times[self.minute] = Entry(self, width=en_w)
        self.times[self.second] = Entry(self, width=en_w)
        self.set_default_date(self.dates)
        self.set_default_time(self.times)
        i = 0
        for label, entry in self.dates.items():
            label.grid(row=1, column=i)
            entry.grid(row=2, column=i)
            i += 1
        i = 0
        for label, entry in self.times.items():
            label.grid(row=3, column=i)
            entry.grid(row=4, column=i)
            i += 1
        self.error_span = Label(self, fg='red')
        self.error_span.grid(row=5, columnspan=3)

    def set_default_date(self, labels):
        day = StringVar()
        month = StringVar()
        month_str = datetime.datetime.now().strftime('%m')
        month.set(month_str)
        year_str = datetime.datetime.now().year
        year = StringVar()
        year.set(year_str)
        if self.start:
            day.set('01')
        else:
            day.set(calendar.monthrange(year_str, int(month_str))[1])
        labels[self.day].config(textvariable=day)
        labels[self.month].config(textvariable=month)
        labels[self.year].config(textvariable=year)

    def set_default_time(self, labels):
        hour, minute, second = StringVar(), StringVar(), StringVar()
        if self.start:
            hour.set('00')
            minute.set('00')
            second.set('00')
        else:
            hour.set('23')
            minute.set('59')
            second.set('59')
        labels[self.hour].config(textvariable=hour)
        labels[self.minute].config(textvariable=minute)
        labels[self.second].config(textvariable=second)

    def get_values(self):
        self.error_span.config(text='')
        values = [int(x) for x in (self.dates[self.day].get(), self.dates[self.month].get(), self.dates[self.year].get(),
                                 self.times[self.hour].get(), self.times[self.minute].get(),
                                 self.times[self.second].get())]
        try:
            result = datetime.datetime(day=values[0], month=values[1], year=values[2], hour=values[3], minute=values[4],
                                       second=values[5])
            return result
        except ValueError as e:
            self.error_span.config(text='Incorrect date')