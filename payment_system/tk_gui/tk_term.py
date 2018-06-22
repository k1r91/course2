import sys
sys.path.append('..')
from terminal import Terminal, TerminalException
from tkinter import *


class TkTerminal(Terminal):

    def __init__(self, _id):
        super().__init__(_id)
        self.root = Tk()
        self.root.title('Terminal № {}'.format(self._id))
        self.hs = self.root.winfo_screenheight()//5
        self.ws = self.root.winfo_screenwidth()//5
        self.h = int(self.root.winfo_screenheight()*2/3)
        self.w = int(self.root.winfo_screenwidth()*2/3)
        self.root.geometry('{}x{}+{}+{}'.format(self.w, self.h, self.ws, self.hs))
        print(self.errors)

    def mainloop(self):
        self.root.mainloop()


class Display(Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

if __name__ == '__main__':
    t = TkTerminal(1049)
    t.mainloop()