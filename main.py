from __future__ import print_function

from datetime import datetime

from ovApi import OV


def main():

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
