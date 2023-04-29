from app.spawn import *


def generate():
    Airline()
    for func in functions: 
        func()
        
def print_results(results: list[FlightItinerary]):
    for itinerary in results:
        print('-', end=' ')
        for instance in itinerary:
            flight = instance.flight
            print(
                f'{flight.designator: <6} {instance.date} | {flight.origin.location_code} {flight.departure} -> {flight.destination.location_code} {flight.arrival}  ',
                end=' '
            )
        print()
        
    
if __name__ == '__main__' and 0:
    Airline.load()
    results = search('bkk', 'icn')
    # print_results(search('sin', 'doh'))
    # print_results(search('LHR', 'cai'))
    # print_results(search('sfo', 'sin'))
    # print_results(search('zrh', 'icn'))
    # print_results(search('zrh', 'bkk'))
    # print_results(search('bkk', 'icn'))
    # print_results(search('bkk', 'vie'))
    
    plum = Airline.accounts.get('Plum123')
    assert isinstance(plum, Customer)

    passenger1 = Passenger(
        'Plum', 'Arpleum',
        dt.date(1999, 1, 1),
        'Thai', '254123543',
        GenderType.MALE,
        PassengerType.ADULT,
    )
    contact1 = ContactInformation(
        passenger1, 
        '0812345678', 
        '516516@kmitl.com'
    )
    Airline.create_booking(
        plum, contact1, [passenger1], [
            (results[0], TravelClass.ECONOMY)
        ], 
    )
    booking = plum.bookings[0]
    reservation = next(booking.all_reservations)
    instance = reservation.provider.host

    seats = instance.aircraft.all_seats
    seatiter = iter(seats)
    seat1 = next(seatiter)

    Airline.select_seats(
        reservation, [
            (passenger1, seat1)
        ]
    )