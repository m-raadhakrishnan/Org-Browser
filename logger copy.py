# logger.py

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import requests

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SERVICE_ACCOUNT_FILE = 'credentials.json'

SPREADSHEET_NAME = 'TrackerDB'  # Same sheet name
LOG_SHEET = 'tracker'  # Sheet/tab for activity tracking

def get_gsheet_client():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    return gc.open(SPREADSHEET_NAME)

def get_my_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return 'Unknown'

def log_activity(username, url):
    ip = get_my_ip()
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')
    sheet = get_gsheet_client().worksheet(LOG_SHEET)
    sheet.append_row([ip, username, date, time, url])
