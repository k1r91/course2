"""
This module is used to manage organization and transactions database
"""
import sql
from tkinter import *
from misc import TableGrid
import misc_reports


# main window
root = Tk()
root.resizable(False, False)
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
w = 900
h = 500
table = TableGrid(root, titles=[], header='')
sql.update_terminals(table)
root.geometry('{}x{}+{}+{}'.format(w, h, ws//4, hs//6))
root.title('Payment system administration')
# top main menu
rootm = Menu(root)
select_tm = Menu(rootm)
reports_om = Menu(rootm)
select_tm.add_command(label='Terminals', command=lambda x=table: sql.update_terminals(table))
# select_tm.add_command(label='Transactions', command=lambda x=table: sql.update_trans(table))
select_om = Menu(rootm)
select_om.add_command(label='Organizations', command=lambda x=table: sql.update_organizations(table))
select_om.add_command(label='Organization types', command=lambda x=table: sql.update_types(table))
select_om.add_command(label='Collectors', command=lambda x=table: sql.update_collectors(table))
reports_om.add_command(label='Transactions', command=lambda x=root: misc_reports.report_transactions(root))
reports_om.add_command(label='One organization', command=lambda x=root:misc_reports.report_one_org(root))
reports_om.add_command(label='All organizations', command=lambda x=root:misc_reports.report_all_org(root))
rootm.add_cascade(label='Terminal DB', menu=select_tm)
rootm.add_cascade(label='Organizations DB', menu=select_om)
rootm.add_cascade(label='Reports', menu=reports_om)
root.config(menu=rootm)
# end menu
mainloop()