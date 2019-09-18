from __future__ import print_function
from googleApi import get_events
from datetime import datetime
from ovApi import OV

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

    start_time, start_location, end_time, end_location = get_arrival_departure_time_location(events)
    print("Arrive at: " + start_time + " at: " + start_location)
    print("Departure at: " + end_time + " from: " + end_location)

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
    print('---------------------------------')

    from_station = str(locations.get(int(location)))
    to_station = "amsterdam/hogeschool-van-amsterdam-loc-wbh"
    time = datetime.now().strftime('%Y-%m-%dT%H%M')
    departure = "departure"

    route = ov.plan_journey(from_station, to_station, time, departure)

    for part in route:
        print(part)
        print()


if __name__ == '__main__':
    main()
