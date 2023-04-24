from tkinter import *
import tkinter as tk
import requests
import datetime as dt

API_EndPoint1 = "http://127.0.0.1:8000/flight/get_flight"
API_EndPoint2 = "http://127.0.0.1:8000/flight/add_flight"


class Application:
    def __init__(self, master):
        self.master = master
        master.title("Flight Management")
        master.geometry("400x450")
        master.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Designator input
        self.designator_label = Label(master, text="Designator:")
        self.designator_label.grid(row=0, column=0, sticky="w")
        self.designator_entry = Entry(master)
        self.designator_entry.grid(row=0, column=1)

        # Departure input
        self.departure_label = Label(master, text="Departure time (HH:MM):")
        self.departure_label.grid(row=1, column=0, sticky="w")
        self.departure_entry = Entry(master)
        self.departure_entry.grid(row=1, column=1)

        # Arrival input
        self.arrival_label = Label(master, text="Arrival time (HH:MM):")
        self.arrival_label.grid(row=2, column=0, sticky="w")
        self.arrival_entry = Entry(master)
        self.arrival_entry.grid(row=2, column=1)

        # Origin airport input
        self.origin_label = Label(master, text="Origin airport:")
        self.origin_label.grid(row=3, column=0, sticky="w")
        self.origin_entry = Entry(master)
        self.origin_entry.grid(row=3, column=1)

        # Destination airport input
        self.destination_label = Label(master, text="Destination airport:")
        self.destination_label.grid(row=4, column=0, sticky="w")
        self.destination_entry = Entry(master)
        self.destination_entry.grid(row=4, column=1)

        # Add flight button
        self.add_flight_button = Button(master, text="Add Flight", command=self.add_flight)
        self.add_flight_button.grid(row=5, column=0, pady=(20, 0), sticky="w")

        # Get flights button
        self.get_flights_button = Button(master, text="Get Flights", command=self.get_flights)
        self.get_flights_button.grid(row=5, column=1, pady=(20, 0), sticky="e")

        # Quit button
        self.quit_button = Button(master, text="Quit", command=self.master.quit)
        self.quit_button.grid(row=6, column=1, pady=(20, 0), sticky="e")

        # Status label
        self.status_label = Label(master, text="", fg="green")
        self.status_label.grid(row=7, columnspan=2, pady=(20, 0))

        # Flights listbox
        self.flights_listbox = Listbox(master)
        self.flights_listbox.grid(row=8, columnspan=2, padx=(10, 0), pady=(20, 0))

    def add_flight(self):
        designator = self.designator_entry.get()
        departure_str = self.departure_entry.get()
        arrival_str = self.arrival_entry.get()
        origin = self.origin_entry.get()
        destination = self.destination_entry.get()

        try:
            departure = dt.datetime.strptime(departure_str, "%H:%M").time()
            arrival = dt.datetime.strptime(arrival_str, "%H:%M").time()
        except ValueError:
            self.status_label.config(text="Invalid time format")
            return

        response = requests.post(API_EndPoint2, params={
            "designator": designator,
            "departure": str(departure),
            "arrival": str(arrival),
            "origin": origin,
            "destination": destination
        })
        if response.status_code == 200:
            self.status_label.config(text="New flight added", fg="green")
        else:
            self.status_label.config(text="Error adding flight", fg="red")

    def get_flights(self):
        response = requests.get(API_EndPoint1)
        if response.status_code == 200:
            flights = response.json()
            self.flights_listbox.delete(0, END)
            for flight in flights:
                flight_str = f"{flight['designator']} - {flight['origin']} to {flight['destination']}, {flight['departure']} to {flight['arrival']}"
                self.flights_listbox.insert(END, flight_str)
            self.status_label.config(text="")
        else:
            self.status_label.config(text="Error getting flights")

master = Tk()
app = Application(master)
master.mainloop()