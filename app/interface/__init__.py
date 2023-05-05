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
        self.geometry("900x600")
        # self.resizable(False, False)
        self.title("Main")
        # self.iconbitmap("app\\interface\\images\\icon.ico")

        self.username: Optional[str] = None
        self.get_airports()
        self.get_aircraft()
        
        self.open(main_tk.MenuPage(self))
        
    def get_airports(self):
        data: list[dict[str, str]] = requests.get(f'{URL}{API_Data1}').json()        
        self.airports = [
            body.AirportBody(**attr) for attr in data
        ]

    def get_aircraft(self):
        data: dict[str, dict] = requests.get(f'{URL}/data/aircrafts').json()
        self.aircraft = {
            model: body.AircraftBody(**attr) for model, attr in data.items()
        }
        
    def get_booking(self, id: UUID):
        response = requests.get(f'{URL}/account/{self.username}/{id}')
        return body.BookingInfoBody(**response.json())


while 1:
    try:
        requests.get(f'{URL}/')
    except:
        sleep(1)
    else:
        break
    
Root().mainloop()