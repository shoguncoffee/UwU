from tkinter import *
import tkinter as tk
import requests
import datetime as dt

API_EndPoint1 = "http://127.0.0.1:8000/flight/get_flight"
API_EndPoint2 = "http://127.0.0.1:8000/flight/add_flight"


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Flight Management")
        self.master.geometry("400x450")
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Designator input
        self.designator_label = tk.Label(self, text="Designator:")
        self.designator_label.grid(row=0, column=0, sticky="w")
        self.designator_entry = tk.Entry(self)
        self.designator_entry.grid(row=0, column=1)

        # Departure input
        self.departure_label = tk.Label(self, text="Departure time (HH:MM):")
        self.departure_label.grid(row=1, column=0, sticky="w")
        self.departure_entry = tk.Entry(self)
        self.departure_entry.grid(row=1, column=1)

        # Arrival input
        self.arrival_label = tk.Label(self, text="Arrival time (HH:MM):")
        self.arrival_label.grid(row=2, column=0, sticky="w")
        self.arrival_entry = tk.Entry(self)
        self.arrival_entry.grid(row=2, column=1)

        # Origin airport input
        self.origin_label = tk.Label(self, text="Origin airport:")
        self.origin_label.grid(row=3, column=0, sticky="w")
        self.origin_entry = tk.Entry(self)
        self.origin_entry.grid(row=3, column=1)

        # Destination airport input
        self.destination_label = tk.Label(self, text="Destination airport:")
        self.destination_label.grid(row=4, column=0, sticky="w")
        self.destination_entry = tk.Entry(self)
        self.destination_entry.grid(row=4, column=1)

        # Add flight button
        self.add_flight_button = tk.Button(self, text="Add Flight", command=self.add_flight)
        self.add_flight_button.grid(row=5, column=0, pady=(20, 0), sticky="w")

        # Get flights button
        self.get_flights_button = tk.Button(self, text="Get Flights", command=self.get_flights)
        self.get_flights_button.grid(row=5, column=1, pady=(20, 0), sticky="e")

        # Quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.master.quit)
        self.quit_button.grid(row=6, column=1, pady=(20, 0), sticky="e")

        # Status label
        self.status_label = tk.Label(self, text="", fg="green")
        self.status_label.grid(row=7, columnspan=2, pady=(20, 0))

        # Flights listbox
        self.flights_listbox = tk.Listbox(self)
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