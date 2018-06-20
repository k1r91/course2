import sys
import datetime
from collections import OrderedDict
from tkinter import *
sys.path.append('..')
import reports


def report_transactions(parent):
    report = TrDialogReport(parent)
    report.mainloop()


class TrDialogReport(Toplevel):
    """
    class to display dialog box of report for transactions
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ws, hs = parent.winfo_screenwidth(), parent.winfo_screenheight()
        self.geometry('{}x{}+{}+{}'.format(500, 500, ws//4, hs//5))
        self.start_date = DateEntry(self, 'Start date')
        self.start_date.grid(row=0, column=0)
        self.title('Transaction report')
        self.grid_buttons()

    def grid_buttons(self):
        bw = 15
        self.button_form = Button(self, text='Generate', command=self.generate, width=bw)
        self.button_form.grid(row=1, column=0)
        self.button_cancel = Button(self, text='Cancel', command=self.destroy, width=bw)
        self.button_cancel.grid(row=1, column=1)

    def generate(self):
        print(self.start_date.get_values())


class ReportWindow(Toplevel):
    """
    class to display report data
    """


class DateEntry(Frame):

    def __init__(self, parent, dtitle, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        if dtitle is not None:
            self.dtitle = Label(self, text=dtitle)
            self.dtitle.grid(row=0, columnspan=3)
        self.day, self.month, self.year = Label(self, text='day'), Label(self, text='month'), Label(self, text='year')
        en_w = 5
        self.labels = OrderedDict()
        self.labels[self.day] = Entry(self, width=en_w)
        self.labels[self.month] = Entry(self, width=en_w)
        self.labels[self.year] = Entry(self, width=en_w)
        self.set_default_date(self.labels)
        i = 0
        for label, entry in self.labels.items():
            label.grid(row=1, column=i)
            entry.grid(row=2, column=i)
            i += 1
        self.error_span = Label(self, fg='red')
        self.error_span.grid(row=3, columnspan=3)

    def set_default_date(self, labels):
        day = StringVar()
        day.set(datetime.datetime.now().day)
        month = StringVar()
        month.set(datetime.datetime.now().month)
        year = StringVar()
        year.set(datetime.datetime.now().year)
        labels[self.day].config(textvariable=day)
        labels[self.month].config(textvariable=month)
        labels[self.year].config(textvariable=year)

    def get_values(self):
        return self.labels[self.day].get(), self.labels[self.month].get(), self.labels[self.year].get()

    def check_errors(self):
        pass