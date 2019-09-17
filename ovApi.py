from datetime import datetime
import requests


class NS (object):
    url = 'http://api.9292.nl/0.1/'

    def plan_journey(self):
        base_url = "journeys?lang=nl-NL&"
        time = "dateTime=" + datetime.now().strftime('%Y-%m-%dT%H%M')
        from_station = "&from=station-hoorn"
        to_station = "&to=amsterdam/hogeschool-van-amsterdam-loc-wbh"
        before = "&before=1"
        after = "&after=5"
        sequence = "&sequence=1"
        options = "&byFerry=true&bySubway=true&byBus=true&byTram=true&byTrain=true"

        url = self.url + base_url + time + from_station + to_station + before + after + sequence + options
        response = requests.get(url)
        print(response.status_code)
        return url

    def get_locations(self, location):
        url = self.url + 'locations?lang=nl-NL&q=' + location
        response = requests.get(url)
        return response.json()
