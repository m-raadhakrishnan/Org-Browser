# auth.py

import gspread
from google.oauth2.service_account import Credentials
import bcrypt

# Setup constants
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
SERVICE_ACCOUNT_FILE = 'credentials.json'

SPREADSHEET_NAME = ''  # Replace with your spreadsheet name
CREDENTIALS_SHEET = ''  # Sheet/tab for user credentials

def get_gsheet_client():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    gc = gspread.authorize(creds)
    return gc.open(SPREADSHEET_NAME)

def signup_user(username, password):
    sheet = get_gsheet_client().worksheet(CREDENTIALS_SHEET)
    usernames = sheet.col_values(1)
    if username in usernames:
        return False  # Username exists

    pwd_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    sheet.append_row([username, pwd_hash])
    return True

def verify_user(username, password):
    sheet = get_gsheet_client().worksheet(CREDENTIALS_SHEET)
    records = sheet.get_all_records()  # returns list of dicts
    for record in records:
        if record['Username'] == username:
            return bcrypt.checkpw(password.encode(), record['PasswordHash'].encode())
    return False
