from __future__ import annotations
from tkinter import *
from tkinter.ttk import *
from typing_extensions import Literal
import sv_ttk
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(True)


def check(input, entry):
    if input.lower().strip() in codes:
        entry.state(["!invalid"])
        return True
    
    entry.state(["invalid"])

    
def validate(input: str, char: str, name: str):
    if char.isdigit(): return False
    print(string.get())
    print(f'<{input} {char}>')
    entry = root.nametowidget(name)
    check(input, entry)
    
    result = search(input)
    tree.delete(*tree.get_children())
    for name, code, country in result:
        tree.insert('', END, text=code, values=[f'{country}\n{name}'])
        
    tree.config(
        height = min([5, len(result)])
    )  

    return True


root = Tk()
root.geometry("900x600")
# root.resizable(False, False)
sv_ttk.set_theme('dark')


Label(root, text="Hello World555555555").pack()
Button(root, text="Click Me").pack(padx=50, pady=0)
Button(root, text="Click Me").pack(padx=50, pady=0, ipadx=20, ipady=20)
Button(root, text="Click Me").pack(anchor="se", pady=20)

string = StringVar()
en = Entry(root, 
    width = 20, 
    textvariable=string,
    validate = 'key',
    validatecommand = (root.register(validate), '%P', '%S', '%W'), 
)
en.pack()


Style().configure('MyStyle1.Treeview', rowheight=56)
tree = Treeview(root, 
    columns = '#1', 
    show = ['tree'], 
    selectmode = 'browse',
    style = 'MyStyle1.Treeview',
)
tree.column('#0', width=76)
tree.column('#1', width=280)



def search(input: str):
    print('search')
    return [
        airport for airport in l 
        if input.lower() in '\n'.join(airport).lower()
    ]


def on_focus_out(event):
    print('pe')
    if root.focus_get() is tree:
        tree.after(160, tree.place_forget)

        entry = event.widget
        id = tree.focus()
        item = tree.item(id)
        code = item['text']
        string.set(code)
        
    else:
        tree.place_forget()
    
    
def on_focus_in(event):
    print('re')
    entry = event.widget
    check(entry.get(), entry)
    tree.place(
        in_ = en,
        anchor = NW,
        y = en.winfo_height() + 6,
    )
    tree.config(height=0)
    print('re', 'set = ', tree['height'])

    
def on_return(event):
    print('return')
    entry = event.widget
    root.focus_set()

    children = tree.get_children()
    if len(children) == 1:
        item = tree.item(children[0])
        code = item['text']
        string.set(code)
        
    text = entry.get()
    if check(text, entry):
        string.set(text.upper())
            

en.bind('<FocusOut>', on_focus_out)
en.bind('<FocusIn>', on_focus_in)
en.bind('<Return>', on_return)






l = [
    ('Homad International Airport', 
            'DOH', 'Qatar'),
    ('Suvarnabhumi International Airport',
        'BKK', 'Thailand'),
    ('London City Airport',
        'LCY', 'United Kingdom'),
    ('Don Mueang International Airport', 
        'DMK', 'Thailand'),
    ('Cairo International Airport', 
        'CAI', 'Egypt'),
    ('Miami International Airport',
        'MIA','United States'),
    ('Taiwan Taoyuan International Airport',
        'TPE', 'Taiwan'),
    ('Incheon International Airport',
        'ICN', 'South Korea'),
    ('Hong Kong International Airport',
        'HKG', 'Hong Kong'),
    ('Singapore Changi Airport',
        'SIN', 'Singapore'),
    ('Sydney Kingsford Smith Airport',
        'SYD', 'Australia'),
    ('Hartsfield-Jackson Atlanta Airport',
        'ATL', 'United States'),
]
codes = [
    code.lower() for name, code, country in l
]
   

root.mainloop()