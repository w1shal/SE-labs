"""Manage event creation, guest registration, and event persistence."""

import json
import re
import secrets
import subprocess
from datetime import date

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """Create and return an event with its venue, capacity, and guests."""
    if guests is None:
        guests = []

    events[event_name] = {
        "venue": venue,
        "capacity": capacity,
        "guests": guests,
    }

    return events[event_name]


def register_guest(event_name, guest):
    """Register a guest if the event exists and has available capacity."""
    event = events.get(event_name)

    if event is None:
        print("No such event:", event_name)
        return False

    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False

    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """Return the number of seats remaining at an event."""
    event = events[event_name]
    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """Return whether an event is upcoming or completed."""
    if event_date >= date.today():
        return "Upcoming"

    return "Completed"


def guest_report(event_name, sort_order="name"):
    """Return the event's guest names in the requested alphabetical order."""
    names = events[event_name]["guests"]

    if sort_order == "name":
        sorted_names = sorted(names)
    elif sort_order == "reverse":
        sorted_names = sorted(names, reverse=True)
    else:
        raise ValueError(
            "sort_order must be 'name' or 'reverse'"
        )

    return ", ".join(sorted_names)


def save_events(file_name="events.json"):
    """Save all events to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=4)


def load_events(file_name="events.json"):
    """Load event data from JSON and validate its top-level structure."""
    with open(file_name, "r", encoding="utf-8") as file:
        restored_events = json.load(file)

    if not isinstance(restored_events, dict):
        raise ValueError("Invalid event data: expected a dictionary")

    return restored_events


def print_badges(event_name):
    """Print the badge file associated with an event."""
    if not re.fullmatch(r"[A-Za-z0-9_-]+", event_name):
        raise ValueError("Invalid event name")

    filename = f"badges_{event_name}.txt"

    subprocess.run(
        ["lp", filename],
        check=True,
        shell=False,
    )


def main():
    """Run the event manager demonstration."""
    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop", 2)

    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")

    left = seats_left("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seats_left("Alumni Dinner"))

    print(
        "Tech Meetup guests:",
        guest_report("Tech Meetup", "name"),
    )

    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print("Alumni Dinner is", event_status(date(2020, 5, 1)))

    guests = events["Tech Meetup"]["guests"]

    if guests:
        winner = secrets.choice(guests)
        print("Lucky draw winner:", winner)
    else:
        print("No guests registered for the lucky draw.")

    save_events()
    restored = load_events()  # Reload to confirm the save worked.

    print("Events restored from file:", len(restored))
    print("Venues:", [event["venue"] for event in restored.values()])


if __name__ == "__main__":
    main()
