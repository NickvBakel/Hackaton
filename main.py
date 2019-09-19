from __future__ import print_function
from googleApi import get_events
from datetime import datetime
from ovApi import OV
from flask import Flask
import json
app = Flask(__name__)


@app.route("/stations/<query>")
def hello(query):
    ov = OV()
    return ov.get_locations(query)


@app.route('/route/<from_station>')
def get_route(from_station):
    events = get_events()
    ov = OV()
    if not events:
        print("No data")
        return
    start_time_calendar, start_location_calendar, end_time_calendar, end_location_calendar = get_arrival_departure_time_location(
        events)
    departure = ov.plan_journey(from_station, start_location_calendar, start_time_calendar, "arrival")
    arrival = ov.plan_journey(end_location_calendar, from_station, end_time_calendar, "departure")
    print(departure)
    return json.dumps(departure.__dict__)


ov_location_base = "amsterdam_hogeschool-van-amsterdam-loc-"


def get_arrival_departure_time_location(events):
    start_time = None
    start_location = None
    end_time = None
    end_location = None
    for i in range(len(events)):
        if i == 0:
            event = events[i]
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = datetime.fromisoformat(start).strftime('%Y-%m-%dT%H%M')
            start_location = ov_location_base + event['location'][0:3].lower()
        if i == (len(events) - 1):
            event = events[i]
            end = event['end'].get('dateTime', event['end'].get('date'))
            end_time = datetime.fromisoformat(end).strftime('%Y-%m-%dT%H%M')
            end_location = ov_location_base + event['location'][0:3].lower()
    return start_time, start_location, end_time, end_location


def main():
    events = get_events()
    if not events:
        print("No data")
        return

    start_time_calendar, start_location_calendar, end_time_calendar, end_location_calendar = get_arrival_departure_time_location(events)

    ov = OV()
    locations = {}

    location = input("Please enter location: ")
    print("\nYou entered: " + location)
    print('---------------------------------')

    counter = 1
    for location in ov.get_locations(location)['locations']:
        locations[counter] = location['id']
        print(str(counter) + ". " + location['name'] + " (" + location['type'] + ")")
        counter += 1

    location = input("Select location: ")
    print("\nYou entered: " + location)

    from_station = str(locations.get(int(location)))

    print("----------------------------Heenreis----------------------")

    route = ov.plan_journey(from_station, start_location_calendar, start_time_calendar, "arrival")

    for part in route:
        part.show()
        print()

    print("---------------------------Terugreis----------------------")
    route = ov.plan_journey(end_location_calendar, from_station, end_time_calendar, "departure")

    for part in route:
        part.show()
        print()


if __name__ == '__main__':
    app.run()
