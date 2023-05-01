from tkinter import *
from tkinter.ttk import *
from datetime import *
import sv_ttk 

root = Tk()
sv_ttk.set_theme('light')

top_frame = Frame(root)
top_frame.pack(side=TOP)
        
label1 = Label(top_frame,
    text="View Booking"                   
)
label1.grid(row=0, column=0)

data = [
    {
        'status': 'Confirmed',
        'datetime': datetime.now(),
        'pax': [('Adult', 1), ('Child', 2)],
        'trip': [
            ('SYD', 'MEL', date(2020, 2, 1), date(2020, 6, 1)),
            ('MEL', 'SYD', date(2020, 1, 3), date(2020, 1, 2)),
        ]
    }, {
        'status': 'Not Paid',
        'datetime': datetime.now(),
        'pax': [('Adult',2)],
        'trip': [
            ('SYD', 'MEL', date(2020, 2, 1), date(2020, 6, 1)),
            ('MEL', 'SYD', date(2020, 7, 3), date(2020, 1, 2)),
        ]
    }, {
        'status': 'UnConfirmed',
        'datetime': datetime.now(),
        'pax': [('Adult', 1), ('Child', 2)],
        'trip': [
            ('SYD', 'MEL', date(2020, 3, 1), date(2020, 9, 1)),
            ('MEL', 'SYD', date(2020, 5, 3), date(2020, 6, 2)),
        ]
    }, {
        'status': 'XXX Paid',
        'datetime': datetime.now(),
        'pax': [('Adult',2)],
        'trip': [
            ('SYD', 'MEL', date(2020, 2, 1), date(2020, 4, 1)),
            ('MEL', 'SYD', date(2020, 1, 3), date(2020, 3, 2)),
        ]
    },
]



for booking in data:
    button = LabelFrame(root, text=f'{booking["datetime"]: %d %b %Y %H:%M}')
    button.pack()
    
    button.booking = booking # type: ignore
    button.bind("<Button-1>", lambda event: print(123))

    Label(button, 
        text=booking['status']
    ).pack(side=LEFT)
    
    Label(button, 
        text=' '.join(f'{number} {type}' for type, number in booking['pax'])
    ).pack(side=LEFT)

    itinerary = Frame(button, width=10)
    itinerary.pack(side=RIGHT)
    
    for origin, destination, departure, arrival in booking['trip']:
        tab = Frame(itinerary)
        tab.pack()
        
        Label(tab, 
            text=f'{origin} -> {destination}'
        ).grid(column=0)
        
        Label(tab, 
            text=f'{departure: %a, %d %b %Y} - {arrival: %a, %d %b %Y}'
        ).grid(column=1)


root.mainloop()