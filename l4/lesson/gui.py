from tkinter import *
from tkinter.messagebox import *
import os


def not_implemented():
    print('Not implemented yet!')
    showerror('Not implemented yet!')

main_window = Tk()
main_window.minsize(400, 400)
main_window.resizable(width=False, height=False)
main_window.title('Star administrator')
main_window.iconbitmap(os.path.join(os.getcwd(), 'test.ico'))
btn = Button(main_window, text='Create DB', command=not_implemented)
btn.pack(side=BOTTOM)
mainloop()
