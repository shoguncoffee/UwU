r"""
interface of main package (UwU/app)

for this package:
- `\UwU> python -m app`


for individual submodule in this package:
- `\UwU> python -m app.<module>`
"""
from app.airline import Airline

# if new system?
if True:
    system = Airline('UwU Airline', 'UW')
    
    from app.utils.spawn import *

    add_airports(system)
    add_aircrafts(system)
    add_flights(system)
    add_flight_plans(system)
    add_accounts(system)


    ### test flight seaching
    # print_results(search(system, 'sin', 'doh'))
    # print_results(search(system, 'LHR', 'cai'))
    # print_results(search(system, 'sfo', 'sin'))
    # print_results(search(system, 'zrh', 'icn'))
    # print_results(search(system, 'zrh', 'bkk'))
    # print_results(search(system, 'bkk', 'icn'))
    # print_results(search(system, 'bkk', 'vie'))
    

    ### example of booking
    
    results = search(system, 'bkk', 'icn')
    
    plum = system.accounts.get('Plum123')
    
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
    
    # user choice first result with economy class
    choosen_itinerary = results[0], TravelClass.ECONOMY

    # create booking
    booking_id = system.create_booking(
        plum, contact1, [passenger1], [choosen_itinerary], 
    )

    # check booking is created; if can't create booking it will return None
    assert booking_id is not None

    # get booking instance from booking reference (id)
    booking = plum.get_booking(booking_id)

    # confirm pending, change status from incomplete to pending
    system.pending_booking(booking)

    # pick reservation of first flight in this booking
    reservation = booking.all_reservations[0]

    # get flightclass of that reservation
    flightclass = reservation.provider

    # get all remaining seats of that flightclass
    seats = flightclass.get_remain_seats()

    # pick first available seat
    seat1 = next(iter(seats))

    # choose seat and passenger
    choosen_seat = passenger1, seat1
    
    # select seat for this reservation
    system.select_seats(
        reservation, [choosen_seat]
    )
    
    system.pay(booking, {})

    import pickle
    with open('data/system.pkl', 'wb') as f:
        pickle.dump(system, f)


else:
    # เฉพาะกรณีต้องการโหลดข้อมูลจากไฟล์
    import pickle
    
    with open('data/system.pkl', 'rb') as f:
        system: Airline = pickle.load(f)