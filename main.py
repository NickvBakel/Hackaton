from __future__ import print_function
from googleApi import get_events
from datetime import datetime
from ovApi import OV
from flask import Flask
import json
from flask_cors import CORS
app = Flask(__name__)


@app.route("/stations/<query>")
def hello(query):
    CORS(app)
    ov = OV()
    return ov.get_locations(query)


@app.route('/route/<search_type>/<from_station>')
def get_route(search_type, from_station):
    CORS(app)
    events = get_events()
    ov = OV()
    if not events:
        print("No data")
        return
    start_time_calendar, start_location_calendar, end_time_calendar, end_location_calendar = get_arrival_departure_time_location(
        events)
    departure = ov.plan_journey(from_station, start_location_calendar, start_time_calendar, "arrival")
    arrival = ov.plan_journey(end_location_calendar, from_station, end_time_calendar, "departure")
    if search_type == 'departure':
        return json.dumps(departure, default = lambda x: x.__dict__)
    else:
        return json.dumps(arrival, default = lambda x: x.__dict__)


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


if __name__ == '__main__':
    app.run()
