from collections import deque

class BalloonTwister:
    def __init__(self, name):
        self.name = name

class Holiday:
    def __init__(self, name):
        self.name = name

class Booking:
    def __init__(self, customer, holiday, twister):
        self.customer = customer
        self.holiday = holiday
        self.twister = twister

def find_available_twister(schedule, holiday, twisters):
    for twister in twisters:
        for booking in schedule.get(holiday, []):
            if booking.twister == twister.name and booking.holiday==holiday:
                break
        else:
            return twister
    return None

def add_booking_to_schedule(schedule, customer, holiday, twister):
    booking = Booking(customer, holiday, twister)
    if holiday not in schedule:
        schedule[holiday] = []
    schedule[holiday].append(booking)

def add_twister_to_list(twisters, twister_name):
    twisters.append(BalloonTwister(twister_name))

def add_to_waiting_list(waiting_list, customer, holiday):
    waiting_list.append((customer, holiday))

def remove_from_waiting_list(waiting_list, customer, holiday):
    waiting_list.remove((customer, holiday))

def get_schedule_for_twister(schedule, twister_name):
    return [booking for bookings in schedule.values() for booking in bookings if booking.twister == twister_name]

def get_schedule_for_holiday(schedule, holiday_name):
    return schedule.get(holiday_name, [])

def read_waiting_list(filename):
    waiting_list = deque()
    with open(filename, 'r') as file:
        for line in file:
            customer, holiday = line.strip().split(',')
            waiting_list.append((customer, holiday))
    return waiting_list

def save_waiting_list(filename, waiting_list):
    with open(filename, 'w', newline='') as file:
        for customer, holiday in waiting_list:
            file.write(f"{customer},{holiday}\n")
