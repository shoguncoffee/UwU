import tkinter as tk
from tkinter import ttk, messagebox, BooleanVar
import requests

API_EndPoint1 = "http://127.0.0.1:8000/account/createAccount"
API_EndPoint2 = "http://127.0.0.1:8000/account/login"

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Main")
        self.master.geometry("500x300")

        # Create header
        self.username_label = tk.Label(master, text="SHOGUNUS Airline", font="Bold 20")
        self.username_label.pack()

        # Create button to go to login window
        self.login_button = tk.Button(master, text="Login", command=self.open_login)
        self.login_button.pack()

        # Create button to go to register window
        self.register_button = tk.Button(master, text="Register", command=self.open_register)
        self.register_button.pack()

        # Create button to go to search window
        self.search_button = tk.Button(master, text="Search Flight", command=self.open_search)
        self.search_button.pack()

    def open_login(self):
        # Close the window
        self.master.destroy()
        # Open the login window
        root = tk.Tk()
        login_window = LoginWindow(root)
        root.mainloop()

    def open_register(self):
        # Close the window
        self.master.destroy()
        # Open the registration window
        root = tk.Tk()
        register_window = RegisterWindow(root)
        root.mainloop()

    def open_search(self):
        # Close the window
        self.master.destroy()
        # Open the search window
        root = tk.Tk()
        search_window = SearchFlightWindow(root)
        root.mainloop()

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        self.master.geometry("300x200")

        # Create labels and entries for user input
        self.username_label = tk.Label(master, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        # Create a button to submit the form
        self.submit_button = tk.Button(master, text="Login", command=self.submit_form)
        self.submit_button.pack()

        # Create a button to go to the registration window
        self.register_button = tk.Button(master, text="Register", command=self.open_registration)
        self.register_button.pack()

        # Create a button to go to the main window
        self.back_button = tk.Button(master, text="Back", command=self.open_main)
        self.back_button.pack()

        # Create a label for the response message
        self.response_label = tk.Label(master, text="")
        self.response_label.pack()

    def submit_form(self):
        # Get input values from the user
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Send a POST request to the server to login
        url = API_EndPoint2
        data = {"username": username, "password": password}
        response = requests.post(url, params=data)

        # Show the response message to the user
        if response.status_code == 200:
            self.response_label.config(text="Login successful!", fg="green")
        else:
            self.response_label.config(text="Error: " + response.json()["detail"], fg="red")

    def open_registration(self):
        # Close the window
        self.master.destroy()
        # Open the registration window
        root = tk.Tk()
        registration_window = RegisterWindow(root)
        root.mainloop()

    def open_main(self):
        # Close the window
        self.master.destroy()
        # Open the Main window
        root = tk.Tk()
        main_window = MainWindow(root)
        root.mainloop()

class RegisterWindow:
    def __init__(self, master):
        self.master = master
        master.title("Register")
        self.master.geometry("300x250")

        # Create labels and entries for user input
        self.username_label = tk.Label(master, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        self.email_label = tk.Label(master, text="Email")
        self.email_label.pack()
        self.email_entry = tk.Entry(master)
        self.email_entry.pack()

        self.phone_label = tk.Label(master, text="Phone")
        self.phone_label.pack()
        self.phone_entry = tk.Entry(master)
        self.phone_entry.pack()

        # Create a button to submit the form
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_form)
        self.submit_button.pack()

        # Create a button to go back to the login window
        self.login_button = tk.Button(master, text="Go to Login", command=self.go_to_login)
        self.login_button.pack()

        # Create a label for the response message
        self.response_label = tk.Label(master, text="")
        self.response_label.pack()

    def submit_form(self):
        # Get input values from the user
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        # Send a POST request to the server to create a new account
        data = {"username": username, "password": password, "email": email, "phone": phone}
        response = requests.post(API_EndPoint1, params=data)

        # Show the response message to the user
        if response.status_code == 200:
            self.response_label.config(text="New account created!", fg="green")
        else:
            self.response_label.config(text="Error: " + response.json()["detail"], fg="red")

        self.response_label.pack()

    def go_to_login(self):
        # Close the window
        self.master.destroy()
        # Open the login window
        root = tk.Tk()
        login_window = LoginWindow(root)
        root.mainloop()

API_Data1 = "http://127.0.0.1:8000/data/airports"
API_Endpoint3 = "http://127.0.0.1:8000/search/one-way"
class SearchFlightWindow:
    def __init__(self, master):
        self.master = master
        master.title("Search Flight")
        self.airports = requests.get(API_Data1).json()
        self.airports_code = [airport["location_code"] for airport in self.airports]
        
        self.from_label = tk.Label(master, text="From").grid(row=0, column=0)
        self.from_combobox = ttk.Combobox(master,height=5, width=15, values=self.airports_code)
        self.from_combobox.grid(row=1, column=0)

        self.to_label = tk.Label(master, text="To").grid(row=0, column=1)
        self.to_combobox = ttk.Combobox(master,height=5, width=15, values=self.airports_code)
        self.to_combobox.grid(row=1, column=1)

        self.trip_label = tk.Label(master, text="Trip").grid(row=0, column=2)
        self.trip_combobox = ttk.Combobox(master,height=5,width=15,values=["One Way"])
        self.trip_combobox.grid(row=1,column=2)

        self.departure_date_label = tk.Label(master, text="Departure Date").grid(row=0, column=3)

        self.departure_day_combobox = ttk.Combobox(master,height=5,width=15,values=list(range(1, 32)))
        self.departure_day_combobox.grid(row=1,column=3)
        self.departure_day_combobox.insert(0, "Day")

        self.departure_month_combobox = ttk.Combobox(master,height=5,width=15,values=list(range(1, 13)))
        self.departure_month_combobox.grid(row=2,column=3)
        self.departure_month_combobox.insert(0, "Month")

        self.departure_year_combobox = ttk.Combobox(master,height=5,width=15,values=['2023'])
        self.departure_year_combobox.grid(row=3,column=3)
        self.departure_year_combobox.insert(0, "Year")

        self.passenger_label = tk.Label(master, text="Passenger").grid(row=0, column=5)

        self.passenger_adult_combobox = ttk.Combobox(master,height=5,width=15,values=["1","2","3","4","5","6","7","8","9"])
        self.passenger_adult_combobox.grid(row=1,column=5)
        self.passenger_adult_combobox.insert(0, "Adult")

        self.passenger_children_combobox = ttk.Combobox(master,height=5,width=15,values=["0","1","2","3","4","5","6","7","8","9"])
        self.passenger_children_combobox.grid(row=2,column=5)
        self.passenger_children_combobox.insert(0, "Children")

        self.passenger_infant_combobox = ttk.Combobox(master,height=5,width=15,values=["0","1","2","3","4","5","6","7","8","9"])
        self.passenger_infant_combobox.grid(row=3,column=5)
        self.passenger_infant_combobox.insert(0, "Infant")

        self.search_button = tk.Button(master, text="Search", command=self.search_flight).grid(row=5, column=2)

        self.back_button = tk.Button(master, text="Back to Main", command=self.open_main).grid(row=6, column=2)

    def search_flight(self):
        origin = self.from_combobox.get()
        destination = self.to_combobox.get()
        trip = self.trip_combobox.get()
        departure_day = self.departure_day_combobox.get()
        departure_month = self.departure_month_combobox.get()
        departure_year = self.departure_year_combobox.get()
        passenger_adult = self.passenger_adult_combobox.get()
        passenger_children = self.passenger_children_combobox.get()
        passenger_infant = self.passenger_infant_combobox.get()

        if origin=="" or destination=="" or trip=="" or departure_day=="" or departure_month=="" or departure_year=="" or passenger_adult=="" or passenger_children=="" or passenger_infant=="":
            messagebox.showerror("Error","Please fill all the fields")
        else:
            if origin == destination:
                messagebox.showerror("Error","Origin and Destination cannot be same")
            else:
                data = {
                    "origin": origin,
                    "destination": destination,
                    "date": departure_year + "-" + departure_month + "-" + departure_day,
                    "adult": passenger_adult,
                    "child": passenger_children,
                    "infant": passenger_infant,
                }

                response = requests.get(url = API_Endpoint3, params=data)
                
                self.master.destroy()
                # Open the Main window
                root = tk.Tk()
                search_flight_result_window = SearchFlightResultWindow(root, response)
                root.mainloop()

    def open_main(self):
        # Close the window
        self.master.destroy()
        # Open the Main window
        root = tk.Tk()
        main_window = MainWindow(root)
        root.mainloop()        

class SearchFlightResultWindow:
    def __init__(self, master, response: requests.Response):
        self.master = master
        master.title("Search Flight Result")

        self.origin_label = tk.Label(master, text="Origin").grid(row=0, column=0)
        self.destination_label = tk.Label(master, text="Destination").grid(row=0, column=1)
        self.departure_label = tk.Label(master, text="Departure").grid(row=0, column=2)
        self.arrival_label = tk.Label(master, text="Arrival").grid(row=0, column=3)
        self.economy_label = tk.Label(master, text="Economy").grid(row=0, column=5)
        self.business_label = tk.Label(master, text="Business").grid(row=0, column=6)
        self.first_label = tk.Label(master, text="First").grid(row=0, column=7)
        
        self.back_button = tk.Button(master, text="SearchFlight", command=self.open_search_flight).grid(row=0, column=8)
        self.book_button = tk.Button(master, text="Book", command=self.open_passenger_details).grid(row=0, column=9)


        print(response.text)
        result = response.json()
        for n, itinerary in enumerate(result) :
            first_flight = itinerary['flights'][0]
            last_flight = itinerary['flights'][-1]

            departure = first_flight['departure']
            arrival = last_flight['arrival']
            origin = first_flight['origin']
            destination = last_flight['destination']

            self.origin_result_label = tk.Label(master,text=origin).grid(row=n+1,column=0)
            self.destination_result_label = tk.Label(master,text=destination).grid(row=n+1,column=1)
            self.departure_result_label = tk.Label(master,text=departure).grid(row=n+1,column=2)
            self.arrival_result_label = tk.Label(master,text=arrival).grid(row=n+1,column=3)

    def open_search_flight(self):
        # Close the window
        self.master.destroy()
        # Open the searchflight window
        root = tk.Tk()
        searchFlight_window = SearchFlightWindow(root)
        root.mainloop()

    def open_passenger_details(self):
        # Close the window
        self.master.destroy()
        # Open the fill passenger details window
        root = tk.Tk()
        fillPassengerDetails_window = FillPassengerDetail(root)
        root.mainloop()

class FillPassengerDetail:
    def __init__(self, master):
        self.master = master
        master.title("Fill Passenger Details")
        master.geometry("500x500")

        self.title_label = tk.Label(master, text="Title").grid(row=0, column=0)

        self.mr_check = BooleanVar()
        self.mrs_check = BooleanVar()
        self.ms_check = BooleanVar()
        self.male_check = BooleanVar()
        self.female_check = BooleanVar()

        self.mr_checkbutton = tk.Checkbutton(master, text="Mr.", variable=self.mr_check).grid(row=1, column=0)
        self.mrs_checkbutton = tk.Checkbutton(master, text="Mrs.", variable=self.mrs_check).grid(row=1, column=1)
        self.ms_checkbutton = tk.Checkbutton(master, text="Ms.", variable=self.ms_check).grid(row=1, column=2)

        self.firstname_label = tk.Label(master, text="First Name").grid(row=2, column=0)
        self.firstname_entry = tk.Entry(master)
        self.firstname_entry.grid(row=3, column=0)
        self.lastname_label = tk.Label(master, text="Last Name").grid(row=2, column=1)
        self.lastname_entry = tk.Entry(master)
        self.lastname_entry.grid(row=3, column=1)
        self.birth_label = tk.Label(master, text="Date of Birth (DD/MM/YYYY)").grid(row=4, column=0)
        self.birth_entry = tk.Entry(master)
        self.birth_entry.grid(row=5, column=0)

        self.nationality_combobox = ttk.Combobox(master, height=5, width=15, values=["Thailand","India","China"])
        self.nationality_combobox.grid(row=5, column=1)
        self.nationality_combobox.insert(0, "Nationality")

        self.label1 = tk.Label(master, text="").grid(row=6, column=1)

        self.male_checkbutton = tk.Checkbutton(master, text="MALE", variable=self.male_check).grid(row=7, column=0)
        self.female_checkbutton = tk.Checkbutton(master, text="FEMALE", variable=self.female_check).grid(row=7, column=1)

        self.label2 = tk.Label(master, text="").grid(row=8, column=1)

        self.passport_detail_label = tk.Label(master, text="Passport details (Optional)").grid(row=9, column=0)
        self.passport_detail_entry = tk.Entry(master)
        self.passport_detail_entry.grid(row=10, column=0)
        self.passport_expiry_label = tk.Label(master, text="Passport expiry date (Optional)").grid(row=9, column=1)
        self.passport_expiry_entry = tk.Entry(master)
        self.passport_expiry_entry.grid(row=10, column=1)

        self.travel_type_label = tk.Label(master, text="Travel document (Optional)").grid(row=11, column=0)
        self.travel_type_combobox = ttk.Combobox(master, height=5, width=15, values=["Passport", "Green Card", "Visa"])
        self.travel_type_combobox.grid(row=12, column=0)
        self.travel_type_combobox.insert(0, "Travel Document Type")

        self.residence_country_label = tk.Label(master, text="Country of residence (Optional").grid(row=11, column=1)
        self.residence_country_combobox = ttk.Combobox(master, height=5, width=15, values=["Thailand","India","China"])
        self.residence_country_combobox.grid(row=12, column=1)
        self.residence_country_combobox.insert(0, "Select Country")

        self.label3 = tk.Label(master, text="").grid(row=13, column=1)

        self.contact_detail_label = tk.Label(master, text="Contact details").grid(row=15, column=0)
        self.phone_entry = tk.Entry(master)
        self.phone_entry.grid(row=16, column=0)
        self.phone_entry.insert(0, "Phone number")
        self.email_entry = tk.Entry(master)
        self.email_entry.grid(row=16, column=1)
        self.email_entry.insert(0, "Email address")

        self.label4 = tk.Label(master, text="").grid(row=17, column=1)

        self.back_button = tk.Button(master, text="SearchFlight", command=self.open_search_flight).grid(row=18, column=0)
        self.booking_button = tk.Button(master, text="Book", command=self.create_booking).grid(row=18, column=1)

    def create_booking(self):
        mr = self.mr_check.get()
        mrs = self.mrs_check.get()
        ms = self.ms_check.get()
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        date_of_birth = self.birth_entry.get()
        nationality = self.nationality_combobox.get()
        male = self.male_check.get()
        female = self.female_check.get()
        passport_detail = self.passport_detail_entry.get()
        passport_expiry = self.passport_expiry_entry.get()
        travel_document = self.travel_type_combobox.get()
        country_of_residence = self.residence_country_combobox.get()
        phone_number = self.phone_entry.get()
        email_address = self.email_entry.get()

        # Close the window
        self.master.destroy()
        # Open the bookingSummary window
        root = tk.Tk()
        searchFlight_window = BookingSummaryWindow(root)
        root.mainloop()

    def open_search_flight(self):
        # Close the window
        self.master.destroy()

        # Open the searchflight window
        root = tk.Tk()
        searchFlight_window = SearchFlightWindow(root)
        root.mainloop()

class BookingSummaryWindow:
    def __init__(self, master):
        self.master = master
        master.title("Booking Summary")

        self.trip_summary_label = tk.Label(master, text="Trip Summary").grid(row=0, column=0)
        self.origin_summary_labbel = tk.Label(master, text="Origin").grid(row=1, column=0)
        self.departure_summary_label = tk.Label(master, text="Departuer").grid(row=1, column=1)
        self.destination_summary_label = tk.Label(master, text="Destination").grid(row=1, column=2)
        self.arrival_summary_label = tk.Label(master, text="Arrival").grid(row=1, column=3)
        self.class_summary_label = tk.Label(master, text="Class").grid(row=1, column=4)
        
        #need to get trip data

        self.label1 = tk.Label(master, text="").grid(row=3, column=1)

        self.passenger_detail_summary_label = tk.Label(master, text="Passenger details").grid(row=4, column=0)
        self.passenger_name_summary_label = tk.Label(master, text="Passenger name").grid(row=5, column=0)
        self.date_of_birth_summary_label = tk.Label(master, text="Date of birth").grid(row=5, column=1)
        self.type_summary_label = tk.Label(master, text="Type").grid(row=5, column=2)

        #need to get passenger details data

        self.label2 = tk.Label(master, text="").grid(row=7, column=1)

        self.contact_detail_label = tk.Label(master, text="Contact details").grid(row=8, column=0)
        self.passenger_name_contact_label = tk.Label(master, text="Passenger name").grid(row=9, column=0)
        self.email_contact_label = tk.Label(master, text="E-mail").grid(row=9, column=1)
        self.phone_contact_label = tk.Label(master, text="Phone number").grid(row=9, column=2)

        #need to get contact details data

        self.label3 = tk.Label(master, text="").grid(row=11, column=1)

        self.total_price_label = tk.Label(master, text="Total price").grid(row=12, column=0)
        self.payable_amount_label = tk.Label(master, text="Payable amount").grid(row=13, column=0)

        #need to get total price data

        self.label4 = tk.Label(master, text="").grid(row=14, column=1)

        self.choose_how_to_pay_label = tk.Label(master, text="Choose how to pay").grid(row=15, column=0)

        self.pay_now_check = BooleanVar()
        self.hold_my_booking_check = BooleanVar()
        self.pay_now_checkbutton = tk.Checkbutton(master, text="Pay now", variable=self.pay_now_check).grid(row=16, column=0)
        self.hold_my_booking_checkbutton = tk.Checkbutton(master, text="Hold my booking", variable=self.hold_my_booking_check).grid(row=16, column=1)

        self.label5 = tk.Label(master, text="").grid(row=17, column=1)

        self.cancel_button = tk.Button(master, text="Cancel", command=self.open_search_flight).grid(row=18, column=0)
        self.purchase_button = tk.Button(master, text="Purchase", command=self.open_payment).grid(row=18, column=1)

    def open_search_flight(self):
        # Close the window
        self.master.destroy()
        # Open the searchflight window
        root = tk.Tk()
        searchFlight_window = SearchFlightWindow(root)
        root.mainloop()

    def open_payment(self):
        ...

root = tk.Tk()
login_window = MainWindow(root)
root.mainloop()