from datetime import datetime, timedelta
import requests


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
        journeys = requests.get(url)
        journeys = journeys.json()
        print(url)
        steps = []
        first = True
        counter = 1
        destination_temp = ""
        end_time_temp = ""

        for part in journeys['journeys'][1]['legs']:
            if part['type'] == "continuous":
                if first:
                    kind = part['mode']['name'][0:5]
                    departure_location = part['stops'][0]['location']['name']
                    if 'stopType' in part['stops'][-1]['location']:
                        arrival_location = part['stops'][-1]['location']['stopType'] + " " + \
                                           part['stops'][-1]['location']['place']['name'] + " " + \
                                           part['stops'][-1]['location']['name']
                    else:
                        arrival_location = part['stops'][-1]['location']['place']['name'] + " " + \
                                           part['stops'][-1]['location']['stationType']
                    departure_time = journeys['journeys'][1]['departure']
                    arrival_time = calculate_end_time(journeys['journeys'][1]['departure'], part['duration'])
                    duration = part['duration']
                elif counter == len(journeys['journeys'][1]['legs']):
                    kind = part['mode']['name'][0:5]
                    departure_location = destination_temp
                    arrival_location = part['stops'][-1]['location']['place']['name'] + " " + \
                                       part['stops'][-1]['location']['name']
                    departure_time = end_time_temp
                    arrival_time = journeys['journeys'][1]['arrival']
                    duration = part['duration']
                else:
                    kind = part['mode']['name'][0:5]
                    departure_location = destination_temp
                    if 'stopType' in part['stops'][-1]['location']:
                        arrival_location = part['stops'][-1]['location']['place']['name'] + " " + \
                                           part['stops'][-1]['location']['stopType']
                    else:
                        arrival_location = part['stops'][-1]['location']['place']['name'] + " " + \
                                           part['stops'][-1]['location']['stationType']
                    departure_time = end_time_temp
                    arrival_time = calculate_end_time(end_time_temp, part['duration'])
                    duration = part['duration']
            else:
                end_time_temp = part['stops'][-1]['arrival']
                if part['mode']['type'] == 'train':
                    destination_temp = part['stops'][-1]['location']['stationType'] + " " + \
                                       part['stops'][-1]['location']['name']
                    kind = part['mode']['name'] + " richting " + part['destination']
                    departure_location = part['stops'][0]['location']['stationType'] + " " + \
                                         part['stops'][0]['location']['name']
                    arrival_location = part['stops'][-1]['location']['stationType'] + " " + \
                                       part['stops'][-1]['location']['name']
                    departure_time = part['stops'][0]['departure']
                    arrival_time = part['stops'][-1]['arrival']
                    duration = calculate_duration(part['stops'][-1]['arrival'], part['stops'][0]['departure'])
                else:
                    destination_temp = part['stops'][-1]['location']['stopType'] + " " + \
                                       part['stops'][-1]['location']['place']['name'] + " " + \
                                       part['stops'][-1]['location']['name']
                    kind = part['mode']['name'] + " richting " + part['destination']
                    departure_location = part['stops'][0]['location']['stopType'] + " " + \
                                         part['stops'][0]['location']['place']['name'] + " " + \
                                         part['stops'][0]['location']['name']
                    arrival_location = part['stops'][-1]['location']['stopType'] + " " + \
                                       part['stops'][-1]['location']['place']['name'] + " " + \
                                       part['stops'][-1]['location']['name']
                    departure_time = part['stops'][0]['departure']
                    arrival_time = part['stops'][-1]['arrival']
                    duration = calculate_duration(part['stops'][-1]['arrival'], part['stops'][0]['departure'])
            steps.append({
                'kind': kind,
                'departure_location': departure_location,
                'arrival_location': arrival_location,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration': duration
            })
            counter += 1
            first = False
        return steps

    def get_locations(self, location):
        url = self.url + 'locations?lang=nl-NL&q=' + location
        response = requests.get(url)
        return response.json()


def calculate_end_time(start, end):
    start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
    start = start + timedelta(minutes=int(end[3:5]))
    return start.strftime('%Y-%m-%dT%H:%M')


def calculate_duration(arrival, departure):
    arrival = datetime.strptime(arrival, '%Y-%m-%dT%H:%M')
    departure = datetime.strptime(departure, '%Y-%m-%dT%H:%M')
    return datetime.strptime(str(arrival - departure), '%H:%M:%S').strftime('%H:%M')
