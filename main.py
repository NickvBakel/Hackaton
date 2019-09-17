from __future__ import print_function

from googleApi import get_events
from ovApi import OV

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    # events = get_events()
    #
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(event['location'])
    #     break
    #     print(start, event['summary'])

    ns_getter = OV()
    locations = {}

    location = input("Please enter location: ")
    print("\nYou entered: " + location)
    print('---------------------------------')

    counter = 1
    for location in ns_getter.get_locations(location)['locations']:
        locations[counter] = location['id']
        print(str(counter) + ". " + location['name'])
        counter += 1

    location = input("Select location: ")
    print("\nYou entered: " + location)
    print('---------------------------------')

    ns_getter.plan_journey(str(locations.get(int(location))))


if __name__ == '__main__':
    main()
