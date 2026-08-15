"""
AI Hospitality Booking Assistant (Prototype)
A simple CLI prototype using state-machine style conversation logic.
All availability is mock/sample data and does not represent a real business.
"""

from datetime import date, datetime
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("mock_availability.json")


class BookingAssistant:
    def __init__(self):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.state = "START"
        self.booking = {
            "type": None,
            "date": None,
            "time": None,
            "party_size": None,
            "room_type": None,
            "guest_name": None,
        }

    def run(self):
        print("\n=== AI Hospitality Booking Assistant ===")
        print("Prototype only — availability is mock data.\n")

        while self.state != "DONE":
            if self.state == "START":
                self.choose_type()
            elif self.state == "RESTAURANT_DATE":
                self.ask_restaurant_date()
            elif self.state == "RESTAURANT_TIME":
                self.ask_restaurant_time()
            elif self.state == "RESTAURANT_PARTY":
                self.ask_party_size()
            elif self.state == "HOTEL_DATE":
                self.ask_hotel_date()
            elif self.state == "HOTEL_ROOM":
                self.ask_room_type()
            elif self.state == "HOTEL_GUESTS":
                self.ask_party_size()
            elif self.state == "CHECK_AVAILABILITY":
                self.check_availability()
            elif self.state == "CONFIRM":
                self.confirm_booking()
            elif self.state == "CANCEL":
                print("\nBooking cancelled. Thank you!")
                self.state = "DONE"

        print("\nGoodbye!")

    def choose_type(self):
        print("What would you like to book?")
        print("1. Restaurant")
        print("2. Hotel")
        choice = input("Choose 1 or 2: ").strip()

        if choice == "1":
            self.booking["type"] = "restaurant"
            self.state = "RESTAURANT_DATE"
        elif choice == "2":
            self.booking["type"] = "hotel"
            self.state = "HOTEL_DATE"
        else:
            print("Please enter 1 or 2.\n")

    def get_future_date(self, prompt):
        value = input(prompt).strip()
        try:
            selected = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2026-08-20.\n")
            return None

        if selected < date.today():
            print("That date is in the past. Please choose today or a future date.\n")
            return None

        return selected.isoformat()

    def ask_restaurant_date(self):
        selected = self.get_future_date("Enter dining date (YYYY-MM-DD): ")
        if selected:
            self.booking["date"] = selected
            self.state = "RESTAURANT_TIME"

    def ask_restaurant_time(self):
        value = input("Enter time (HH:MM, 24-hour format): ").strip()
        try:
            datetime.strptime(value, "%H:%M")
        except ValueError:
            print("Invalid time. Use HH:MM, e.g. 19:30.\n")
            return

        self.booking["time"] = value
        self.state = "RESTAURANT_PARTY"

    def ask_party_size(self):
        value = input("Enter number of guests: ").strip()
        try:
            size = int(value)
        except ValueError:
            print("Party size must be a whole number.\n")
            return

        if not 1 <= size <= 20:
            print("Party size must be between 1 and 20.\n")
            return

        self.booking["party_size"] = size
        self.state = "CHECK_AVAILABILITY"

    def ask_hotel_date(self):
        check_in = self.get_future_date("Enter check-in date (YYYY-MM-DD): ")
        if not check_in:
            return

        check_out = self.get_future_date("Enter check-out date (YYYY-MM-DD): ")
        if not check_out:
            return

        if check_out <= check_in:
            print("Check-out must be after check-in.\n")
            return

        self.booking["date"] = check_in
        self.booking["time"] = check_out  # Reused field for a compact prototype.
        self.state = "HOTEL_ROOM"

    def ask_room_type(self):
        rooms = self.data["hotel"]["room_types"]
        print("\nAvailable room types:")
        for i, room in enumerate(rooms, start=1):
            print(f"{i}. {room}")

        choice = input("Choose a room type: ").strip()
        try:
            index = int(choice) - 1
            self.booking["room_type"] = rooms[index]
        except (ValueError, IndexError):
            print("Please choose a valid room type.\n")
            return

        self.state = "HOTEL_GUESTS"

    def check_availability(self):
        if self.booking["type"] == "restaurant":
            available = self.data["restaurant"].get(self.booking["date"], [])
            match = next(
                (
                    item for item in available
                    if item["time"] == self.booking["time"]
                    and item["max_party_size"] >= self.booking["party_size"]
                ),
                None,
            )
            if match:
                self.booking["available"] = True
                self.booking["price"] = match["price_per_person"]
                print("\nAvailability found!")
                self.state = "CONFIRM"
            else:
                self.booking["available"] = False
                print("\nSorry, no matching restaurant slot is available.")
                self.state = "CANCEL"

        else:
            available = self.data["hotel"].get("availability", {}).get(
                self.booking["date"], []
            )
            match = next(
                (
                    item for item in available
                    if item["room_type"] == self.booking["room_type"]
                    and item["available_rooms"] > 0
                ),
                None,
            )
            if match:
                self.booking["available"] = True
                self.booking["price_per_night"] = match["price_per_night"]
                self.state = "CONFIRM"
                print("\nRoom available!")
            else:
                self.booking["available"] = False
                print("\nSorry, that room type is not available for the selected date.")
                self.state = "CANCEL"

    def confirm_booking(self):
        print("\n--- Booking Summary ---")
        print(f"Type: {self.booking['type'].title()}")
        print(f"Date: {self.booking['date']}")

        if self.booking["type"] == "restaurant":
            print(f"Time: {self.booking['time']}")
            print(f"Guests: {self.booking['party_size']}")
            print(f"Mock price: ${self.booking['price']} per person")
        else:
            print(f"Check-out: {self.booking['time']}")
            print(f"Room: {self.booking['room_type']}")
            print(f"Guests: {self.booking['party_size']}")
            print(f"Mock price: ${self.booking['price_per_night']} per night")

        choice = input("\nConfirm booking? (yes/no): ").strip().lower()

        if choice in {"yes", "y"}:
            self.booking["guest_name"] = input("Enter guest name: ").strip() or "Guest"
            confirmation_id = "MOCK-" + datetime.now().strftime("%Y%m%d%H%M%S")
            print("\nBooking confirmed!")
            print(f"Guest: {self.booking['guest_name']}")
            print(f"Confirmation ID: {confirmation_id}")
            print("This is a prototype confirmation only.")
        else:
            print("\nBooking not confirmed.")

        self.state = "DONE"


if __name__ == "__main__":
    BookingAssistant().run()
