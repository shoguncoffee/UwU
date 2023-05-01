from __future__ import annotations
from tkinter import *
from tkinter.ttk import *
from typing import Literal, Optional
import sv_ttk
import ctypes
# from .base import CustomWidget

ctypes.windll.shcore.SetProcessDpiAwareness(True)


class AirportEntry(Entry):    
    def __init__(self, master: Misc, airports: list):
        self.airports = airports
        self.input = StringVar()

        self.suggest_frame = Frame(root)
        self.scroller = Scrollbar(self.suggest_frame)
        self.scroller.pack(side=RIGHT, fill=Y)

        self.suggester = Treeview(
            self.suggest_frame, 
            columns = '#1', 
            show = ['tree'], 
            selectmode = BROWSE,
            style = 'AirportEntry.Treeview',
            yscrollcommand=self.scroller.set,
        )
        self.suggester.column('#0', width=76)
        self.suggester.column('#1', width=280)
        self.suggester.pack()
        
        self.scroller.config(command=self.suggester.yview)        

        
        registar = master.register(self.validate)
        super().__init__(master, 
            # background=background, 
            # class_=class_, 
            # cursor=cursor, 
            # exportselection=exportselection, 
            # font=font, 
            # foreground=foreground, 
            # invalidcommand=invalidcommand, 
            # justify=justify, 
            # name=name, 
            # show=show, 
            # state=state, 
            # style=style, 
            # takefocus=takefocus, 
            width = 20, 
            textvariable = self.input, 
            validate = 'key', 
            validatecommand = (registar, '%P', '%S'), 
            # xscrollcommand=xscrollcommand
        )
        self.bind('<FocusOut>', self.on_focus_out)
        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<Return>', self.on_return)

    @property
    def string(self):
        return self.clean(self.input.get())

    @staticmethod
    def clean(string: str):
        return string.lower().strip()
        
    def check(self, string: Optional[str] = None):
        string = string or self.string
        
        for name, code, country in self.airports:
            if string == code.lower():
                self.state(["!invalid"])
                return True
        
        self.state(["invalid"])

    def validate(self, input: str, char: str = ''):
        if char.isdigit(): return False

        input = self.clean(input)
        self.check(input)
        result = self.search(input)

        self.suggester.delete(
            *self.suggester.get_children()
        )
        for name, code, country in result:
            self.suggester.insert(
                '', END, 
                text = code, 
                values = [f'{country}\n{name}']
            )
        self.suggester.config(
            height = min([5, len(result)])
        )  
        
        return True

    def on_return(self, event):
        self.master.focus_set()
        suggestion = self.suggester.get_children()

        if self.check():
            self.input.set(self.string.upper())
            
        elif len(suggestion) == 1:
            item = self.suggester.item(suggestion[0])
            self.input.set(item['text'])
            self.state(["!invalid"])
            
    def on_focus_in(self, event):
        self.check()
        self.suggest_frame.place(
            in_ = self,
            anchor = NW,
            y = self.winfo_height() + 6,
        )
        self.validate(self.string)

    def on_focus_out(self, event):
        if self.master.focus_get() is self.suggester:
            self.suggest_frame.after(
                ms = 160, 
                func = self.suggest_frame.place_forget
            )
            item_id = self.suggester.focus()
            item = self.suggester.item(item_id)
            self.input.set(item['text'])
            self.state(["!invalid"])
            
        else:
            self.suggest_frame.place_forget()
  
    def search(self, input: str):
        return [
            airport for airport in self.airports
            if input in '\n'.join(airport).lower()
        ]


if __name__ == '__main__':
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
    
    root = Tk()
    sv_ttk.set_theme('dark')
    root.geometry("900x600")
    root.resizable(False, False)
    Style().configure(
        'AirportEntry.Treeview', 
        rowheight = 56
    )
    f = Frame(root)
    Button().pack()
    AirportEntry(f, l).pack()
    f.pack()
    
    root.mainloop()