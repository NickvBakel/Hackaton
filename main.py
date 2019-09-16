from __future__ import print_function
from googleApi import get_events

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    events = get_events()

    if not events:
        print('No upcoming events found.')
    for event in events:
        print(event)
        break
        # start = event['start'].get('dateTime', event['start'].get('date'))
        # print(start, event['summary'])

if __name__ == '__main__':
    main()