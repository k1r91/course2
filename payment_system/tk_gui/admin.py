"""
This module is used to manage organization and transactions database
"""
import os
import sql
from tkinter import *
from misc import TableGrid


# main window
root = Tk()
root.resizable(False, False)
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
w = 900
h = 500
table = TableGrid(root, titles=[], header='')
sql.update_terminals(table)
root.geometry('{}x{}+{}+{}'.format(w, h, ws//3, hs//4))
root.title('Payment system administration')
# top main menu
rootm = Menu(root)
select_tm = Menu(rootm)
select_tm.add_command(label='Terminals', command=lambda x=table: sql.update_terminals(table))
# select_tm.add_command(label='Transactions', command=lambda x=table: sql.update_trans(table))
select_om = Menu(rootm)
select_om.add_command(label='Organizations', command=lambda x=table: sql.update_organizations(table))
select_om.add_command(label='Organization types', command=lambda x=table: sql.update_types(table))
select_om.add_command(label='Collectors', command=lambda x=table: sql.update_collectors(table))
rootm.add_cascade(label='Terminal DB', menu=select_tm)
rootm.add_cascade(label='Organizations DB', menu=select_om)
root.config(menu=rootm)
# end menu
mainloop()