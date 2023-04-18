from tkinter import *
import requests

API_EndPoint1 = "http://127.0.0.1:8000/flight"
API_EndPoint2 = "http://127.0.0.1:8000/add_flight"

root = Tk()
root.option_add("*Font", "impact 20")

designator = StringVar()
departure = StringVar()
arrival = StringVar()
origin = StringVar()
destination = StringVar()

def on_click():
    payload = {
        "designator" : designator.get(),
        "departure" : departure.get(),
        "arrival" : arrival.get(),
        "origin" : origin.get(),
        "destination" : destination.get()
    }
    response = requests.post(API_EndPoint2, params=payload)
    if response.ok:
        Label(root, text="Add Flight :" + str(response.json())).grid(row=15, column=1, padx=5, pady=5)

def on_click2():
    ...

Label(root, text="Designator :").grid(row=0, column=0, padx=10, ipady=5, sticky='E')
Entry(root, textvariable=designator, width=12, justify="left").grid(row=0, column=1, padx=10)
Label(root, text="Departure :").grid(row=1, column=0, padx=10, ipady=5, sticky='E')
Entry(root, textvariable=departure, width=12, justify="left").grid(row=1, column=1, padx=10)
Label(root, text="Arrival :").grid(row=2, column=0, padx=10, ipady=5, sticky='E')
Entry(root, textvariable=arrival, width=12, justify="left").grid(row=2, column=1, padx=10)
Label(root, text="Origin :").grid(row=3, column=0, padx=10, ipady=5, sticky='E')
Entry(root, textvariable=origin, width=12, justify="left").grid(row=3, column=1, padx=10)
Label(root, text="Destination :").grid(row=4, column=0, padx=10, ipady=5, sticky='E')
Entry(root, textvariable=destination, width=12, justify="left").grid(row=4, column=1, padx=10)
Button(root, text="Add Flight", bg="green", command=on_click).grid(row=5, column=0, columnspan=2)
##Button(root, text="Search", bg="green", command=on_click).grid(row=5, column=0, columnspan=2)

root.mainloop()