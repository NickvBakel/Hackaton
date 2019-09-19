from datetime import datetime, timedelta
import requests
from Step import Step


class OV(object):
    url = 'http://api.9292.nl/0.1/'

    def plan_journey(self, from_location, to_station, time, departure):
        base_url = "journeys?lang=nl-NL&"
        time = "dateTime=" + time
        from_station = "&from=" + from_location
        to_station = "&to=" + to_station
        before = "&before=1"
        after = "&after=5"
        sequence = "&sequence=1"
        options = "&byFerry=true&bySubway=true&byBus=true&byTram=true&byTrain=true"
        search_type = "&searchType=" + departure

        url = self.url + base_url + time + from_station + to_station + before + after + sequence + options + search_type
        journeys = requests.get(url).json()
        print(url)
        steps = []
        first = True
        counter = 1
        destination_temp = ""
        end_time_temp = ""

        for part in journeys['journeys'][1]['legs']:
            last_stop = part['stops'][-1]['location']
            first_stop = part['stops'][0]['location']

            step = Step()
            if part['type'] == "continuous":
                if first:
                    step.kind = part['mode']['name'][0:5]
                    step.departure_location = first_stop['name']
                    if 'stopType' in last_stop:
                        step.arrival_location = last_stop['stopType'] + " " + last_stop['place']['name'] + last_stop['name']
                    else:
                        step.arrival_location = last_stop['place']['name'] + " " + last_stop['stationType']
                    step.departure_time = journeys['journeys'][1]['departure']
                    step.arrival_time = self.calculate_end_time(journeys['journeys'][1]['departure'], part['duration'])
                    step.duration = part['duration']
                elif counter == len(journeys['journeys'][1]['legs']):
                    step.kind = part['mode']['name'][0:5]
                    step.departure_location = destination_temp
                    step.arrival_location = last_stop['place']['name'] + " " + last_stop['name']
                    step.departure_time = end_time_temp
                    step.arrival_time = journeys['journeys'][1]['arrival']
                    step.duration = part['duration']
                else:
                    step.kind = part['mode']['name'][0:5]
                    step.departure_location = destination_temp
                    if 'stopType' in last_stop:
                        step.arrival_location = last_stop['place']['name'] + " " + last_stop['stopType']
                    else:
                        step.arrival_location = last_stop['place']['name'] + " " + last_stop['stationType']
                    step.departure_time = end_time_temp
                    step.arrival_time = self.calculate_end_time(end_time_temp, part['duration'])
                    step.duration = part['duration']
            else:
                end_time_temp = part['stops'][-1]['arrival']
                if part['mode']['type'] == 'train':
                    destination_temp = last_stop['stationType'] + " " + last_stop['name']
                    step.kind = part['mode']['name'] + " richting " + part['destination']
                    step.departure_location = first_stop['stationType'] + " " + first_stop['name']
                    step.arrival_location = last_stop['stationType'] + " " + last_stop['name']
                    step.departure_time = part['stops'][0]['departure']
                    step.arrival_time = part['stops'][-1]['arrival']
                    step.duration = self.calculate_duration(part['stops'][-1]['arrival'], part['stops'][0]['departure'])
                else:
                    destination_temp = last_stop['stopType'] + " " + last_stop['place']['name'] + " " + last_stop['name']
                    step.kind = part['mode']['name'] + " richting " + part['destination']
                    step.departure_location = first_stop['stopType'] + " " + first_stop['place']['name'] + " " + first_stop['name']
                    step.arrival_location = last_stop['stopType'] + " " + last_stop['place']['name'] + " " + last_stop['name']
                    step.departure_time = part['stops'][0]['departure']
                    step.arrival_time = part['stops'][-1]['arrival']
                    step.duration = self.calculate_duration(part['stops'][-1]['arrival'], part['stops'][0]['departure'])
            steps.append(step)
            counter += 1
            first = False
        return steps

    def get_locations(self, location):
        url = self.url + 'locations?lang=nl-NL&q=' + location
        response = requests.get(url)
        return response.json()

    def calculate_end_time(self, start, end):
        start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        start = start + timedelta(minutes=int(end[3:5]))
        return start.strftime('%Y-%m-%dT%H:%M')

    def calculate_duration(self, arrival, departure):
        arrival = datetime.strptime(arrival, '%Y-%m-%dT%H:%M')
        departure = datetime.strptime(departure, '%Y-%m-%dT%H:%M')
        return datetime.strptime(str(arrival - departure), '%H:%M:%S').strftime('%H:%M')
