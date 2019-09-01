from __future__ import print_function
import datetime
import pickle
import json
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def getService():
  """Shows basic usage of the Google Calendar API.
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
  return service

def insertEvents(events, service, config):
  # Get selected events
  week = config['week'] == 'that'
  periods = [
    27000, 30600, 33600, 37200, 40200, 45000, 48600, 51600, 54600, 58200
  ]
  period = 3000
  secsPerDay = 86400

  main_events = []
  for e in events:
    event = events[e]
    event_week = datetime.datetime.strptime(event['Tuần bắt đầu'], '%d/%m/%Y').isocalendar()[1]
    this_week = datetime.datetime.now().isocalendar()[1]
    #if you wanna repeat the scheduler, use main_events.append(event) without if
    if(event_week <= this_week + week): 
      main_events.append(event)
    

  # print(main_events)

  # Push events
  for event in main_events:
    temp = datetime.datetime.strptime(event['Tuần bắt đầu'], '%d/%m/%Y')
    temp = datetime.datetime.fromtimestamp(temp.timestamp() - temp.isocalendar()[2]*secsPerDay + secsPerDay)
    date = temp.timestamp() + (int(event['Lịch học']['Thứ']) - 1 - temp.isocalendar()[2]) * secsPerDay
    
    this_week = datetime.datetime.now().isocalendar()[1]
    while(this_week + week > datetime.datetime.fromtimestamp(date).isocalendar()[1]): date = date + secsPerDay * 7

    if(date < temp.timestamp()): continue

    start_time = periods[int(event['Lịch học']['Tiết bắt đầu']) - 1]
    end_time = periods[int(event['Lịch học']['Tiết kết thúc']) - 1] + period

    e = {
      'summary': event['Mã môn học'] + ' - ' + event['Tên môn học'],
      'location': event['Lịch học']['Phòng'] + ' - ' + event['Lịch học']['Cơ sở'],
      'description': event['Loại'],
      'start': {
        'dateTime': datetime.datetime.utcfromtimestamp(date + start_time).isoformat() + 'Z',
        'timeZone' : 'UTC',
      },
      'end': {
        'dateTime': datetime.datetime.utcfromtimestamp(date + end_time).isoformat() + 'Z',
        'timeZone' : 'UTC',
      },
      'reminders': {
        'useDefault': False,
      },
      #un-comment this code if you wanna repeat the scheduler
      #'recurrence': [ 
      #"RRULE:FREQ=WEEKLY",
      #],
    }

    print(e['summary'], datetime.datetime.fromtimestamp(date).isoformat())

    #e = service.events().insert(calendarId='primary', body=e).execute()
    #return

def readJSON(JsonPath = 'TKB.json'):
  with open(JsonPath, encoding='utf-8') as db:
    data = json.load(db)
    return data

def postCalendar(data):
  # data là dữ liệu tkb
  with open('config.json') as conf:
    config = json.load(conf)
  service = getService()
  insertEvents(data, service, config)

