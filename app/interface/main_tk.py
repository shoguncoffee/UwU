"""
https://tkdocs.com/tutorial/concepts.html
http://tkdocs.com/pyref/index.html
"""
from __future__ import annotations
from .base import *


class MenuPage(StaticPage):
    master: Root
    
    def add_widgets(self):
        Label(self, 
            text="UwU Airline", 
            font="Bold 20",
        ).pack()
        
        Button(self, 
            command=partial(self.jump, BookingSection), 
            width=15,
            text="Search Flight",
        ).pack()
        
        Button(self, 
            command=partial(self.jump, LoginPage), 
            width=15,
            text="Login",
        ).pack()
        
        Button(self,
            command=partial(self.jump, ViewBookingSection),
            width=15,
            text="View Booking"
        ).pack()


class LoginPage(StaticPage):
    master: Root

    def submit(self):
        username = self.username_entry.get()
        response = requests.post(URL + API_EndPoint2, params={
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
            width=10,
        ).pack()
        
        self.register_button = Button(self, 
            command=partial(self.jump, RegisterPage), 
            text="Register",
            width=10,
        ).pack()
        
        self.back_button = Button(self, 
            command=partial(self.jump, MenuPage), 
            text="Back",
            width=10,
        ).pack()
        
        self.response_label = Label(self, 
            text="",
        ).pack()


class RegisterPage(StaticPage):
    master: Root

    def submit(self):
        response = requests.post(URL + API_EndPoint1, params={
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
        
        passengers, contact, want_select_seat = self.open(
            PassengerSection(self, pax)
        ).returned()
        booking_id = self.create_booking(passengers, contact, selected_trip)
                
        if want_select_seat:
            self.open(
                SelectSeatSection(self, self.root.get_booking(booking_id))
            ).returned()
        
        self.open(
            ReviewSection(self, self.root.get_booking(booking_id))
        )
        self.jump(MenuPage)

    def create_booking(self,
        passengers: list[body.PassengerBody],
        contact: body.ContactInfoBody,
        selected_trip: list[tuple[list[body.FlightInfoBody],  TravelClass]],
    ):
        prebooking = body.PreBookingBody(
            contact = contact,
            passengers = passengers,
            journey = [(
                    [flight.reduce() for flight in flights], travel_class
                ) for flights, travel_class in selected_trip
            ],
        )
        response = requests.post(
            f'{URL}/account/{self.root.username}/book', 
            prebooking.json()
        )
        return UUID(response.json())


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
        return self.pax, [(self.flights, self.classinfo.travel_class)] #!


class SearchPage(Page):
    master: SearchSection

    def predefine(self):
        super().predefine()
        self.trip_type = tk.IntVar(self)

    def returned(self):
        super().returned()
        trip = self.trip_type.get()
        departure_day = self.departure_day_spinbox.get()
        departure_month = self.departure_month_spinbox.get()
        departure_year = self.departure_year_spinbox.get()
        
        pax = src.Pax({
            passenger_type: int(spinbox.get())
            for passenger_type, spinbox in self.pax_spinbox.items()
        }.items())
        
        response = requests.get(URL + API_Endpoint3, params={
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
        
        Radiobutton(self,
            text = 'One Way',
            variable = self.trip_type,
            value = 0
        ).grid(row=1, column=2,)
        
        Radiobutton(self,
            text = 'Return',
            variable = self.trip_type,
            value = 1
        ).grid(row=2, column=2,)

        
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
                text = passenger_type.name
            ).grid(row=row, column=5)
            spinbox.grid(row=row, column=6)


        self.search_button = Button(self, 
            command = self.next, 
            text = "Search",
        ).grid(row=4, column=2,)
        
        self.back_button = Button(self, 
            command = partial(self.master.jump, MenuPage), 
            text = "Back to Menu",
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
            text="Origin",
            width=11,
        ).grid(row=0, column=1)
        
        self.destination_label = Label(self, 
            text="Destination",
            width=11,
        ).grid(row=0, column=2)
        
        self.departure_label = Label(self, 
            text="Departure",
            width=11,
        ).grid(row=0, column=3)
        
        self.arrival_label = Label(self, 
            text="Arrival",
            width=11,
        ).grid(row=0, column=4)
        
        self.economy_label = Label(self, 
            text="Economy",
            width=11,
        ).grid(row=0, column=5)
        
        self.business_label = Label(self, 
            text="Business",
            width=11,
        ).grid(row=0, column=6)
        
        self.first_label = Label(self, 
            text="First",
            width=11,
        ).grid(row=0, column=7)
        
        self.back_button = Button(self, 
            command=self.back,
            text="Search Flight",
        ).grid(row=0, column=0)
        
        for row, itinerary in enumerate(self.itinerarys, 1):
            first_flight = itinerary.flights[0]
            last_flight = itinerary.flights[-1]

            origin = first_flight.origin
            departure = first_flight.departure
            destination = last_flight.destination
            arrival = last_flight.arrival

            Label(self, 
                text = 'Non-Stop' if (n := len(itinerary.flights)) == 1 else f'{n-1} Stop'
            ).grid(row=row, column=0)

            Label(self, 
                text = origin
            ).grid(row=row, column=1)
            
            Label(self, 
                text = destination
            ).grid(row=row, column=2)
            
            Label(self, 
                text = f'{departure:%H:%M}'
            ).grid(row=row, column=3)
            
            Label(self, 
                text = f'{arrival:%H:%M}'
            ).grid(row=row, column=4)
            
            for data in itinerary.classes:
                travel_class = data.travel_class
                select = Button(self, 
                    text = data.price,
                    command = partial(self.choose, itinerary, travel_class)
                ).grid(row=row, column=travel_class + 4)

                if not data.seat_left:
                    select['state'] = 'disabled'
                
                elif data.seat_left < 20: # show seat left
                    ...


class PassengerSection(SubSection):    
    def __init__(self, master, pax: src.Pax):
        self.pages = [(
            type(f'{FillPassengerPage.__name__}{n}', (FillPassengerPage,), {}), passenger_type
            ) for passenger_type, number in pax for n in range(number)
        ]
        super().__init__(master)

    def returned(self):
        return self.passengers, self.contact, self.want_select_seat

    def procedure(self):
        self.passengers: list[body.PassengerBody] = []
        
        for n, (FillPage, passenger_type) in enumerate(self.pages):
            page = self.peek(
                FillPage(self, passenger_type, n)
            )
            self.passengers.append(page.returned())

        self.contact, self.want_select_seat = self.peek(
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
        self.want_select_seat = False
        self.passengers_name = {
            passenger.name: n for n, passenger in enumerate(passengers)
            if passenger.type is PassengerType.ADULT
        }
        super().__init__(master)

    def returned(self):
        super().returned()
        return body.ContactInfoBody(
            index = self.passengers_name[self.contact_combobox.get()],
            phone = self.phone_entry.get(),
            email = self.email_entry.get()
        ), self.want_select_seat

    def select_seat(self):
        self.want_select_seat = True
        self.next()
        
    def add_widgets(self):
        self.contact_combobox = Combobox(self,
            height = 5, width = 20,
            values = list(self.passengers_name),
            state = 'readonly',
        ).grid(row=18,column=1)

        self.contact_detail_label = Label(self, 
            text="Contact details"
        ).grid(row=15, column=0)
          
        self.next_button = Button(self, 
            text="summery", 
            command=self.next,
        ).grid(row=19, column=1)
        
        if self.root.username is None:
            self.next_button['state'] ='disabled'
        
        self.phone_entry = Entry(self
        ).grid(row=17, column=0)

        self.email_entry = Entry(self,
            width = 20,
        ).grid(row=17, column=1)

        self.back_button = Button(self, 
            text = 'cancel', 
            command = partial(self.jump, MenuPage)
        ).grid(row=19, column=0)

        self.select_seat_button = Button(self, 
            text="Select seat", 
            command=self.select_seat
        ).grid(row=19, column=2)
        
        self.contact_combobox.insert(0, "Choose whose contact")
        self.phone_entry.insert(0, "Phone number")
        self.email_entry.insert(0, "Email address") 


class ReviewSection(SubSection):
    def __init__(self, master, booking: body.BookingInfoBody):
        self.booking = booking
        super().__init__(master)

    def procedure(self):
        confirm, paynow = self.peek(SummeryPage(self)).returned()

        if confirm:
            self.pend_booking()
            if paynow:
                self.peek(PaymentPage(self)).returned()
        else:
            self.temp_booking()

    def pend_booking(self):
        if self.booking.status is BookingStatus.INCOMPLETE:
            requests.put(f'{URL}/account/{self.root.username}/{self.booking.reference}/pend')

    def temp_booking(self):
        if self.booking.status is BookingStatus.INCOMPLETE:
            requests.delete(f'{URL}/account/{self.root.username}/{self.booking.reference}/temp')


class SummeryPage(Page):
    master: ReviewSection

    def returned(self):
        super().returned()
        return self.confirm, self.pay_now_var.get(), 

    def cancel(self):
        self.confirm = False
        self.next()

    def predefine(self):
        super().predefine()
        self.confirm = True
        self.pay_now_var = tk.BooleanVar(self)
        
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
        for segment in self.master.booking.segments:
            for reservation in segment:
                flight = reservation.flight
                
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

        self.seat_summary_label = Label(self, 
            text="Seat"
        ).grid(row=m+3, column=4)

        travel_class = self.master.booking.segments[0][0].travel_class

        for n, passenger in enumerate(self.master.booking.passengers, 1):
            seat = self.master.booking.segments[0][0].selected[n-1]
            if seat is not None:
                seat = seat.number
            else:
                seat = 'Not specified'

            self.seleted_seat_label = Label(self,
                text=seat
            ).grid(row=n+m+3, column=4)
            
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

            

        i = m+3 + len(self.master.booking.passengers)
        
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

        contact = self.master.booking.contact
        passenger_name = self.master.booking.passengers[contact.index].name
        email = contact.email
        phone = contact.phone

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
 
        total_price = self.master.booking.price

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
        respone = requests.post(
            f'{URL}/account/{self.root.username}/{self.master.booking.reference}/payment', 
            params={'method': PaymentMethod.CREDIT_CARD},
            json={
                'data': {
                    'method': self.method_combobox.get(),
                    'card_holder_firstname': self.firstname_entry.get(),
                    'card_holder_lastname': self.lastname_entry.get(),
                    'card_number': self.card_number_entry.get(),
                    'expiration_date': self.expiration_date_entry.get(),
                    'verification_number': self.verification_entry.get()
                }
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

        self.total_price_label = Label(self,
            text=self.master.booking.price
        ).grid(row=1, column=1)

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
        ).grid(row=10, column=0)

        self.purchase_button = Button(self, 
            text="Purchase", 
            command=self.pay
        ).grid(row=10, column=1)


class SelectSeatSection(SubSection):
    def __init__(self, master, booking: body.BookingInfoBody):
        self.booking = booking
        super().__init__(master)

    def procedure(self):
        for segment_index, segment in enumerate(self.booking.segments):
            for reservation_index, reservation in enumerate(segment):
                selected_seats: list[str] = []
                available_seats = self.get_avaliable_seats(reservation.flight, reservation.travel_class)
                
                for passenger in self.booking.passengers:
                    seat = self.peek(
                        SelectSeatPage(self, passenger, reservation, available_seats)
                    ).returned()
                    available_seats.remove(seat)
                    selected_seats.append(seat)

                self.selecting(
                    segment_index, 
                    reservation_index,
                    selected_seats
                )

    def selecting(self, 
        segment_index: int,
        reservation_index: int,
        seats: list[str]
    ):
        response = requests.post(
            f'{URL}/account/{self.root.username}/{self.booking.reference}/select-seat', 
            json=seats, params={
                'segment_index': segment_index,
                'reservation_index': reservation_index,
            },
        )
        
    def get_avaliable_seats(self, flight: body.FlightInfoBody, travel_class: TravelClass) -> list[str]:
        response = requests.get(f'{URL}/avaliable-seat', params={
                'date': flight.date.isoformat(),
                'designator': flight.designator,
                'travel_class': travel_class,
            }
        )
        return response.json()


class SelectSeatPage(Page):
    def __init__(self, master, 
        passenger: body.PassengerBody,
        reservation: body.FlightReservationBody,
        avaliable_seats: list[str],
    ):
        self.passenger = passenger
        self.reservation = reservation
        self.avaliable_seats = avaliable_seats
        super().__init__(master)

    def select(self):
        self.seat = self.selected_seats_entry.get()
        self.next()

    def returned(self):
        super().returned()
        return self.seat

    def add_widgets(self):
        flight = self.reservation.flight
        travel_class = self.reservation.travel_class
        
        model = flight.aircraft_model
        aircraft = self.root.aircraft[model]
        cabin_no, cabin = next(
            (n, cabin) for n, cabin in enumerate(aircraft.decks[0])
            if cabin.travel_class == travel_class
        )
        
        Label(self,
            text = f'aircraft: {model}'
        ).pack()
        Label(self,
            text = f'cabin no.{cabin_no}'
        ).pack()
        Label(self,
            text = f'passenger: {self.passenger.name}'
        ).pack()
        
        
        seat_frame = Frame(self).pack()
        Label(seat_frame,
            text = 'avaliable seats: '+ ', '.join(self.avaliable_seats)
        ).pack()

        
        # for seat in self.seats:
        #     seat = Button(self.seat_frame, 
        #         text = seat.number, 
        #         command = partial(self.select, )
        #     ).pack(side=LEFT)

        self.confirm_frame = Frame(self).pack()

        self.selected_seats_label = Label(
            self.confirm_frame,
            text='Selected seats: '               
        ).grid(row=0, column=0)
        
        self.selected_seats_entry = Entry(
            self.confirm_frame,
        ).grid(row=0, column=1)

        self.confirm_button = Button(
            self.confirm_frame,
            text='Confirm selection',
            command=self.select
        ).grid(row=2, column=1)
                

class ViewBookingSection(SubSection):
    def procedure(self):
        self.all_bookings = self.get_all_bookings()
        
        selected = self.peek(
            ViewBookingsPage(self)
        ).returned()

        if selected: 
            booking = self.root.get_booking(selected)
            will_pay = self.peek(
                BookingPage(self, booking)
            ).returned()
            
            if will_pay:
                self.peek(
                    ReviewSection(self, booking)
                )
        self.jump(MenuPage)
        
    def get_all_bookings(self):
        response = requests.get(f'{URL}/account/{self.root.username}/my-bookings')
        return [
            body.BookingBody(**data) for data in response.json()
        ]


class ViewBookingsPage(Page):
    master: ViewBookingSection

    def __init__(self, master):
        self.selected_id = None
        super().__init__(master)

    def choose(self, selected_id: UUID):
        self.selected_id = selected_id
        self.next()

    def returned(self):
        super().returned()
        return self.selected_id
    
    def add_widgets(self):
        top_frame = Frame(self).pack(side=TOP)
        
        self.label1 = Label(top_frame,
            text="View Booking"                   
        ).pack()
        
        Button(top_frame,
            text='back',
            command=self.next
        ).pack(side=LEFT)
        
        for booking in self.master.all_bookings:
            button = LabelFrame(self,
                text=f'{booking.datetime: %d %b %Y %H:%M}'
            ).pack(ipadx=5, ipady=5, padx=5, pady=6)

            Button(button, 
                text=booking.status.name,
                width=12,
                command=partial(self.choose, booking.reference)
            ).pack(side=LEFT)
            
            Label(button, 
                text=' '.join(f'{type.name} {number}' for type, number in booking.pax),
                width=9,
            ).pack(side=LEFT)            
            
            itinerary = Frame(button).pack(side=RIGHT)
            for n, (origin, destination, departure, arrival) in enumerate(booking.trip):
                Label(itinerary, 
                    text=f'{origin.code} -> {destination.code}',
                    width=15,
                ).grid(row=n, column=0)
                
                Label(itinerary, 
                    text=f'{departure: %a, %d %b %Y} - {arrival: %a, %d %b %Y}',
                    width=15,
                ).grid(row=n, column=35)


class BookingPage(Page):
    master: ViewBookingSection

    def __init__(self, master, booking: body.BookingInfoBody):
        self.booking = booking
        self.will_pay = False
        super().__init__(master)

    def pay(self):
        self.will_pay = True
        self.next()

    def returned(self):
        super().returned()
        return self.will_pay

    def cancel(self):
        ...
    
    def add_widgets(self):        
        self.label1 = Label(self,
            text="Booking details", 
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
        for segment in self.booking.segments:
            for reservation in segment:
                flight = reservation.flight
                
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

        self.seat_summary_label = Label(self, 
            text="Seat"
        ).grid(row=m+3, column=4)

        travel_class = self.booking.segments[0][0].travel_class

        for n, passenger in enumerate(self.booking.passengers, 1):
            
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

            seat = self.booking.segments[0][0].selected[n-1]
            if seat is not None:
                seat = seat.number
            else:
                seat = 'Not specified'

            self.seleted_seat_label = Label(self,
                text=seat
            ).grid(row=n+m+3, column=4)

        i = m+3 + len(self.booking.passengers)

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

        contact = self.booking.contact
        passenger_name = self.booking.passengers[contact.index].name
        email = contact.email
        phone = contact.phone

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

        total_price = self.booking.price
        payment = self.booking.payment

        self.payable_amount_result_label = Label(self,
            text=total_price,
            font=("bold")   
        ).grid(row=i+7, column=1)

        self.back_button = Button(self,
            text="Back",
            command=self.back
        ).grid(row=i+11, column=0)

        if payment is None:
            self.paybutton = Button(self,
                text="pay",
                command=self.pay
            ).grid(row=i+11, column=1)

            self.cancel_booking_button = Button(self,
                text='Cancel booking',
                command=self.cancel
            ).grid(row=i+11, column=2)
        else:
            self.payment_label = Label(self,
                text="Payment: ",                           
            ).grid(row=i+8, column=0)

            self.transaction_id_label = Label(self,
                text="Transaction ID: ",                           
            ).grid(row=i+9, column=0)

            self.payment_time_label = Label(self,
                text="Payment time: ",                           
            ).grid(row=i+10, column=0)

            self.payment_result_label = Label(self,
                text=payment.status,  
            ).grid(row=i+8, column=1)

            self.transaction_id_result_label = Label(self,
                text=str(payment.transaction_id),                           
            ).grid(row=i+9, column=1)

            self.payment_time_result_label = Label(self,
                text=str(payment.payment_time),                           
            ).grid(row=i+10, column=1)  