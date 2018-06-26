import os
import threading
import time
from tkinter import *
from PIL import ImageTk, Image
sys.path.append('..')
from terminal import Terminal, TerminalException
from transaction import PaymentTransaction
import sql


def get_resized_image(path, width, height):
    img = Image.open(path)
    img = img.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)


class TkTerminal(Terminal):

    def __init__(self, _id):
        self.errors = {}
        try:
            super().__init__(_id)
        except TerminalException:
            self.errors['connection'] = False
        self.root = Tk()
        self.root.title('Terminal № {}'.format(self._id))
        self.root.resizable(False, False)
        self.hs = self.root.winfo_screenheight() // 5
        self.ws = self.root.winfo_screenwidth() // 5
        self.h = int(self.root.winfo_screenheight() * 2 / 3)
        self.w = int(self.root.winfo_screenwidth() * 2 / 3)
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, self.ws, self.hs))
        self.display = Display(self, height=self.h-200, width=self.w)
        self.display.grid(row=0, columnspan=3)
        self.check_printer = CheckPrinter(self.root)
        self.check_printer.grid(row=1, column=0, pady=self.h//40, padx=self.w//30, sticky='nw')
        self.strongbox = StrongBox(self.root)
        self.strongbox.grid(row=1, column=1, sticky='nw', pady=self.h//40, padx=self.w//30)
        self.bill_acceptor = BillAcceptor(self.root)
        self.bill_acceptor.grid(row=1, column=2, sticky='ws', pady=self.h // 40, padx=self.w // 30)
        settings_img = get_resized_image(os.path.join('gif', 'settings.gif'), 20, 20)
        self.settings_btn = Button(self.root, image=settings_img, command=self.open_service)
        self.settings_btn.grid(row=2, column=0, sticky='nw', padx=10)
        self.settings_btn.image = settings_img
        self.items = []
        self.display.display_organizations()

    def open_service(self):
        print('Not implemented yet!')

    def activate_bill_acceptor(self, data, amount, account):
        self.bill_acceptor.activate()
        print(data, amount, account)

    def disable_bill_acceptor(self):
        self.bill_acceptor.disable()

    def mainloop(self):
        self.root.mainloop()


class Display(Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent.root
        self.terminal = parent
        self.parent.update()
        self.width = self.parent.winfo_width()
        self.height = self.parent.winfo_height()-200
        background_image = get_resized_image(os.path.join('gif', 'display.gif'), self.width,
                                             self.height)
        self.frame = Label(self, image=background_image)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.image = background_image
        self.types = []
        self.elements = []

    def display_organizations(self):
        self.display_types()
        self.change_page(1)

    def display_types(self):
        types = sql.get_org_types()
        for i, org_type in enumerate(types):
            btn = Button(self.frame, text=org_type[1], command=lambda x=i+1: self.change_page(x),
                         width=15)
            if i == 0:
                padx = (10, 3)
            else:
                padx = 3
            btn.grid(row=0, column=i, pady=10, padx=padx)
            self.types.append(btn)

    def change_page(self, page):
        self.flush()
        self.display_types()
        self.types[page-1].config(fg='red')
        data = sql.get_org_by_type(page)
        row = 1
        col = 0
        width = self.width // 6
        height = self.height // 4
        for i, item in enumerate(data):
            bfr = Frame(self.frame, width=width, height=height)
            filename = item[3].split('/')[-1].replace('.png', '.gif')
            img_path = os.path.join('gif', *item[3].split('/')[:-1], filename)
            btn = Button(bfr, command=lambda x=item: self.display_pay_page(x))
            try:
                image = get_resized_image(img_path, width, height)
                btn.config(image=image)
                btn.image = image
            except FileNotFoundError:
                btn.config(text=item[1])
            if not i % 5:
                col = 0
                row += 1
            if col == 0:
                padx = (self.width // 30, 10)
            else:
                padx = 10
            bfr.grid(row=row, column=col, pady=10, padx=padx, sticky='nw')
            btn.place(x=0, y=0, relwidth=1, relheight=1)
            col += 1
            self.elements.append(bfr)

    def display_pay_page(self, data):
        self.flush()
        self.frame.columnconfigure(0, weight=1)
        btn_main = Button(self.frame, text="To main page", width=15, command=lambda x=1: self.change_page(x))
        btn_main.grid(row=0, column=0, padx=50, pady=10, sticky='nw')
        phead = Label(self.frame, text='Pay for organization {}({})'.format(data[1], data[2]))
        phead.config(font=('Courier', 22), fg='blue')
        phead.grid(row=1, column=0, padx=50, pady=50, sticky='nwes')
        self.accvar = StringVar()
        self.amountvar = StringVar()
        paccl = Label(self.frame, text='Input your personal account: ', font=('Courier', 12), fg='blue')
        paccl.grid(row=2, column=0)
        self.paccl_entry = Entry(self.frame, textvariable=self.accvar, width=11)
        self.paccl_entry.grid(row=3, column=0)
        pamountl = Label(self.frame, text='Input amount: ', font=('Courier', 12), fg='blue')
        pamountl.grid(row=4, column=0)
        self.pamountl_entry = Entry(self.frame, textvariable=self.amountvar, width=11)
        self.pamountl_entry.grid(row=5, column=0)
        bfr = Frame(self.frame, width=300)
        self.error_label = Label(bfr, fg='red', font=('Courier', 12))
        self.error_label.grid(row=0, columnspan=2)
        submit = Button(bfr, text='OK', font=('Courier', 14), fg='blue', width=10,
                        command=lambda x=data: self.threaded_pay(x))
        submit.grid(row=1, column=0, padx=10)
        cancel = Button(bfr, text='Cancel', font=('Courier', 14), fg='blue', width=10,
                        command=lambda x=1: self.change_page(x))
        cancel.grid(row=1, column=1)
        bfr.grid(row=7, column=0, pady=20)
        self.elements.append(btn_main)
        self.elements.append(phead)
        self.elements.append(paccl)
        self.elements.append(self.paccl_entry)
        self.elements.append(pamountl)
        self.elements.append(self.pamountl_entry)
        self.elements.append(bfr)

    def threaded_pay(self, data):
        self.error_label.config(text='')
        try:
            amount, account = int(self.amountvar.get()), int(self.accvar.get())
        except ValueError:
            self.error_label.config(text='Please, input numbers.')
            return
        if amount < PaymentTransaction.MIN_AMOUNT // 100:
            self.error_label.config(text='Min pay {} rubles'.format(PaymentTransaction.MIN_AMOUNT // 100))
            return
        if amount > PaymentTransaction.MAX_AMOUNT // 100:
            self.error_label.config(text='Max pay {} rubles.'.format(PaymentTransaction.MAX_AMOUNT // 100))
        self.paccl_entry.config(state=DISABLED)
        self.pamountl_entry.config(state=DISABLED)
        task = threading.Thread(target=self.terminal.activate_bill_acceptor, args=(data, amount, account))
        task.start()
    def flush(self):
        """
        eliminates types and organization buttons
        :return:
        """
        self.terminal.disable_bill_acceptor()
        self.frame.columnconfigure(0, weight=0)
        for btn in self.types:
            btn.destroy()
        self.types = []
        for org in self.elements:
            org.destroy()
        self.elements = []


class CheckPrinter(Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent.update()
        self.width = parent.winfo_width() // 10
        print_img = get_resized_image(os.path.join('gif', 'check_printer.gif'), self.width, self.width)
        self.print_button = Button(self, image=print_img, command=self.print_check, state=DISABLED)
        self.print_button.image = print_img
        self.print_button.grid(row=0, column=0)

    def print_check(self):
        print('Not implemented yet!')


class StrongBox(Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent.update()
        self.width = parent.winfo_width() // 10
        print_img = get_resized_image(os.path.join('gif', 'strongbox.gif'), self.width, self.width)
        self.open_button = Button(self, image=print_img, command=self.open, state=DISABLED)
        self.open_button.image = print_img
        self.open_button.grid(row=0, column=0)

    def open(self):
        print('Not implemented yet!')


class BillAcceptor(Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent.update()
        self.width = parent.winfo_width() // 10
        print_img = get_resized_image(os.path.join('gif', 'bill_acceptor.gif'), self.width, self.width)
        self.insert_cash = Button(self, image=print_img, command=self.insert, state=DISABLED)
        self.insert_cash.image = print_img
        self.insert_cash.grid(row=0, column=0)
        self.rf = Frame(self)
        self.rf.grid(row=0, column=1)
        self.var = StringVar()
        self.entry = Entry(self.rf, textvariable=self.var, state=DISABLED, width=10)
        self.entry.grid(row=0, column=0, sticky='nw', padx=3)
        Label(self.rf, text='rubles', width=10).grid(row=1, column=0, sticky='nw', padx=3)
        self.state = 0

    def insert(self):
        print('Not implemented yet!')

    def activate(self):
        self.insert_cash.config(state=NORMAL)
        self.entry.config(state=NORMAL)
        self.active = self.after(700, self.change_image)

    def change_image(self):
        if self.state:
            print_img = get_resized_image(os.path.join('gif', 'bill_acceptor.gif'), self.width, self.width)
            self.insert_cash.config(image=print_img)
            self.insert_cash.image=print_img
            self.state =0
        else:
            print_img = get_resized_image(os.path.join('gif', 'bill_acceptor_2.gif'), self.width, self.width)
            self.insert_cash.config(image=print_img)
            self.insert_cash.image = print_img
            self.state = 1
        self.active = self.after(700, self.change_image)

    def disable(self):
        self.insert_cash.config(state=DISABLED)
        self.entry.config(state=DISABLED)
        if hasattr(self, 'active'):
            self.after_cancel(self.active)

if __name__ == '__main__':
    t = TkTerminal(1049)
    with t:
        t.mainloop()
