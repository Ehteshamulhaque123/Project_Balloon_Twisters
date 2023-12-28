import csv
from business_layer import *
def read_balloon_twisters(filename):
    with open(filename, 'r') as file:
        return [BalloonTwister(line.strip()) for line in file]

def read_holidays(filename):
    with open(filename, 'r') as file:
        return [Holiday(line.strip()) for line in file]

def read_schedule(filename):
    schedule = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            holiday_name, customer_name, twister_name = row
            booking = Booking(customer_name, holiday_name, twister_name)
            if holiday_name not in schedule:
                schedule[holiday_name] = []
            schedule[holiday_name].append(booking)
    return schedule

def save_schedule(filename, schedule):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for holiday_name, bookings in schedule.items():
            for booking in bookings:
                writer.writerow([holiday_name, booking.customer, booking.twister])

def save_balloon_twisters(filename, twisters):
    with open(filename, 'w') as file:
        for twister in twisters:
            file.write(twister.name + '\n')
