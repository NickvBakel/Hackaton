from __future__ import print_function
import datetime
import pickle
import os.path
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_events():
    """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Get the calendar id of the HvA schedule
    page_token = None
    calendar_id = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        # print(calendar_list['items'])
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'][0:23] == 'HvA persoonlijk rooster':
                calendar_id = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    # Return if HvA is not added
    if not calendar_id:
        return []

    # Call the Calendar API
    now = datetime.datetime.now(pytz.timezone('Europe/Amsterdam'))
    now = now.replace(day=20, hour=8)

    end_time = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    events_result = service.events().list(calendarId=calendar_id, timeMin=now.isoformat(), timeMax=end_time.isoformat(),
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events
