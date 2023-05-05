from tkinter import *
from tkinter.ttk import *
from random import randint
import sv_ttk, ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = Tk()
sv_ttk.set_theme('light')


def t():
    tree.insert('', 'end', text=f'{randint(0, 20)}')
    tree.config(height=1 *randint(10, 20))

b = Button(root, text="Hello", command=t)
b.pack()

tree = Treeview(root, height=1)
tree.place(in_=b, y=30, anchor=NW)
var = BooleanVar()
var2 = BooleanVar()
check = Checkbutton(text="Checkbutton", variable=var)
check2 = Checkbutton(text="Checkbutton", variable=var)
check.pack()
check2.pack()
root.mainloop()