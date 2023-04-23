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

        self.departure_day_combobox = ttk.Combobox(master,height=5,width=15,values=list(str(s) for s in range(1, 32)))
        self.departure_day_combobox.grid(row=1,column=3)
        self.departure_day_combobox.insert(0, "Day")

        self.departure_month_combobox = ttk.Combobox(master,height=5,width=15,values=list(str(s) for s in range(1, 13)))
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
                all_passengers = int(passenger_adult) + int(passenger_children) + int(passenger_infant)
                # Close the window
                self.master.destroy()
                # Open the search flight result window
                root = tk.Tk()
                search_flight_result_window = SearchFlightResultWindow(root, response, all_passengers)
                root.mainloop()

    def open_main(self):
        # Close the window
        self.master.destroy()
        # Open the Main window
        root = tk.Tk()
        main_window = MainWindow(root)
        root.mainloop()        

class SearchFlightResultWindow:
    def __init__(self, master, response: requests.Response, all_passengers: int):
        self.master = master
        master.title("Search Flight Result")

        print(all_passengers)

        self.origin_label = tk.Label(master, text="Origin").grid(row=0, column=0)
        self.destination_label = tk.Label(master, text="Destination").grid(row=0, column=1)
        self.departure_label = tk.Label(master, text="Departure").grid(row=0, column=2)
        self.arrival_label = tk.Label(master, text="Arrival").grid(row=0, column=3)
        self.economy_label = tk.Label(master, text="Economy").grid(row=0, column=5)
        self.business_label = tk.Label(master, text="Business").grid(row=0, column=6)
        self.first_label = tk.Label(master, text="First").grid(row=0, column=7)
        
        self.back_button = tk.Button(master, text="SearchFlight", command=self.open_search_flight).grid(row=0, column=8)

        result = response.json()
        self.all_passengers = all_passengers
        
        for n, itinerary in enumerate(result) :
            flights = itinerary['flights']
            first_flight = flights[0]
            last_flight = flights[-1]
 
            departure = first_flight['departure']
            arrival = last_flight['arrival']
            origin = first_flight['origin']
            destination = last_flight['destination']

            self.origin_result_label = tk.Label(master,text=origin).grid(row=n+1,column=0)
            self.destination_result_label = tk.Label(master,text=destination).grid(row=n+1,column=1)
            self.departure_result_label = tk.Label(master,text=departure).grid(row=n+1,column=2)
            self.arrival_result_label = tk.Label(master,text=arrival).grid(row=n+1,column=3)

            classes = itinerary['classes']
            for item in classes.items():
                cls, data = item
                price = data['price']
                self.book_button = tk.Button(master, text=price, command=self.select_flight(flights, item)).grid(row=n+1, column=4+int(cls))
            
    def open_search_flight(self):
        # Close the window
        self.master.destroy()
        # Open the searchflight window
        root = tk.Tk()
        searchFlight_window = SearchFlightWindow(root)
        root.mainloop()

    def select_flight(self, itinerary, travel_class):
        def func():
            all_passengers = self.all_passengers
            passenger_num = 1
            passenger_detail_list = []
            # Close the window
            self.master.destroy()
            # Open the fill passenger details window
            root = tk.Tk()
            fillPassengerDetails_window = FillPassengerDetail(root, itinerary, travel_class, passenger_num, all_passengers, passenger_detail_list)
            root.mainloop()
        return func

class FillPassengerDetail:
    def __init__(self, master, itinerary, travel_class, passenger_num: int, all_passengers: int, passenger_detail_list: list):
        self.master = master
        master.title("Fill Passenger Details")

        print(itinerary)
        print(travel_class)
        print(passenger_num)
        print(all_passengers)

        self.all_itinerary = itinerary
        self.travel_class = travel_class
        self.passenger_num = passenger_num
        self.all_passengers = all_passengers 
        self.passenger_detail_list = passenger_detail_list
        #self.total_price = travel_class[1]["price"]

        from app.constants import GenderType
        self.title_label = tk.Label(master, text="Title").grid(row=0, column=0)

        self.title_combobox = ttk.Combobox(master,height=5,width=15,values=["Mr.", "Mrs", "Ms."])
        self.title_combobox.grid(row=1,column=0)
        self.title_combobox.insert(0, "Choose your title")

        self.firstname_label = tk.Label(master, text="First Name").grid(row=2, column=0)
        self.firstname_entry = tk.Entry(master)
        self.firstname_entry.grid(row=3, column=0)
        self.lastname_label = tk.Label(master, text="Last Name").grid(row=2, column=1)
        self.lastname_entry = tk.Entry(master)
        self.lastname_entry.grid(row=3, column=1)
        self.birth_label = tk.Label(master, text="Date of Birth (YYYY-MM-DD)").grid(row=4, column=0)
        self.birth_entry = tk.Entry(master)
        self.birth_entry.grid(row=5, column=0)

        self.nationality_combobox = ttk.Combobox(master, height=5, width=15, values=["Thailand","India","China"])
        self.nationality_combobox.grid(row=5, column=1)
        self.nationality_combobox.insert(0, "Nationality")

        self.label1 = tk.Label(master, text="Gender").grid(row=6, column=0)
        from app.constants import GenderType
        self.gender_list = [gender.name for gender in GenderType]
        self.gender_combobox = ttk.Combobox(master,height=5,width=15,values=self.gender_list)
        self.gender_combobox.grid(row=7,column=0)
        self.gender_combobox.insert(0, "Choose your gender")

        self.label2 = tk.Label(master, text="Passenger type").grid(row=6, column=1)
        from app.constants import PassengerType
        self.passenger_type_list = [age.name for age in PassengerType]
        self.passenger_type_combobox = ttk.Combobox(master,height=5,width=15,values=self.passenger_type_list)
        self.passenger_type_combobox.grid(row=7,column=1)
        self.passenger_type_combobox.insert(0, "Choose your age range")

        self.label3 = tk.Label(master, text="").grid(row=8, column=1)

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

        self.label4 = tk.Label(master, text="").grid(row=13, column=1)

        self.back_button = tk.Button(master, text="SearchFlight", command=self.open_search_flight).grid(row=19, column=0)

        if passenger_num < all_passengers:
            self.next_passenger_button = tk.Button(master, text="Next Passenger", command=self.next_passenger).grid(row=19, column=1)
        
        else:
            self.contact_detail_label = tk.Label(master, text="Contact details").grid(row=15, column=0)
            self.phone_entry = tk.Entry(master)
            self.phone_entry.grid(row=17, column=0)
            self.phone_entry.insert(0, "Phone number")
            self.email_entry = tk.Entry(master)
            self.email_entry.grid(row=17, column=1)
            self.email_entry.insert(0, "Email address")

            self.username_entry = tk.Entry(master)
            self.username_entry.grid(row=18, column=0)
            self.username_entry.insert(0, "Account username")

            self.contact_combobox = ttk.Combobox(master,height=5,width=15,values=list(str(i) for i in range(1, self.all_passengers+1)))
            self.contact_combobox.grid(row=18,column=1)
            self.contact_combobox.insert(0, "Choose whose contact")

            self.booking_button = tk.Button(master, text="Book", command=self.create_booking).grid(row=19, column=1)
    
    def next_passenger(self):
        from app.constants import GenderType, PassengerType

        title = self.title_combobox.get()
        firstname = title + self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        date_of_birth = self.birth_entry.get()
        nationality = self.nationality_combobox.get()
        gender = GenderType[self.gender_combobox.get()]
        passenger_type = PassengerType[self.passenger_type_combobox.get()]
        passport_detail = self.passport_detail_entry.get()
        passport_expiry = self.passport_expiry_entry.get()
        travel_document = self.travel_type_combobox.get()
        country_of_residence = self.residence_country_combobox.get()

        passenger_detail = {
            "forename": firstname,
            "surname": lastname,
            "birthdate": date_of_birth,
            "nationality": nationality,
            "passport_id": passport_detail,
            "gender": gender,
            "type": passenger_type
            }
        
        self.passenger_detail_list.append(passenger_detail)
        
        itinerary = self.all_itinerary
        travel_class = self.travel_class
        passenger_num = self.passenger_num + 1
        all_passengers = self.all_passengers

        print(passenger_detail)
        print(self.passenger_detail_list)

        # Close the window
        self.master.destroy()
        # Open the fill window
        root = tk.Tk()
        fillPassengerDetails_window = FillPassengerDetail(root, itinerary, travel_class, passenger_num, all_passengers, self.passenger_detail_list)
        root.mainloop()
        

    def create_booking(self):
        from app.constants import GenderType, PassengerType
        
        title = self.title_combobox.get()
        firstname = title + self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        date_of_birth = self.birth_entry.get()
        nationality = self.nationality_combobox.get()
        gender = GenderType[self.gender_combobox.get()]
        passenger_type = PassengerType[self.passenger_type_combobox.get()]
        passport_detail = self.passport_detail_entry.get()
        passport_expiry = self.passport_expiry_entry.get()
        travel_document = self.travel_type_combobox.get()
        country_of_residence = self.residence_country_combobox.get()
        phone_number = self.phone_entry.get()
        email_address = self.email_entry.get()
        username = self.username_entry.get()
        contact = self.contact_combobox.get()

        API_EndPoint4 = f"http://127.0.0.1:8000/account/{username}/book"
        
        data = {
            "journey":
            [
                (
                    [
                        {
                            "date": flight['date'],
                            "designator": flight['designator']
                        }
                        for flight in self.all_itinerary
                    ], 
                    self.travel_class[0]
                )
            ],
            "contact":
            {
                "index": int(contact),
                "phone":phone_number,
                "email": email_address
            },
            "passengers": self.passenger_detail_list + [
                {
                    "forename": firstname,
                    "surname": lastname,
                    "birthdate": date_of_birth,
                    "nationality": nationality,
                    "passport_id": passport_detail,
                    "gender": gender,
                    "type": passenger_type
                }
            ]
        }
        import json
        print(json.dumps(data, indent=4))

        response = requests.post(url=API_EndPoint4, params=username, data=data)
        
        print(response.text)

        # Close the window
        self.master.destroy()
        # Open the bookingSummary window
        root = tk.Tk()
        booking_summary_window = BookingSummaryWindow(root, data)
        root.mainloop()

    def open_search_flight(self):
        # Close the window
        self.master.destroy()
        # Open the searchflight window
        root = tk.Tk()
        searchFlight_window = SearchFlightWindow(root)
        root.mainloop()

class BookingSummaryWindow:
    def __init__(self, master, data: dict):
        self.master = master
        master.title("Booking Summary")

        self.data = data 

        self.trip_summary_label = tk.Label(master, text="Trip Summary", font="bold").grid(row=0, column=0)
        self.origin_summary_labbel = tk.Label(master, text="Origin").grid(row=1, column=0)
        self.departure_summary_label = tk.Label(master, text="Departuer").grid(row=1, column=1)
        self.destination_summary_label = tk.Label(master, text="Destination").grid(row=1, column=2)
        self.arrival_summary_label = tk.Label(master, text="Arrival").grid(row=1, column=3)
        self.class_summary_label = tk.Label(master, text="Class").grid(row=1, column=4)
        
        #need to get trip data

        self.label1 = tk.Label(master, text="").grid(row=3, column=1)

        self.passenger_detail_summary_label = tk.Label(master, text="Passenger details", font="bold").grid(row=4, column=0)
        self.passenger_name_summary_label = tk.Label(master, text="Passenger name").grid(row=5, column=0)
        self.date_of_birth_summary_label = tk.Label(master, text="Date of birth").grid(row=5, column=1)
        self.type_summary_label = tk.Label(master, text="Type").grid(row=5, column=2)

        #get passenger details data
        passenger_detail = self.data["passengers"]
        from app.constants import PassengerType
        n = 0
        i = 5
        for item in passenger_detail:
            passenger_name = item["forename"] + " " + item["surname"]
            date_of_birth = item["birthdate"]
            passenger_type = PassengerType(int(item["type"])).name

            print(passenger_name)
            print(date_of_birth)
            print(passenger_type)
            n += 1
            i += 1

            self.passenger_name_summary_result_label = tk.Label(master, text=passenger_name).grid(row=n+5, column=0)
            self.date_of_birth_summary_result_label = tk.Label(master, text=date_of_birth).grid(row=n+5, column=1)
            self.type_summary_result_label = tk.Label(master, text=passenger_type).grid(row=n+5, column=2)

        self.label2 = tk.Label(master, text="").grid(row=i+1, column=1)

        self.contact_detail_label = tk.Label(master, text="Contact details", font="bold").grid(row=i+2, column=0)
        self.passenger_name_contact_label = tk.Label(master, text="Passenger name").grid(row=i+3, column=0)
        self.email_contact_label = tk.Label(master, text="E-mail").grid(row=i+3, column=1)
        self.phone_contact_label = tk.Label(master, text="Phone number").grid(row=i+3, column=2)

        #get contact details data
        contact = self.data["contact"]
        index = contact["index"]
        passenger_name = passenger_detail[int(index)-1]["forename"] + " " + passenger_detail[int(index)-1]["surname"]
        email = contact["email"]
        phone = contact["phone"]

        self.passenger_name_contact_result_label = tk.Label(master, text=passenger_name).grid(row=i+4, column=0)
        self.email_contact_result_label = tk.Label(master, text=email).grid(row=i+4, column=1)
        self.phone_contact_result_label = tk.Label(master, text=phone).grid(row=i+4, column=2)

        self.label3 = tk.Label(master, text="").grid(row=i+5, column=1)

        self.total_price_label = tk.Label(master, text="Total price", font="bold").grid(row=i+6, column=0)
        self.payable_amount_label = tk.Label(master, text="Payable amount", font="bold").grid(row=i+7, column=0)

        #need to get total price data

        self.label4 = tk.Label(master, text="").grid(row=14, column=1)

        self.choose_how_to_pay_label = tk.Label(master, text="Choose how to pay" , font="bold").grid(row=15, column=0)

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
        # Close the window
        self.master.destroy()
        # Open the payment window
        root = tk.Tk()
        payment_window = PaymentWindow(root)
        root.mainloop()

class PaymentWindow:
    def __init__(self, master):
        self.master = master
        master.title("Payment")

        self.payment_label = tk.Label(master, text="Select your preferred payment method").grid(row=0, column=0)
        
        #need to create input and get data

        self.back_button = tk.Button(master, text="Back", command=self.open_booking_summary).grid(row=2, column=0)

    def open_booking_summary(self):
        # Close the window
        self.master.destroy()
        # Open the booking summary window
        root = tk.Tk()
        booking_summary_window = MainWindow(root)
        root.mainloop()


root = tk.Tk()
main_window = MainWindow(root)
root.mainloop()

#q = []
#for a in range(10):
    #def g():
    #    return a
    
    #q.append(g)


#for n, func in zip(range(3), q):
    #b1 = (command=func)