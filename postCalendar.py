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
  loop = config['loop'] == 'true'
  periods = {
    '1'	:	27000,
    '2'	:	30000,
    '2.5' : 31500,
    '3'	:	33600,
    '3.5'	:	35100,
    '4'	:	36600,
    '5'	:	40200,
    '6'	:	45000,
    '7'	:	48000,
    '7.5' : 49500,
    '8'	:	51600,
    '8.5'	:	51900,
    '9'	:	54600,
    '10'	:	58200
  }
  period = 3000
  half_period = 1500
  secsPerDay = 86400

  main_events = []
  for e in events:
    event = events[e]
    event_week = datetime.datetime.strptime(event['StartWeek'], '%d/%m/%Y').isocalendar()[1]
    this_week = datetime.datetime.now().isocalendar()[1]
    if loop or (event_week <= this_week + week):
      main_events.append(event)

  # print(main_events)

  # Push events
  for event in main_events:
    temp = datetime.datetime.strptime(event['StartWeek'], '%d/%m/%Y')
    temp = datetime.datetime.fromtimestamp(temp.timestamp() - temp.isocalendar()[2]*secsPerDay + secsPerDay)
    date = temp.timestamp() + (int(event['Schedule']['Day']) - 1 - temp.isocalendar()[2]) * secsPerDay
    
    this_week = datetime.datetime.now().isocalendar()[1]
    while(this_week + week > datetime.datetime.fromtimestamp(date).isocalendar()[1]): date = date + secsPerDay * 7

    if(date < temp.timestamp()): continue

    start_time = periods[event['Schedule']['StartTime']]
    if (str(event['Schedule']['EndTime']).find('.') == -1):
      end_time = periods[event['Schedule']['EndTime']] + period
    else:
      end_time = periods[event['Schedule']['EndTime']] + half_period
    e = {
      'summary': event['SubjectID'] + ' - ' + event['SubjectName'],
      'location': event['Schedule']['Room'] + ' - ' + event['Schedule']['Where'],
      'description': event['ClassType'],
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
      if loop:
        'recurrence': [ 
        "RRULE:FREQ=WEEKLY",
        ],
    }

    print(e['summary'], datetime.datetime.fromtimestamp(date).isoformat())

    e = service.events().insert(calendarId='primary', body=e).execute()

def readJSON(JsonPath = 'TKB.json'):
  with open(JsonPath, encoding='utf-8') as db:
    data = json.load(db)
    return data

def postCalendar(data):
  with open('config.json') as conf:
    config = json.load(conf)
  service = getService()
  insertEvents(data, service, config)
