import os
import sql
from tkinter import *
from PIL import Image, ImageTk


class TableGrid(Frame):

    buttons_img = os.path.join(os.path.dirname(__file__), 'gif')

    def __init__(self, parent=None, header=None, titles=None, rows=0, *args, **kwargs):
        h = kwargs.get('h')
        w = kwargs.get('w')
        self.parent = parent
        super().__init__(parent, width=w, height=h)
        self.w = w
        self.h = h
        self.tablename = None
        self._create_scroll()
        self.header = Label(self.frame, text=header, font=("Courier", 32))
        if titles:
            self.header.grid(row=0, columnspan=len(titles))
        self.update_titles(titles)
        self.rebuild(rows, len(titles))
        self.pack(side=LEFT, fill=BOTH, expand=True)

    def rebuild(self, rows=0, cols=0):
        self.vars=[]
        self.cells=[]
        self.buttons = []
        for row in range(2, rows+2):
            self.vars.append([])
            for col in range(cols):
                var = StringVar()
                self.vars[row-2].append(var)
                cell = Entry(self.frame, textvariable=var)
                cell.config(state=DISABLED)
                cell.grid(row=row, column=col)
                self.cells.append(cell)
            b = MagicButtons(self.frame, row_id=row-2, table=self)
            b.grid(row=row, column=len(self.titles))
            self.buttons.append(b)

    def _create_scroll(self):
        ''' Обёртка для создания прокрутки внутри Frame.
                Дело в том, что элемент Scrollbar можно привязать
                только к "прокручиваемым" виджетам (Canvas, Listbox, Text),
                в то время как наша "таблица" создана на основе Frame.

                Чтобы решить эту задачу, нужно внутри нашего фрейма создать дополнительные
                виджеты: Canvas и Frame.
                '''
        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas)

        # Сам по себе Scrollbar - хитрый...
        # Нужно сделать связь не только в Scrollbar, но и в привязанном Canvas'е:
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_h = Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.configure(xscrollcommand=self.scrollbar_h.set)

        # "Упаковываем" Canvas и Scrollbar - один слева, другой справа:
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar_h.pack(side=BOTTOM, fill="x")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        # Отрисовываем новый фрейм на Canvas'е
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # При событии <Configure> будет происходить перерисовывание Canvas'а.
        # Событие <Configure> - базовое событие для виджетов;
        # происходит, когда виджет меняет свой размер или местоположение.
        self.frame.bind("<Configure>", lambda e: self._scroll(e))

    def _scroll(self, e):
        """
            Перерисовка канвы и области прокрутки
        """
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.config(width=self.w, height=self.h)

    def update_titles(self, titles):
        self.titles = []
        for index, title in enumerate(titles):
            label = Label(self.frame, text=title)
            label.grid(row=1, column=index)
            self.titles.append(label)


    def table_update(self, data, titles=None, header=None, tablename=None):
        self.tablename = tablename
        for b in self.buttons:
            b.destroy()
        for cell in self.cells:
            cell.destroy()
        if header is not None:
            self.header.config(text=header)
            self.header.grid(row=0, columnspan=len(titles))
        if titles is not None:
            for t in self.titles:
                t.destroy()
            self.update_titles(titles)
        self.rebuild(len(data), len(data[0]))
        for i, record in enumerate(data):
            for j, item in enumerate(record):
                self.vars[i][j].set(item)


class MagicButtons(Frame):
    img_dir = os.path.join(os.path.dirname(__file__), 'gif')

    def __init__(self, parent=None, row_id=None, table=None):
        super().__init__(parent)
        self.state = 0  # disabled
        self.table = table
        self.btn_update = \
            self.pack_button(os.path.join(self.img_dir, 'update.gif'), lambda x=row_id: self.row_update(x))
        self.btn_delete = \
            self.pack_button(os.path.join(self.img_dir, 'delete.gif'), lambda x=row_id: self.row_delete(x))

    @staticmethod
    def get_image(path_image):
        img = Image.open(path_image)
        img = img.resize((17, 17), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        return img

    def pack_button(self, path_image, command):
        image = self.get_image(path_image)
        btn = Button(self, image=image, width=17, height=17)
        btn.img = image
        btn.pack(side=LEFT)
        btn.config(command=command)
        return btn

    def row_update(self, id):
        cell_st_index = (len(self.table.titles) - 1) * id
        cell_end_index = cell_st_index + len(self.table.titles) - 1
        if self.state:
            self.state = 0  # disabled
            values = [x.get() for x in self.table.vars[id]]
            for cell in self.table.cells[cell_st_index: cell_end_index]:
                cell.config(state=DISABLED)
            sql.perform_query(self.table.tablename, values)
            image = self.get_image(os.path.join(self.img_dir, 'update.gif'))
            self.btn_update.config(image=image)
            self.btn_update.img = image
        else:
            self.state = 1  # enabled
            image = self.get_image(os.path.join(self.img_dir, 'apply.gif'))
            self.btn_update.config(image=image)
            self.btn_update.img = image
            for cell in self.table.cells[cell_st_index: cell_end_index]:
                cell.config(state=NORMAL)

    def row_delete(self, id):
        print('Deleting {} row from table {}'.format(id, self.table.tablename))