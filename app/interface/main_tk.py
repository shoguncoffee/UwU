"""
https://tkdocs.com/tutorial/concepts.html
http://tkdocs.com/pyref/index.html
"""
from __future__ import annotations
from .base import *


class MenuPage(StaticPage):
    master: Root
    
    def add_widgets(self):
        self.label = Label(self, 
            text="SHOGUNUS Airline", 
            font="Bold 20",
        ).pack()
        
        self.login_button = Button(self, 
            command=partial(self.jump, LoginPage), 
            width=15,
            text="Login",
        ).pack()
        
        self.search_button = Button(self, 
            command=partial(self.jump, BookingSection), 
            width=15,
            text="Search Flight",
        ).pack()


class LoginPage(StaticPage):
    master: Root

    def submit(self):
        response = requests.post(API_EndPoint2, params={
            "username": self.username_entry.get(), 
            "password": self.password_entry.get()
        })
        if response.status_code == 200:
            self.response_label.configure(
                text="Login successful!"
            )
            self.root.username = response.json()
        else:
            self.response_label.configure(
                text=f'Error: {response.json()["detail"]}', 
            )
    
    def add_widgets(self):
        self.username_label = Label(self, 
            text="Username"
        ).pack()
        self.username_entry = Entry(self, 
        ).pack()
        
        self.password_label = Label(self, 
            text="Password"
        ).pack()
        self.password_entry = Entry(self, 
            show="*"
        ).pack()
        
        self.submit_button = Button(self, 
            command=self.submit, 
            text="Login",
        ).pack()
        
        self.register_button = Button(self, 
            command=partial(self.jump, RegisterPage), 
            text="Register",
        ).pack()
        
        self.back_button = Button(self, 
            command=partial(self.jump, MenuPage), 
            text="Back",
        ).pack()
        
        self.response_label = Label(self, 
            text="",
        ).pack()


class RegisterPage(StaticPage):
    master: Root

    def submit(self):
        response = requests.post(API_EndPoint1, params={
            "username": self.username_entry.get(), 
            "password": self.password_entry.get(), 
            "email": self.email_entry.get(), 
            "phone": self.phone_entry.get()
        })
        if response.status_code == 200:
            self.response_label.configure(
                text="New account created!", 
            )
        else:
            self.response_label.configure(
                text=f'Error: {response.json()["detail"]}', 
            )
    
    def add_widgets(self):        
        self.username_label = Label(self, 
            text="Username",
        ).pack()
        self.username_entry = Entry(self,
        ).pack()
        
        self.password_label = Label(self, 
            text="Password",
        ).pack()
        self.password_entry = Entry(self, 
            show="*",
        ).pack()
        
        self.email_label = Label(self, 
            text="Email",
        ).pack()
        self.email_entry = Entry(self,
        ).pack()
        
        self.phone_label = Label(self, 
            text="Phone",
        ).pack()
        self.phone_entry = Entry(self,
        ).pack()
        
        self.submit_button = Button(self, 
            command=self.submit, 
            text="Submit",
        ).pack()
        
        self.login_button = Button(self, 
            command=partial(self.jump, LoginPage), 
            text="Go to Login",
        ).pack()
        
        self.response_label = Label(self, 
            text="",
        ).pack()


class BookingSection(SubSection):
    def procedure(self):
        pax, self.journey = self.open(
            SearchSection(self)
        ).returned()
        
        self.passengers, self.contact = self.open(
            PassengerSection(self, pax)
        ).returned()
        #contact_unforgot
        self.summery()
        self.wait_variable(self.waiter)
        self.jump(MenuPage)
        
    def create_booking(self):
        API_EndPoint4 = f"http://127.0.0.1:8000/account/{self.root.username}/book"

        response = requests.post(API_EndPoint4, json={
            "journey": [(
                    [flight.reduce().json() for flight in itinerary.flights], travel_class
                ) for itinerary, travel_class in self.journey
            ],
            "contact": self.contact.json(),
            "passengers": [
                passenger.json() for passenger in self.passengers
            ]
        })
        self.next()

    def summery(self): 
        frame = Frame(self)
        
        self.trip_summary_label = Label(frame, 
            text="Trip Summary", 
            font="bold"
        ).grid(row=0, column=0)
        
        self.origin_summary_labbel = Label(frame, 
            text="Origin"
        ).grid(row=1, column=0)
        
        self.departure_summary_label = Label(frame, 
            text="Departuer"
        ).grid(row=1, column=1)
        
        self.destination_summary_label = Label(frame,               
            text="Destination"
        ).grid(row=1, column=2)
        
        self.arrival_summary_label = Label(frame, 
            text="Arrival"
        ).grid(row=1, column=3)
        
        self.class_summary_label = Label(frame, 
            text="Class"
        ).grid(row=1, column=4)
        
        #need to get trip data
        self.label1 = Label(frame, 
            text=""
        ).grid(row=3, column=1)
        
        self.passenger_detail_summary_label = Label(frame, 
            text="Passenger details", 
            font="bold"
        ).grid(row=4, column=0)
        
        self.passenger_name_summary_label = Label(frame, 
            text="Passenger name"
        ).grid(row=5, column=0)
        
        self.date_of_birth_summary_label = Label(frame, 
            text="Date of birth"
        ).grid(row=5, column=1)
        
        self.type_summary_label = Label(frame, 
            text="Type"
        ).grid(row=5, column=2)

        for n, passenger in enumerate(self.passengers, 1):
            self.passenger_name_summary_result_label = Label(frame, 
                text = passenger.name
            ).grid(
                row=n+5, column=0
            )
            self.date_of_birth_summary_result_label = Label(frame, 
                text = str(passenger.birthdate)
            ).grid(row=n+5, column=1)
            
            self.type_summary_result_label = Label(frame, 
                text = passenger.type.name
            ).grid(row=n+5, column=2)

        i = 5 + len(self.passengers)
        
        self.label2 = Label(frame, 
            text=""
        ).grid(row=i+1, column=1)

        self.contact_detail_label = Label(frame, 
            text="Contact details", 
            font="bold"
        ).grid(row=i+2, column=0)
        
        self.passenger_name_contact_label = Label(frame, 
            text="Passenger name"
        ).grid(row=i+3, column=0)
        
        self.email_contact_label = Label(frame, 
            text="E-mail"
        ).grid(row=i+3, column=1)
        
        self.phone_contact_label = Label(frame, 
            text="Phone number"
        ).grid(row=i+3, column=2)

        passenger_name = self.passengers[self.contact.index].name
        email = self.contact.email
        phone = self.contact.phone

        self.passenger_name_contact_result_label = Label(frame, 
            text=passenger_name
        ).grid(row=i+4, column=0)
        
        self.email_contact_result_label = Label(frame, 
            text=email
        ).grid(row=i+4, column=1)
        
        self.phone_contact_result_label = Label(frame, 
            text=phone
        ).grid(row=i+4, column=2)

        self.label3 = Label(frame, 
            text=""
        ).grid(row=i+5, column=1)

        self.total_price_label = Label(frame, 
            text="Total price", 
            font="bold"
        ).grid(row=i+6, column=0)
        
        self.payable_amount_label = Label(frame, 
            text="Payable amount", 
            font="bold"
        ).grid(row=i+7, column=0)

        #need to get total price data
        self.label4 = Label(frame, 
            text=""
        ).grid(row=14, column=1)

        self.choose_how_to_pay_label = Label(frame, 
            text="Choose how to pay" , 
            font="bold"
        ).grid(row=15, column=0)

        pay_now_check = tk.BooleanVar(frame)
        hold_my_booking_check = tk.BooleanVar(frame)
        
        self.pay_now_checkbutton = Checkbutton(frame, 
            text = "Pay now", 
            variable = pay_now_check,
        ).grid(row = 16, column=0)
        
        self.hold_my_booking_checkbutton = Checkbutton(frame, 
            text = "Hold my booking", 
            variable = hold_my_booking_check
        ).grid(row=16, column=1)

        self.label5 = Label(frame, 
            text=""
        ).grid(row=17, column=1)

        self.cancel_button = Button(frame, 
            text="Cancel", 
            command = self.next
        ).grid(row=18, column=0)
        
        self.purchase_button = Button(frame, 
            text="Purchase", 
            command=self.create_booking
        ).grid(row=18, column=1)

        frame.pack()
        

class SearchSection(SubSection):
    def procedure(self):
        self.pax, itinerarys = self.peek(
            SearchPage(self)
        ).returned()

        # self.jouney = []
        self.itinerarys = self.peek(
            ResultPage(self, itinerarys)
        ).returned()
            
    def returned(self): 
        return self.pax, [self.itinerarys] #!


class SearchPage(Page):
    master: SearchSection
    
    # def next(self):
        # if ['invalaid'] not in self.origin_entry['state']:
            # super().wait_done()
        # super().next()

    def returned(self):
        super().returned()
        trip = self.trip_combobox.get()
        departure_day = self.departure_day_spinbox.get()
        departure_month = self.departure_month_spinbox.get()
        departure_year = self.departure_year_spinbox.get()
        
        pax = src.Pax({
            passenger_type: int(spinbox.get())
            for passenger_type, spinbox in self.pax_spinbox.items()
        }.items())
        
        response = requests.get(url + API_Endpoint3, params={
            "origin": self.origin_entry.get(),
            "destination": self.destination_entry.get(),
            "date": f'{departure_year}-{departure_month}-{departure_day}',
            "adult": pax.get(PassengerType.ADULT),
            "child": pax.get(PassengerType.CHILD),
            "infant": pax.get(PassengerType.INFANT),
        })
        itinerary = [
            body.ItineraryBody(**data) for data in response.json()
        ]
        return pax, itinerary
       
    def add_widgets(self):        
        self.origin_label = Label(self, 
            text="From",
        ).grid(row=0, column=0,)
        
        self.destination_label = Label(self, 
            text="To"
        ).grid(row=0, column=1,)
        
        self.origin_entry = AirportEntry(self).grid(row=1, column=0)
        self.destination_entry = AirportEntry(self).grid(row=1, column=1)
        
        self.trip_label = Label(self, 
            text="Trip",
        ).grid(row=0, column=2,)
        
        self.trip_combobox = Combobox(self,
            height=6, width=13, 
            values=["One Way"],
        ).grid(row=1, column=2,)
        
        self.departure_date_label = Label(self, 
            text="Departure",
        ).grid(row=0, column=3,)
        
        self.departure_day_spinbox = Combobox(self,
            width=6,
            values=[str(s) for s in range(1, 31)],
        ).grid(row=1, column=3)

        self.departure_month_spinbox = Combobox(self,
            width=6,
            values=[str(s) for s in range(1, 13)],
        ).grid(row=2, column=3,)
        
        self.departure_year_spinbox = Combobox(self,
            width=6,
            values=['2023'],
        ).grid(row=3, column=3,)

        self.passenger_label = Label(self, 
            text="Passengers",
        ).grid(row=0, column=5,)

        self.departure_day_spinbox.insert(0, "Day")
        self.departure_month_spinbox.insert(0, "Month")
        self.departure_year_spinbox.insert(0, "Year")

        self.pax_spinbox = {
            PassengerType.ADULT: Spinbox(self,
                    from_=1, to=20, 
                    width=2,
                    state='readonly'
                ).grid(row=1, column=6,),
            PassengerType.CHILD: Spinbox(self,
                    from_=0, to=10, 
                    width=2,
                    state='readonly'
                ).grid(row=2, column=6,),
            PassengerType.INFANT: Spinbox(self,
                    from_=0, to=10, 
                    width=2,
                    state='readonly'
                ).grid(row=3, column=6,),
        }
        for passenger_type, spinbox in self.pax_spinbox.items():
            Label(self, 
                text=passenger_type.name
            ).grid(row=spinbox.grid_info()['row'], column=5,)


        self.search_button = Button(self, 
            command=self.next, 
            text="Search",
            # state=DISABLED,
        ).grid(row=4, column=2,)
        # self.search_button['state'] = NORMAL
        
        self.back_button = Button(self, 
            command=partial(self.master.jump, MenuPage), 
            text="Back to Main",
        ).grid(row=3, column=2,)


class ResultPage(Page):
    master: SearchSection

    def __init__(self, master, itinerarys: list[body.ItineraryBody]):
        self.itinerarys = itinerarys
        super().__init__(master)
        
    def returned(self):
        super().returned()
        return self.itinerary, self.travel_class

    def choose(self, itinerary: body.ItineraryBody, travel_class: TravelClass):
        self.travel_class = travel_class
        self.itinerary = itinerary
        self.next()
        
    def add_widgets(self):        
        self.origin_label = Label(self, 
            text="Origin"
        ).grid(row=0, column=0)
        
        self.destination_label = Label(self, 
            text="Destination"
        ).grid(row=0, column=1)
        
        self.departure_label = Label(self, 
            text="Departure"
        ).grid(row=0, column=2)
        
        self.arrival_label = Label(self, 
            text="Arrival"
        ).grid(row=0, column=3)
        
        self.economy_label = Label(self, 
            text="Economy"
        ).grid(row=0, column=5)
        
        self.business_label = Label(self, 
            text="Business"
        ).grid(row=0, column=6)
        
        self.first_label = Label(self, 
            text="First"
        ).grid(row=0, column=7)
        
        self.back_button = Button(self, 
            command=self.back,
            text="Search Flight",
        ).grid(row=0, column=8)
        
        for n, itinerary in enumerate(self.itinerarys, 1) :
            first_flight = itinerary.flights[0]
            last_flight = itinerary.flights[-1]

            origin = first_flight.origin
            departure = first_flight.departure
            destination = last_flight.destination
            arrival = last_flight.arrival

            if first_flight is last_flight:
                ...

            Label(self, 
                text = origin
            ).grid(row=n, column=0)
            
            Label(self, 
                text = destination
            ).grid(row=n, column=1)
            
            Label(self, 
                text = f'{departure:%H:%M}'
            ).grid(row=n, column=2)
            
            Label(self, 
                text = f'{arrival:%H:%M}'
            ).grid(row=n, column=3)
            
            for data in itinerary.classes:
                travel_class = data.travel_class
                
                if data.seat_left < 20:
                    # show seat left?
                    ...
                
                Button(self, 
                    text = data.price,
                    command = partial(self.choose, itinerary, travel_class)
                ).grid(row=n, column=travel_class + 4)


class PassengerSection(SubSection):    
    def __init__(self, master, pax: src.Pax):
        self.pages = [(
            type(f'{FillPassengerPage.__name__}{n}', (FillPassengerPage,), {}), passenger_type
            ) for passenger_type, number in pax for n in range(number)
        ]
        print(self.pages)
        super().__init__(master)

    def returned(self):
        return self.passengers, self.contact

    def procedure(self):
        self.passengers: list[body.PassengerBody] = []
        
        for n, (FillPage, passenger_type) in enumerate(self.pages):
            page = self.peek(
                FillPage(self, passenger_type, n)
            )
            self.passengers.append(page.returned())
            print('append')

        print('contact')
        self.contact = self.peek(
            SelectContactPage(self, self.passengers)
        ).returned()
        

class FillPassengerPage(Page):
    master: PassengerSection

    def __init__(self, master, passenger_type: PassengerType, number: int):
        self.number = number
        self.passenger_type = passenger_type
        super().__init__(master)

    def returned(self):
        super().returned()
        passport_expiry = self.passport_expiry_entry.get()
        travel_document = self.travel_type_combobox.get()
        country_of_residence = self.residence_country_combobox.get()
        
        return body.PassengerBody(
            forename = self.title_combobox.get() + self.firstname_entry.get(),
            surname = self.lastname_entry.get(),
            birthdate = dt.date.fromisoformat(self.birth_entry.get()),
            nationality = self.nationality_combobox.get(),
            passport_id = self.passport_detail_entry.get(),
            gender = GenderType[self.gender_combobox.get()],
            type = self.passenger_type
        )

    def add_widgets(self):
        self.title_label = Label(self, 
            text="Title"
        ).grid(row=0, column=0)
        self.title_combobox = Combobox(self, 
            height=5, width=15,
            values=["Mr.", "Mrs.", "Ms."]
        ).grid(row=1,column=0)

        self.firstname_label = Label(self, 
            text="First Name"
        ).grid(row=2, column=0)
        self.firstname_entry = Entry(self
        ).grid(row=3, column=0)

        self.lastname_label = Label(self,
             text="Last Name"
        ).grid(row=2, column=1)
        self.lastname_entry = Entry(self
        ).grid(row=3, column=1)
        
        self.birth_label = Label(self, 
            text="Date of Birth (YYYY-MM-DD)"
        ).grid(row=4, column=0)
        self.birth_entry = Entry(self
        ).grid(row=5, column=0)

        self.nationality_combobox = Combobox(self, 
            height=5, 
            width=15, 
            values=["Thailand","India","China"]
        ).grid(row=5, column=1)

        self.label1 = Label(self, 
            text="Gender"
        ).grid(row=6, column=0)
        self.gender_combobox = Combobox(self,
            height=5, width=15, 
            values=[gender.name for gender in GenderType]
        ).grid(row=7, column=0)

        self.label2 = Label(self, 
            text = f'{self.number+1}. {self.passenger_type.name}'
        ).grid(row=0, column=1)

        self.label3 = Label(self, 
            text=""
        ).grid(row=8, column=1)

        self.passport_detail_label = Label(self, 
            text="Passport details (Optional)"
        ).grid(row=9, column=0)
        self.passport_detail_entry = Entry(self
        ).grid(row=10, column=0)

        self.passport_expiry_label = Label(self, 
            text="Passport expiry date (Optional)"
        ).grid(row=9, column=1)
        self.passport_expiry_entry = Entry(self
        ).grid(row=10, column=1)

        self.travel_type_label = Label(self, 
            text="Travel document (Optional)"
        ).grid(row=11, column=0)
        self.travel_type_combobox = Combobox(self, 
            height=5, 
            width=15, 
            values=["Passport", "Green Card", "Visa"]
        ).grid(row=12, column=0)

        self.residence_country_label = Label(self, 
            text="Country of residence (Optional"
        ).grid(row=11, column=1)
        self.residence_country_combobox = Combobox(self, 
            height=5, 
            width=15, 
            values=["Thailand","India","China"]
        ).grid(row=12, column=1)

        self.label4 = Label(self, 
            text=""
        ).grid(row=13, column=1)

        self.title_combobox.insert(0, "Choose your title")
        self.nationality_combobox.insert(0, "Nationality")        
        self.gender_combobox.insert(0, "Choose your gender")
        self.travel_type_combobox.insert(0, "Travel Document Type")
        self.residence_country_combobox.insert(0, "Select Country")        

        if self.number > 0:
            self.back_button = Button(self, 
                text = 'previous', 
                command = self.back
            ).grid(row=19, column=0)
        
        self.next_button = Button(self, 
            text = "Next", 
            command = self.next
        ).grid(row=19, column=1)


class SelectContactPage(Page):
    def __init__(self, master, passengers: list[body.PassengerBody]):
        self.passengers_name = [
            passenger.name for passenger in passengers
            if passenger.type is PassengerType.ADULT
        ]
        super().__init__(master)

    def returned(self):
        super().returned()
        return body.ContactInfoBody(
            index = self.contact_combobox.current(),
            phone = self.phone_entry.get(),
            email = self.email_entry.get()
        )
        
    def add_widgets(self):
        self.contact_combobox = Combobox(self,
            height = 5,
            width = 20,
            values = self.passengers_name
        ).grid(row=18,column=1)

        self.contact_detail_label = Label(self, 
            text="Contact details"
        ).grid(row=15, column=0)
          
        self.next_button = Button(self, 
            text="summery", 
            command=self.next
        ).grid(row=19, column=1)
        
        self.phone_entry = Entry(self
        ).grid(row=17, column=0)

        self.email_entry = Entry(self
        ).grid(row=17, column=1)
        
        self.contact_combobox.insert(0, "Choose whose contact")
        self.phone_entry.insert(0, "Phone number")
        self.email_entry.insert(0, "Email address") 

class PaymentPage(Page):
    def __init__(self, master, booking: body.BookingBody):
        self.booking = booking
        super().__init__(master)

    def add_widgets(self):
        self.payment_label = Label(self, 
            text="Select your preferred payment method"
        ).grid(row=0, column=0)
        
        self.back_button = Button(self, 
            text="Back", 
            command=...
        ).grid(row=2, column=0)


class SelectSeatSection(SubSection):
    def __init__(self, master, 
        itinerary: body.ItineraryBody,
        
    ):
        self.itinerary = itinerary
        self.seats: list[body.SeatBody] = []
        super().__init__(master)    

    def procedure(self):
        search_page = SearchPage(self)
        self.stack(search_page)
        
        self.pax, itinerarys = search_page.returned()

        result = self.stack(ResultPage(self, itinerarys))
        
        for page in SearchPage, ResultPage:
            if ...:
                self
                break
        
        self.pax, itinerarys = self.stack(SearchPage(self)).returned()
        self.travel_class, self.itinerary = self.stack(ResultPage(self, itinerarys)).returned()


    def returned(self):
        return ...


class SelectSeatPage(Page):
    def __init__(self, master, 
        itinerary: body.ItineraryBody,
        
    ):
        self.itinerary = itinerary
        self.seats: list[body.SeatBody] = []
        super().__init__(master)

    def add_widgets(self):
        self.seat_frame = Frame(self).pack(side=RIGHT)

        for seat in self.seats:
            seat = Button(self.seat_frame, 
                text=seat.number, 
                command=...
            ).pack(side=LEFT)