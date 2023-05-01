"""
https://tkdocs.com/tutorial/concepts.html
http://tkdocs.com/pyref/index.html
"""
from __future__ import annotations

from app.api.body_template import PreBookingBody
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
        username = self.username_entry.get()
        response = requests.post(url + API_EndPoint2, params={
            "username": username, 
            "password": self.password_entry.get()
        })
        if response.status_code == 200:
            self.response_label.configure(
                text="Login successful!"
            )
            self.root.username = username
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
        response = requests.post(url + API_EndPoint1, params={
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
        pax, selected_trip = self.open(
            SearchSection(self)
        ).returned()
        
        passengers, contact = self.open(
            PassengerSection(self, pax)
        ).returned()

        self.open(
            ReviewSection(self, passengers, contact, selected_trip)
        )
        
        self.jump(MenuPage)
        

class SearchSection(SubSection):
    def procedure(self):
        self.pax, itinerarys = self.peek(
            SearchPage(self)
        ).returned()

        # self.jouney = []
        self.flights, self.classinfo = self.peek(
            ResultPage(self, itinerarys)
        ).returned()
            
    def returned(self): 
        return self.pax, [(self.flights, self.classinfo)] #!


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
        for row, (passenger_type, spinbox) in enumerate(self.pax_spinbox.items(), 1):
            Label(self, 
                text=passenger_type.name
            ).grid(row=row, column=5)
            spinbox.grid(row=row, column=6)


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
        return self.flights, self.classinfo

    def choose(self, itinerary: body.ItineraryBody, travel_class: TravelClass):
        self.classinfo = itinerary.get_class(travel_class)
        self.flights = itinerary.flights
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
        
        for row, itinerary in enumerate(self.itinerarys, 1):
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
            ).grid(row=row, column=0)
            
            Label(self, 
                text = destination
            ).grid(row=row, column=1)
            
            Label(self, 
                text = f'{departure:%H:%M}'
            ).grid(row=row, column=2)
            
            Label(self, 
                text = f'{arrival:%H:%M}'
            ).grid(row=row, column=3)
            
            for data in itinerary.classes:
                travel_class = data.travel_class
                total_price = data.price
                
                if data.seat_left < 20:
                    # show seat left?
                    ...
                
                Button(self, 
                    text = total_price,
                    command = partial(self.choose, itinerary, travel_class)
                ).grid(row=row, column=travel_class + 4)


class PassengerSection(SubSection):    
    def __init__(self, master, pax: src.Pax):
        self.pages = [(
            type(f'{FillPassengerPage.__name__}{n}', (FillPassengerPage,), {}), passenger_type
            ) for passenger_type, number in pax for n in range(number)
        ]
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


class ReviewSection(SubSection):
    def __init__(self, master, 
        passengers: list[body.PassengerBody],
        contact: body.ContactInfoBody,
        selected_trip: list[tuple[list[body.FlightInfoBody], body.ClassInfoBody]],
    ):
        self.passengers = passengers
        self.contact = contact
        self.selected_trip = selected_trip
        super().__init__(master)

    def procedure(self):
        confirm, paynow = self.peek(
            SummeryPage(self)
        ).returned()
        if confirm:
            self.create_booking()

        if paynow:
            self.peek(
                PaymentPage(self)
            )
    
    def create_booking(self):
        prebooking = body.PreBookingBody(
            contact = self.contact,
            passengers = self.passengers,
            journey = [
                (
                    [flight.reduce() for flight in flights], 
                    classinfo.travel_class
                ) for flights, classinfo in self.selected_trip
            ],
        )
        response = requests.post(
            f'{url}/account/{self.root.username}/book', 
            prebooking.json()
        )
    

class SummeryPage(Page):
    master: ReviewSection

    def __init__(self, master):
        self.is_cancel = False
        self.pay_now_var = tk.BooleanVar(self)
        
        super().__init__(master)

    def returned(self):
        super().returned()
        return self.is_cancel, self.pay_now_var.get() 

    def cancel(self):
        self.is_cancel = True
        self.next()
        
    def add_widgets(self): 
        self.trip_summary_label = Label(self, 
            text="Trip Summary", 
            font="bold"
        ).grid(row=0, column=0)
        
        self.origin_summary_label = Label(self, 
            text="Origin"
        ).grid(row=1, column=0)
        
        self.destination_summary_label = Label(self, 
            text="Destination"
        ).grid(row=1, column=1)
        
        self.departure_summary_label = Label(self,               
            text="Departuer"
        ).grid(row=1, column=2)
        
        self.arrival_summary_label = Label(self, 
            text="Arrival"
        ).grid(row=1, column=3)

        self.date_summary_label = Label(self, 
            text="Date"
        ).grid(row=1, column=4)
        
        m = 2 
        for flight in self.master.selected_trip[0][0]:
            self.each_origin_label = Label(self,
                text=flight.origin
            ).grid(row=m, column=0)

            self.each_destination_label = Label(self,
                text=flight.destination
            ).grid(row=m, column=1)

            self.each_departure_label = Label(self,
                text=str(flight.departure)
            ).grid(row=m, column=2)

            self.each_arrival_label = Label(self,
                text=str(flight.arrival)
            ).grid(row=m, column=3)

            self.each_date_label = Label(self,
                text=str(flight.date)
            ).grid(row=m, column=4)
            m += 1

        self.label1 = Label(self, 
            text=""
        ).grid(row=m+1, column=1)
        
        self.passenger_detail_summary_label = Label(self, 
            text="Passenger details", 
            font="bold"
        ).grid(row=m+2, column=0)
        
        self.passenger_name_summary_label = Label(self, 
            text="Passenger name"
        ).grid(row=m+3, column=0)
        
        self.date_of_birth_summary_label = Label(self, 
            text="Date of birth"
        ).grid(row=m+3, column=1)
        
        self.type_summary_label = Label(self, 
            text="Type"
        ).grid(row=m+3, column=2)

        self.class_summary_label = Label(self, 
            text="Class"
        ).grid(row=m+3, column=3)


        travel_class = self.master.selected_trip[0][1].travel_class

        for n, passenger in enumerate(self.master.passengers, 1):
            self.passenger_name_summary_result_label = Label(self, 
                text = passenger.name
            ).grid(
                row=n+m+3, column=0
            )
            self.date_of_birth_summary_result_label = Label(self, 
                text = str(passenger.birthdate)
            ).grid(row=n+m+3, column=1)
            
            self.type_summary_result_label = Label(self, 
                text = passenger.type.name
            ).grid(row=n+m+3, column=2)

            self.each_class_label = Label(self,
                text=TravelClass(travel_class).name
            ).grid(row=n+m+3, column=3)

        i = m+3 + len(self.master.passengers)
        
        self.label2 = Label(self, 
            text=""
        ).grid(row=i+1, column=1)

        self.contact_detail_label = Label(self, 
            text="Contact details", 
            font="bold"
        ).grid(row=i+2, column=0)
        
        self.passenger_name_contact_label = Label(self, 
            text="Passenger name"
        ).grid(row=i+3, column=0)
        
        self.email_contact_label = Label(self, 
            text="E-mail"
        ).grid(row=i+3, column=1)
        
        self.phone_contact_label = Label(self, 
            text="Phone number"
        ).grid(row=i+3, column=2)

        passenger_name = self.master.passengers[self.master.contact.index].name
        email = self.master.contact.email
        phone = self.master.contact.phone

        self.passenger_name_contact_result_label = Label(self, 
            text=passenger_name
        ).grid(row=i+4, column=0)
        
        self.email_contact_result_label = Label(self, 
            text=email
        ).grid(row=i+4, column=1)
        
        self.phone_contact_result_label = Label(self, 
            text=phone
        ).grid(row=i+4, column=2)

        self.label3 = Label(self, 
            text=""
        ).grid(row=i+5, column=1)

        self.total_price_label = Label(self, 
            text="Total price", 
            font="bold"
        ).grid(row=i+6, column=0)
        
        self.payable_amount_label = Label(self, 
            text="Payable amount : ", 
            font="bold"
        ).grid(row=i+7, column=0)
 
        total_price = self.master.selected_trip[0][1].price

        self.payable_amount_result_label = Label(self,
            text=total_price,
            font=("bold")   
        ).grid(row=i+7, column=1)

        self.label4 = Label(self, 
            text=""
        ).grid(row=i+8, column=1)

        self.choose_how_to_pay_label = Label(self, 
            text="Choose how to pay" , 
            font="bold"
        ).grid(row=i+9, column=0)

        
        self.pay_now_button = Radiobutton(self, 
            text = "Pay now", 
            variable = self.pay_now_var,
            value = True
        ).grid(row = i+10, column=0)
        
        self.hold_my_booking_button = Radiobutton(self, 
            text = "Hold my booking", 
            variable = self.pay_now_var,
            value = False
        ).grid(row=i+10, column=1)

        self.label5 = Label(self, 
            text=""
        ).grid(row=i+11, column=1)

        self.cancel_button = Button(self, 
            text="Cancel", 
            command = self.cancel
        ).grid(row=i+12, column=0)
        
        self.purchase_button = Button(self, 
            text="Purchase", 
            command=self.next
        ).grid(row=i+12, column=1)


class PaymentPage(Page):
    master: ReviewSection
    
    def pay(self):
        requests.post(
            f'{url}/account/{self.root.username}/payment', 
            params={'method': PaymentMethod},
            json={
                'card_number': ...
            }
        )
        self.next()

    def add_widgets(self):
        self.label1 = Label(self, 
            text="Fill payment details"
        ).grid(row=0, column=0) 

        self.payment_detail_lable = Label(self, 
            text="Payable amount:"
        ).grid(row=1, column=0)

        self.method_label = Label(self, 
            text="Payment Method:"
        ).grid(row=2, column=0)
        self.method_combobox = Combobox(self,
            height=5, width=15,
            values=["Cradit card", "Master card"]
        ).grid(row=2, column=1)

        self.firstname_label = Label(self, 
            text="Firstname:"
        ).grid(row=4, column=0)
        self.firstname_entry = Entry(self).grid(row=4, column=1)

        self.lastname_label = Label(self, 
            text="Lastname:"
        ).grid(row=5, column=0)
        self.lastname_entry = Entry(self).grid(row=5, column=1)

        self.label2 = Label(self, 
            text=""
        ).grid(row=6, column=1)

        self.card_number_label = Label(self, 
            text="Card number:"
        ).grid(row=7, column=0)
        self.card_number_entry = Entry(self).grid(row=7, column=1)
        
        self.expiration_date_label = Label(self, 
            text="Expiration date(YYYY-MM-DD):"
        ).grid(row=8, column=0)
        self.expiration_date_entry = Entry(self).grid(row=8, column=1)
        
        self.verification_label = Label(self, 
            text="Verification number:"
        ).grid(row=9, column=0)
        self.verification_entry = Entry(self).grid(row=9, column=1)
        self.label1 = Label(self, 
            text="Fill payment details"
        ).grid(row=0, column=0) 

        self.payment_detail_lable = Label(self, 
            text="Payable amount:"
        ).grid(row=1, column=0)

        self.method_label = Label(self, 
            text="Payment Method:"
        ).grid(row=2, column=0)
        self.method_combobox = Combobox(self,
            height=5, width=15,
            values=["Cradit card", "Master card"]
        ).grid(row=2, column=1)

        self.firstname_label = Label(self, 
            text="Firstname:"
        ).grid(row=4, column=0)
        self.firstname_entry = Entry(self).grid(row=4, column=1)

        self.lastname_label = Label(self, 
            text="Lastname:"
        ).grid(row=5, column=0)
        self.lastname_entry = Entry(self).grid(row=5, column=1)

        self.label2 = Label(self, 
            text=""
        ).grid(row=6, column=1)

        self.card_number_label = Label(self, 
            text="Card number:"
        ).grid(row=7, column=0)
        self.card_number_entry = Entry(self).grid(row=7, column=1)
        
        self.expiration_date_label = Label(self, 
            text="Expiration date(YYYY-MM-DD):"
        ).grid(row=8, column=0)
        self.expiration_date_entry = Entry(self).grid(row=8, column=1)
        
        self.verification_label = Label(self, 
            text="Verification number:"
        ).grid(row=9, column=0)
        self.verification_entry = Entry(self).grid(row=9, column=1)
        
        self.back_button = Button(self, 
            text="Back", 
            command=self.back
        ).grid(row=2, column=0)

        self.purchase_button = Button(self, 
            text="Purchase", 
            command=self.pay
        ).grid(row=10, column=1)


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


    def select(self):
        
        self.next()

    def add_widgets(self):
        self.seat_frame = Frame(self).pack(side=RIGHT)

        for seat in self.seats:
            seat = Button(self.seat_frame, 
                text=seat.number, 
                command=partial(self.select, ...)
            ).pack(side=LEFT)