import json
import re
import secrets
import subprocess
from datetime import date

events = {}


def createEvent(eventName, venue, capacity=50, guests=[]):
    events[eventName] = {"venue": venue, "capacity": capacity,
                         "guests": guests}
    return events[eventName]


def registerGuest(eventName, guest):
    event = events.get(eventName)
    if event is None:
        print("No such event:", eventName)
        return False
    if len(event["guests"]) >= event["capacity"]:
        print(eventName, "is full, cannot add", guest)
        return False
    event["guests"].append(guest)
    return True


def seatsLeft(eventName):
    event = events[eventName]
    return event["capacity"] - len(event["guests"])


def eventStatus(eventDate):
    if eventDate >= date.today():
        return "Upcoming"
    else:
        return "Completed"


def guestReport(eventName, sortOrder):
    names = sorted(events[eventName]["guests"])
    return ", ".join(names)


def saveEvents(fileName="events.json"):
    with open(fileName, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=4)


def loadEvents(fileName="events.json"):
    with open(fileName, "r", encoding="utf-8") as f:
        restored_events = json.load(f)

    if not isinstance(restored_events, dict):
        raise ValueError("Invalid event data: expected a dictionary")

    return restored_events


def printBadges(eventName):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", eventName):
        raise ValueError("Invalid event name")

    filename = f"badges_{eventName}.txt"

    subprocess.run(
        ["lp", filename],
        check=True,
        shell=False,
    )


def main():
    createEvent("Tech Meetup", "Hall A", 3)
    createEvent("Alumni Dinner", "Rooftop",2)
    registerGuest("Tech Meetup", "Asha")
    registerGuest("Tech Meetup", "Ravi")
    registerGuest("Alumni Dinner", "Meena")
    registerGuest("Workshop", "Kiran")
    left=seatsLeft("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seatsLeft("Alumni Dinner"))
    print("Tech Meetup guests:", guestReport("Tech Meetup", "name"))
    print("Tech Meetup is", eventStatus(date(2099, 1, 15)))
    print("Alumni Dinner is", eventStatus(date(2020, 5, 1)))
    guests = events["Tech Meetup"]["guests"]
    if guests:
        winner = secrets.choice(guests)
        print("Lucky draw winner:", winner)
    else:
        print("No guests registered for the lucky draw.")
    saveEvents()
    restored = loadEvents()
    print("Events restored from file:", len(restored))
    print("Venues:", [e["venue"] for e in restored.values()])

main()
