from __future__ import print_function

from googleApi import get_events
from ovApi import NS

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

    ns_getter = NS()

    print(ns_getter.get_locations('hoo'))


if __name__ == '__main__':
    main()
