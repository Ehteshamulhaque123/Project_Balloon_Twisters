from business_layer import *
from data_layer import *

class BookingApp:
    def __init__(self):
        self.twisters = read_balloon_twisters("BalloonTwisters.dat")
        self.holidays = read_holidays("Holidays.dat")
        self.schedule = read_schedule("Schedule.csv")
        self.waiting_list = read_waiting_list("WaitingList.csv")

    def schedule_customer(self):
        print("Available holidays:")
        for holiday in self.holidays:
            print(holiday.name)
        print("----------------------")
        customer = input("Enter customer's name: ").strip()
        holiday = input("Enter holiday name: ").strip()
        
        existing_booking = None
        twister = find_available_twister(self.schedule, holiday, self.twisters)

# Check if there's an existing booking for this holiday
        existing_booking = any(booking.holiday == holiday for bookings in self.schedule.values() for booking in bookings)

        if existing_booking:
            add_to_waiting_list(self.waiting_list, customer, holiday)
            print(f"No available twister for {holiday}")
            print(f"Added {customer} to waiting list for {holiday}.")
            save_waiting_list("WaitingList.csv", self.waiting_list)
        else:
            twister = find_available_twister(self.schedule, holiday, self.twisters)
            if twister:
                add_booking_to_schedule(self.schedule, customer, holiday, twister.name)
                print(f"Booking made: {customer} - {holiday} - {twister.name}")
                save_schedule("Schedule.csv", self.schedule)
            else:
                add_to_waiting_list(self.waiting_list, customer, holiday)
                print(f"No available twister for {holiday}. Added {customer} to waiting list.")
                save_waiting_list("WaitingList.csv", self.waiting_list)
    def cancel_reservation(self):
        customer = input("Enter customer's name: ").strip()
        holiday = input("Enter holiday name: ").strip()
        bookings = self.schedule.get(holiday, [])
        new_schedule = []
        found_waiting_customer = False

        for booking in bookings:
            if booking.customer == customer:
                found_waiting_customer = True
            else:
                new_schedule.append(booking)

        if found_waiting_customer:
            print(f"Reservation canceled for {customer} on {holiday}.")
            self.schedule[holiday] = new_schedule
            save_schedule("Schedule.csv", self.schedule)
        twister_schedule = get_schedule_for_twister(self.schedule, booking.twister)
        if self.waiting_list and twister_schedule:
            waiting_customer, waiting_holiday = self.waiting_list.popleft()
            if waiting_holiday not in self.schedule:
                self.schedule[waiting_holiday] = []
            self.schedule[waiting_holiday].append(Booking(waiting_customer, waiting_holiday, booking.twister))
            print(f"Rescheduled waiting customer: {waiting_customer} - {waiting_holiday} - {booking.twister}")
            save_schedule("Schedule.csv", self.schedule)
                
        else:
            print(f"No reservation found for waiting customer on {holiday}.")

        save_waiting_list("WaitingList.csv", self.waiting_list)

    def show_status(self):
        search_param = input("Enter the name of a balloon twister or holiday: ").strip()
        twister_schedule = get_schedule_for_twister(self.schedule, search_param)
        holiday_schedule = get_schedule_for_holiday(self.schedule, search_param)

        if twister_schedule:
            print(f"Schedule for {search_param}:")
            for booking in twister_schedule:
                print(f"{booking.customer} - {booking.holiday}")
        elif holiday_schedule:
            print(f"Schedule for {search_param}:")
            for booking in holiday_schedule:
                print(f"{booking.customer} - {booking.twister}")
        else:
            print(f"No schedule found for {search_param}.")

    def signup_twister(self):
        twister_name = input("Enter the name of the new balloon twister: ").strip()
        add_twister_to_list(self.twisters, twister_name)
        save_balloon_twisters("BalloonTwisters.dat", self.twisters)
        print(f"New balloon twister signed up: {twister_name}")

    def twister_dropout(self):
        twister_name = input("Enter the name of the balloon twister to dropout: ").strip()

        available_twister = None

        for twister in self.twisters:
            if twister.name != twister_name and not any(booking.twister == twister.name for bookings in self.schedule.values() for booking in bookings):
                available_twister = twister
                break

        if available_twister:
            rescheduled_customers = []
            for holiday, bookings in self.schedule.items():
                for booking in bookings:
                    if isinstance(booking, Booking) and booking.twister == twister_name:
                        self.schedule[holiday].remove(booking)
                        rescheduled_customers.append((booking.customer, holiday))
                        self.schedule[holiday].append(Booking(booking.customer, holiday, available_twister.name))
                        print(f"Rescheduled customer: {booking.customer} - {holiday} - {available_twister.name}")
            self.twisters = [twister for twister in self.twisters if twister.name != twister_name]
            save_balloon_twisters("BalloonTwisters.dat", self.twisters)
            save_schedule("Schedule.csv", self.schedule)
            save_waiting_list("WaitingList.csv", self.waiting_list)
            print(f"{twister_name} has dropped out.")
        else:
            print(f"No available twister without reservations. Customers will be added to the waiting list.")

            for holiday, bookings in self.schedule.items():
                for booking in bookings:
                    if isinstance(booking, Booking) and booking.twister == twister_name:
                        add_to_waiting_list(self.waiting_list, booking.customer, holiday)
                        print(f"Added customer to waiting list: {booking.customer} - {holiday}")
                        self.schedule[holiday].remove(booking)  # Remove customer's booking from the schedule

              # Remove twister from the dat file
            self.twisters = [twister for twister in self.twisters if twister.name != twister_name]
            save_balloon_twisters("BalloonTwisters.dat", self.twisters)
            save_schedule("Schedule.csv", self.schedule)
            save_waiting_list("WaitingList.csv", self.waiting_list)
            print(f"{twister_name} has dropped out.")



    def run(self):
        while True:
            print("\nMenu:")
            print("1. SCHEDULE (customer) (holiday)")
            print("2. CANCEL (customer) (holiday)")
            print("3. STATUS (balloon twister or holiday)")
            print("4. QUIT")
            print("5. SIGNUP (balloon twister)")
            print("6. DROPOUT (balloon twister)")

            choice = input("Enter your choice: ").strip().upper()

            if choice == "1":  # SCHEDULE
                self.schedule_customer()

            elif choice == "2":  # CANCEL
                self.cancel_reservation()

            elif choice == "3":  # STATUS
                self.show_status()

            elif choice == "4":  # QUIT
                save_schedule("Schedule.csv", self.schedule)
                save_waiting_list("WaitingList.csv", self.waiting_list)
                print("Schedule and waiting list saved. Program terminated.")
                break

            elif choice == "5":  # SIGNUP
                self.signup_twister()

            elif choice == "6":  # DROPOUT
                self.twister_dropout()

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = BookingApp()
    app.run()
