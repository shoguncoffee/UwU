from . import booking_tk, addFlight_tk, main_tk
from .base import *
from time import sleep
import sv_ttk

if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(True)


class Root(Section, tk.Tk):
    def __init__(self):
        super().__init__()
        
        sv_ttk.set_theme("light")
        ttk.Style().configure(
            'AirportEntry.Treeview', 
            rowheight = 56
        )
        self.geometry("1920x1080")
        self.resizable(False, False)
        self.title("Main")
        # self.iconbitmap("app\\interface\\images\\icon.ico")

        self.username: Optional[str] = None
        self.get_airports()
        self.open(main_tk.MenuPage(self))
        

    # def report_callback_exception(self, exception: Type[Exception], value, traceback):
    #     if exception is ReLoop:
    #         raise exception #.with_traceback(traceback)
    #     else:
    #         super().report_callback_exception(exception, value, traceback)
        
    def get_airports(self):
        data: list[dict[str, str]] = requests.get(url + API_Data1).json()        
        self.airports = [
            body.AirportBody(**attr) for attr in data
        ]
        
sleep(3.5)
Root().mainloop()