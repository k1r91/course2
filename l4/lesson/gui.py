from tkinter import *
from tkinter.messagebox import *
import os

class TableGrid(Frame):
    def __init__(self, parent=None, titles=None, rows=0, *args):
        super().__init__(parent)

        for index, title in enumerate(titles):
            Label(self, text=title).grid(row=0, column=index)

        for i in range(1, rows+1):
            for j in range(index+1):
                Entry(self).grid(row=i, column=j)
        self.pack()


def not_implemented(x=13):
    print('Not implemented yet!', x)
    # showerror('Not implemented yet!')


def not_implemented_2(event):
    print('Not implemented_2 yet!', event)

main_window = Tk()
main_window.minsize(400, 400)
main_window.resizable(width=False, height=False)
main_window.title('Star administrator')
# fr1 = Frame(main_window)
# fr1.pack(side=LEFT)
# label = Label(fr1, text='This is first frame')
# label.pack()
fr2 = Frame(main_window)
fr3 = Frame(main_window)
fr3.pack(side=RIGHT)
for i in range(5):
    btn = Button(fr2, text='Create DB', command=lambda x=i: not_implemented(x))
    btn.grid(row=0, column=i)
fr2.pack(side=BOTTOM)

# left, wheel, right  mouse buttons accordingly
main_window.bind('<Button-1>', not_implemented_2)
main_window.bind('<Button-2>', not_implemented_2)
main_window.bind('<Button-3>', not_implemented_2)
main_menu = Menu(main_window)
file_menu = Menu(main_menu )
file_menu.add_command(label='Terminals', command=not_implemented)
main_menu.add_cascade(label='Database', menu=file_menu)
main_window.config(menu=main_menu)
grid = TableGrid(main_window, ('Id', 'Name', 'Description'), 3)
mainloop()
