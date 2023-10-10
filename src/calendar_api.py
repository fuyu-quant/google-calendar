import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from google_auth_oauthlib.flow import InstalledAppFlow

from dateutil import parser
import datetime

import pandas as pd
import re
import datetime

# If modifying these SCOPES, delete the file token.json.




SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']



def service_google_calendar():
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file(
        '../credentials_oauth.json', SCOPES)
    #creds = flow.run_local_server(port=0)
    reds = flow.run_console()


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




def convert_to_time(decimal_time):
    hours = int(decimal_time)
    minutes = int((decimal_time - hours) * 60)
    return f"{hours:02d}:{minutes:02d}"


def data_to_df(data):
    # 初期の空のデータフレームを作成します
    df = pd.DataFrame()

    # データをループで処理します
    for i in data:
        description = data[i]['description']
        pattern = re.compile(r'工数:\[(.*?)\]')
        match = pattern.search(description)

        # マッチするものがある場合、データフレームを更新します
        if match:
            code = match.group(1)
            date = data[i]['date']
            time = data[i]['time'].total_seconds() / 3600  # 時間を時間単位に変換します（オプション）

            # 新しいデータが既存のデータフレームに存在するかチェックします
            if date in df.index and code in df.columns:
                df.at[date, code] += time  # 時間を加算します
            else:
                # データが存在しない場合、新しい行または列を作成します
                df.at[date, code] = time

    # NaN値を0で埋めます
    df.fillna(0, inplace=True)

    for column in df.columns:
        df[column] = df[column].apply(convert_to_time)

    return df