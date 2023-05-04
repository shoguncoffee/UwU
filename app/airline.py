from app.base import *
from app.src import *


class Airline:
    """represent the system of this project"""
    
    def __init__(self, name: str, designator: str):
        self.__name = name
        self.__designator = designator
        self.__aircrafts = AircraftCatalog()
        self.__airports = AirportCatalog()
        self.__accounts = AccountCatalog()
        self.__flights = FlightCatalog()
        self.__schedules = ScheduleCatalog()
        self.__plans = FlightScheduling()

    @property
    def name(self):
        return self.__name

    @property
    def designator(self):
        return self.__designator
    
    @property
    def schedules(self):
        return self.__schedules
    
    @property
    def flights(self):
        return self.__flights
    
    @property
    def accounts(self):
        return self.__accounts
    
    @property
    def aircrafts(self):
        return self.__aircrafts
    
    @property
    def airports(self):
        return self.__airports
    
    @property
    def plans(self):
        return self.__plans

    def update_flight(self, *plans: FlightPlan):
        for date in daterange(self.plans.advance_days):
            try:
                schedule = self.schedules.get(date)
            except KeyError:
                schedule = ScheduleDate(date)
                self.schedules.append(schedule)
            
            for plan in self.plans.on_date(date, plans):
                schedule.add(
                    FlightInstance(date, 
                        plan.flight, 
                        plan.default_aircraft, 
                        deepcopy(plan.default_fares)
                    )
                )
    
    def create_booking(self,
        creator: Customer,
        contact: ContactInformation,
        passengers: Sequence[Passenger],
        journey: Sequence[tuple[FlightItinerary, TravelClass]]
    ):
        pax = Pax.count(passengers)
        if all(
            itinerary.bookable(pax, travel_class) 
            for itinerary, travel_class in journey
        ):
            booking = Booking(creator, contact, passengers, journey)
            
            for reservation in booking.all_reservations:
                flightclass = reservation.provider
                flightclass.booked(reservation)
            
            creator.bookings.append(booking)
            return booking.reference
    
    def cancel_booking(self, booking: Booking):
        match booking.status:
            case BookingStatus.INCOMPLETE:
                customer = booking.creator
                customer.bookings.remove(booking)
            
            case BookingStatus.PENDING:
                booking.cancel()

            case _:
                return False
            
        return True

    def pending_booking(self, booking: Booking):
        if booking.status is BookingStatus.INCOMPLETE:
            booking.pending()
            return True
    
    def select_seats(self, 
        reservation: FlightReservation,
        selected: list[tuple[Passenger, Seat]],
    ):
        flightclass = reservation.provider
        booking = reservation.holder
        
        if flightclass.bookable(booking.get_pax()):
            occupied = flightclass.get_occupied_seats()
            selected_seats = [seat for _, seat in selected]
            
            if not occupied.intersection(selected_seats):
                return reservation.assign_seats(
                    SeatReservation(passenger, seat) for passenger, seat in selected
                )
    
    def pay(self, 
        booking: Booking,
        data: dict,
    ):
        if not booking.payment:
            payment = Payment.pay(booking, **data)
            booking.update_payment(payment)
            return True
    
    def register(self, account: Customer):
        if account not in self.accounts:
            self.accounts.append(account)
            return True
    
    def login(self, username: str, password: str):
        account = self.accounts.get(username)
        return account.password == password
    
    def search_journey(self,
        origin: Airport, 
        destination: Airport, 
        date: dt.date,
        pax: Pax = Pax(),
    ): 
        """
        return a list of FlightItinerary by any possible FlightInstance
        that can take from origin to destination in limit duration
            - limit: `datetime.timedelta`
                - maximum flight time of the path (not including transit time)
        """
        from .utils import algorithm

        pool = chain.from_iterable(
            self.schedules.get(day) for day in daterange(2, date)
        )
        searcher = algorithm.SearchHelper(origin, destination, date, list(pool))
        
        bookable = [
            itinerary for itinerary in searcher.result() if itinerary.bookable(pax)
        ]
        unique_departure = {
            itinerary.departure for itinerary in bookable
        }
        per_departure = [
            sorted(
                itinerary for itinerary in bookable if itinerary.departure == departure
            ) for departure in unique_departure
        ]
        return sorted(cheapest for cheapest, *_ in per_departure)