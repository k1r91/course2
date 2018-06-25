import os
from tkinter import *
from PIL import ImageTk, Image
sys.path.append('..')
from terminal import Terminal, TerminalException
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
        self.display = Display(self.root, height=self.h-200, width=self.w)
        self.display.grid(row=0, columnspan=3)
        self.check_printer = CheckPrinter(self.root)
        self.check_printer.grid(row=1, column=0, pady=self.h//30, padx=self.w//30, sticky='nw')
        self.strongbox = StrongBox(self.root)
        self.strongbox.grid(row=1, column=1, sticky='nw', pady=self.h//30, padx=self.w//30)
        self.bill_acceptor = BillAcceptor(self.root)
        self.bill_acceptor.grid(row=1, column=2, sticky='ws', pady=self.h // 30, padx=self.w // 30)
        settings_img = get_resized_image(os.path.join('gif', 'settings.gif'), 20, 20)
        self.settings_btn = Button(self.root, image=settings_img, command=self.open_service)
        self.settings_btn.grid(row=2, column=0, sticky='nw')
        self.settings_btn.image = settings_img
        self.items = []
        self.display.load_organizations()

    def open_service(self):
        print('Not implemented yet!')

    def mainloop(self):
        self.root.mainloop()


class Display(Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent.update()
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()-200
        background_image = get_resized_image(os.path.join('gif', 'display.gif'), self.width,
                                             self.height)
        self.frame = Label(self, image=background_image)
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.image = background_image
        self.types = []
        self.orgs = []

    def load_organizations(self):
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
        for btn in self.types:
            btn.config(fg='black')
        self.types[page-1].config(fg='red')
        for org in self.orgs:
            org.destroy()
        data = sql.get_org_by_type(page)
        print(data)
        row = 1
        col = 0
        width = self.width // 6
        height = self.height // 4
        print(width, height)
        for i, item in enumerate(data):
            bfr = Frame(self.frame, width=width, height=height)
            filename = item[3].split('/')[-1].replace('.png', '.gif')
            img_path = os.path.join('gif', *item[3].split('/')[:-1], filename)
            try:
                image = get_resized_image(img_path, width, height)
                btn = Button(bfr, image=image, command=lambda x=item: self.change_page_topay(x))
                btn.image = image
            except FileNotFoundError:
                btn = Button(bfr, text=item[1], command=lambda x=item: self.change_page_topay(x))
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

    def change_page_topay(self, org_data):
        """
        must be threaded
        :param org_data:
        :return:
        """
        print('Not implemented yet {}'.format(org_data))

    def flush(self):
        """
        eliminates types and organization buttons
        :return:
        """
        for btype in self.types:
            btype.destroy()
        for org in self.orgs:
            org.destroy()


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

    def insert(self):
        print('Not implemented yet!')

if __name__ == '__main__':
    t = TkTerminal(1049)
    with t:
        t.mainloop()
