import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from dateutil import parser
import datetime

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def service_google_calendar():
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file(
        '../credentials_oauth.json', SCOPES)
    creds = flow.run_local_server(port=0)

    service = build('calendar', 'v3', credentials=creds)
    return service



def get_events(start_date, end_date):
    service = service_google_calendar()

    timeMin = start_date.isoformat() + 'Z'
    timeMax = end_date.isoformat() + 'Z'

    print(f'Getting events from {start_date} to {end_date}')
    events_result = service.events().list(
        calendarId='primary', timeMin=timeMin, timeMax=timeMax,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No events found.')
    data = {}
    i = 0
    for event in events:
        i += 1
        start_str = event['start'].get('dateTime', event['start'].get('date'))
        end_str = event['end'].get('dateTime', event['end'].get('date'))
        description = event.get('description', '')

        start_dt = parser.parse(start_str)
        end_dt = parser.parse(end_str)
        time = end_dt - start_dt

        data[i] = {'description': description, 'time' :time }

    return data
