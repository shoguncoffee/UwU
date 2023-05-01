from __future__ import annotations
from app.base import *

import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

from app.utils import search
import app.src as src
import app.api.body_template as body
import requests

if TYPE_CHECKING:
    from . import Root


url = 'http://127.0.0.1:8000'

API_EndPoint1 = "/account/createAccount"
API_EndPoint2 = "/account/login"
API_Data1 = "/data/airports"
API_Endpoint3 = "/search/one-way"


class Reloop(Exception):
    pass


class Section(tk.Misc):
    """
        - container for `Page`
        - showing one page at the time
    """
    master: Section
    
    def __init__(self, *args, **kwargs):
        self.layers: list[StaticPage] = []
        self.index = -1
        super().__init__(*args, **kwargs)

    @property
    def current_page(self):
        return self.layers[self.index]

    def forget_current(self):
        if len(self.winfo_children()) > 1:
            self.current_page.pack_forget()

    def clear(self, *exception: CustomWidget):
        self.layers = [
            page for page in self.layers if page not in exception
        ]
        for child in self.winfo_children():
            if child not in exception:
                child.destroy()

    @overload
    def open(self, page: P) -> P: ...
    @overload
    def open(self, page: StaticPage) -> StaticPage: ...
    def open(self, page: StaticPage):
        self.clear(page)
        return page.pack()
    
    @overload
    def stack(self, page: P) -> P: ...
    @overload
    def stack(self, page: StaticPage) -> StaticPage: ...
    def stack(self, page: StaticPage):
        print('STACK', self, self.index)
        print(self.layers)
        print(self.children)
        self.forget_current()
        layer = page.pack()
        self.layers.append(layer)
        self.index += 1
        return layer

    # def flip(self, key: int | StaticPage):
    #     target = key if isinstance(key, StaticPage) else self.layers[key]
    #     self.forget_current()
    #     target.predefine()
    #     target.pack()
    
    def backwawrd(self):
        self.current_page.destroy()
        del self.layers[self.index]
        self.index -= 1
        self.current_page.predefine()
        self.current_page.pack()
        
        raise Reloop
    
    def procedure(self): ...
    def loop(self):
        while 1:
            try: 
                self.procedure()
                break
            except Reloop: 
                continue
    
    @overload
    def peek(self, page: P) -> P: ...
    @overload
    def peek(self, page: StaticPage) -> StaticPage: ...
    def peek(self, page: StaticPage):
        for layer in self.layers:
            if type(layer) == type(page):
                page.destroy()
                return layer
            
        return self.stack(page)

class CustomWidget(ttk.Widget):
    def _clear_kwargs(self, kwargs: dict[str, Any]):
        return {
            n: v for n, v in kwargs.items()
            if n not in ('self', 'kw', 'kwargs') and v is not ...
        }
    
    def grid(self, 
        cnf: Mapping[str, Any] | None = ..., *, 
        column: int = ..., 
        columnspan: int = ..., 
        row: int = ..., 
        rowspan: int = ..., 
        ipadx: tk._ScreenUnits = ..., 
        ipady: tk._ScreenUnits = ..., 
        padx: tk._ScreenUnits | tuple[tk._ScreenUnits, tk._ScreenUnits] = ..., 
        pady: tk._ScreenUnits | tuple[tk._ScreenUnits, tk._ScreenUnits] = ..., 
        sticky: str = ..., 
        in_: tk.Misc = ..., 
        **kw: Any
    ):
        self.grid_configure(**kw, 
            **self._clear_kwargs(locals())
        )
        return self
    
    def pack(self, 
        cnf: Mapping[str, Any] | None = ..., *, 
        after: tk.Misc = ..., 
        anchor: tk._Anchor = ..., 
        before: tk.Misc = ..., 
        expand: int = ..., 
        fill: Literal['none', 'x', 'y', 'both'] = ..., 
        side: Literal['left', 'right', 'top', 'bottom'] = ..., 
        ipadx: tk._ScreenUnits = ..., 
        ipady: tk._ScreenUnits = ..., 
        padx: tk._ScreenUnits | tuple[tk._ScreenUnits, tk._ScreenUnits] = ..., 
        pady: tk._ScreenUnits | tuple[tk._ScreenUnits, tk._ScreenUnits] = ..., 
        in_: tk.Misc = ..., 
        **kw: Any
    ):
        self.pack_configure(**kw, 
            **self._clear_kwargs(locals())
        )
        return self

    def place(self, 
        cnf: Mapping[str, Any] | None = ..., *, 
        anchor: tk._Anchor = ..., 
        bordermode: Literal['inside', 'outside', 'ignore'] = ..., 
        width: tk._ScreenUnits = ..., 
        height: tk._ScreenUnits = ..., 
        x: tk._ScreenUnits = ..., 
        y: tk._ScreenUnits = ..., 
        relheight: str | float = ..., 
        relwidth: str | float = ..., 
        relx: str | float = ..., 
        rely: str | float = ..., 
        in_: tk.Misc = ..., 
        **kw: Any
    ):
        self.place_configure(**kw, 
            **self._clear_kwargs(locals())
        )
        return self


class StaticPage(CustomWidget, ttk.Frame):
    """
        page with no additional parameter and not have return value
    """
    master: Section

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.predefine()
        self.add_widgets()

    @property
    def root(self) -> Root:
        # or tk._get_default_root()
        return self._root() # type: ignore

    def jump(self, page: Type[StaticPage]):
        root = self.root
        root.clear()
        root.open(page(root))
    
    def predefine(self): ...
    def add_widgets(self): ...
    def submit(self): ...


class Page(StaticPage):
    """
        page with parameter and return value
    """
    def predefine(self): 
        self.waiter = tk.IntVar(self, 0)

    def next(self): 
        self.waiter.set(1)

    def back(self):
        self.waiter.set(2)
    
    def returned(self): 
        if self.waiter.get() == 0:
            self.wait_variable(self.waiter)
            if self.waiter.get() == 2:
                self.master.backwawrd()


class SubSection(Section, Page):
    def predefine(self): 
        self.waiter = tk.IntVar(self, 1)
        
    def pack(self):
        super().pack()
        self.loop()
        return self
    

P = TypeVar('P', bound=Page)

class Label(CustomWidget, ttk.Label): ...
class Radiobutton(CustomWidget, ttk.Radiobutton): ...
class Button(CustomWidget, ttk.Button): ...
class Entry(CustomWidget, ttk.Entry): ...
class Combobox(CustomWidget, ttk.Combobox): ...
class Checkbutton(CustomWidget, ttk.Checkbutton): ...
class Scrollbar(CustomWidget, ttk.Scrollbar): ...
class Frame(CustomWidget, ttk.Frame): ...
class Treeview(CustomWidget, ttk.Treeview): ...
class Spinbox(CustomWidget, ttk.Spinbox): ...
class LabelFrame(CustomWidget, ttk.Labelframe): ...

class AirportEntry(CustomWidget, ttk.Entry): 
    master: Page
      
    def __init__(self, master: Page):
        self.airports = master.root.airports
        self.input = tk.StringVar()

        # non-parent -> root
        self.suggest_frame = Frame()
        self.scroller = Scrollbar(self.suggest_frame).pack(
            side=RIGHT, fill=Y
        )
        self.suggester = Treeview(
            self.suggest_frame, 
            columns = '#1', 
            show = ['tree'], 
            selectmode = BROWSE,
            style = 'AirportEntry.Treeview',
            yscrollcommand = self.scroller.set,
        ).pack()
        self.suggester.column('#0', width=78)
        self.suggester.column('#1', width=260)

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
        
        for airport in self.airports:
            if string == airport.location_code.lower():
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
        for airport in result:
            self.suggester.insert(
                '', END, 
                text = airport.location_code, 
                values = ['\n'.join(
                    [airport.country, airport.name]
                )]
            )
        self.suggester.config(
            height = min([6, len(result)])
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
        ms = 1
        if self.master.focus_get() is self.suggester:
            ms = 160
            item_id = self.suggester.focus()
            item = self.suggester.item(item_id)
            self.input.set(item['text'])
            self.state(["!invalid"])
            
        self.suggest_frame.after(ms, 
            self.suggest_frame.place_forget
        )
  
    def search(self, key: str):
        return [
            *search.multi_opt(
                'location_code', 'name', 'country', 
                query=key, pool=self.airports,
                score_cutoff=80
            )
        ]
        
    def destroy(self):
        self.suggest_frame.destroy()
        super().destroy()