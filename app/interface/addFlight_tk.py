from tkinter import *
import tkinter as tk
import requests
import datetime as dt

API_EndPoint1 = "http://127.0.0.1:8000/flight/get_flight"
API_EndPoint2 = "http://127.0.0.1:8000/flight/add_flight"

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.designator_label = tk.Label(self, text="Designator:")
        self.designator_label.pack()
        self.designator_entry = tk.Entry(self)
        self.designator_entry.pack()

        self.departure_label = tk.Label(self, text="Departure time (HH:MM):")
        self.departure_label.pack()
        self.departure_entry = tk.Entry(self)
        self.departure_entry.pack()

        self.arrival_label = tk.Label(self, text="Arrival time (HH:MM):")
        self.arrival_label.pack()
        self.arrival_entry = tk.Entry(self)
        self.arrival_entry.pack()

        self.origin_label = tk.Label(self, text="Origin airport:")
        self.origin_label.pack()
        self.origin_entry = tk.Entry(self)
        self.origin_entry.pack()

        self.destination_label = tk.Label(self, text="Destination airport:")
        self.destination_label.pack()
        self.destination_entry = tk.Entry(self)
        self.destination_entry.pack()

        self.add_flight_button = tk.Button(self, text="Add Flight", command=self.add_flight)
        self.add_flight_button.pack()

        self.get_flights_button = tk.Button(self, text="Get Flights", command=self.get_flights)
        self.get_flights_button.pack()

        self.quit_button = tk.Button(self, text="Quit", command=self.master.quit)
        self.quit_button.pack()

        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

        self.flights_listbox = tk.Listbox(self)
        self.flights_listbox.pack()

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
            self.status_label.config(text="New flight added")
        else:
            self.status_label.config(text="Error adding flight")

    def get_flights(self):
        response = requests.get(API_EndPoint1)
        if response.status_code == 200:
            flights = response.json()
            self.flights_listbox.delete(0, tk.END)
            for flight in flights:
                flight_str = f"{flight['designator']} - {flight['origin']} to {flight['destination']}, {flight['departure']} to {flight['arrival']}"
                self.flights_listbox.insert(tk.END, flight_str)
            self.status_label.config(text="")
        else:
            self.status_label.config(text="Error getting flights")

root = tk.Tk()
app = Application(master=root)
app.mainloop()