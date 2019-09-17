from __future__ import print_function
from googleApi import get_events
import datetime

ov_location_base = "amsterdam_hogeschool-van-amsterdam-loc-"


def main():
    events = get_events()
    if not events:
        print("No data")
        return

    start_time, start_location, end_time, end_location = get_arrival_departure_time_location(events)
    print("Arrive at: " + start_time + " at: " + start_location)
    print("Departure at: " + end_time + " from: " + end_location)


def get_arrival_departure_time_location(events):
    start_time = None
    start_location = None
    end_time = None
    end_location = None
    for i in range(len(events)):
        if i == 0:
            event = events[i]
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_time = datetime.datetime.fromisoformat(start).strftime('%Y-%m-%dT%H%M')
            start_location = ov_location_base + event['location'][0:3].lower()
        if i == (len(events) - 1):
            event = events[i]
            end = event['end'].get('dateTime', event['end'].get('date'))
            end_time = datetime.datetime.fromisoformat(end).strftime('%Y-%m-%dT%H%M')
            end_location = ov_location_base + event['location'][0:3].lower()
    return start_time, start_location, end_time, end_location


if __name__ == '__main__':
    main()
