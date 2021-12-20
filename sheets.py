import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
sheet_id_filename = 'sheet_id.txt'

def insert_book_in_sheet(service, author_str, title, shelf, isbn):
    SPREADSHEET_ID = None
    if os.path.exists(sheet_id_filename):
        with open(sheet_id_filename, 'r') as keyfile:
            SPREADSHEET_ID = keyfile.readline().strip()
    else:
        print("Spreadsheet ID not set! File {} not found.".format(sheet_id_filename))
        exit(-1)

    # Call the Sheets API
    sheet = service.spreadsheets()
    entry = [author_str, title, shelf, isbn]
    body = {
        'values': [entry]
    }
    result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                range='Sheet1',valueInputOption='RAW',body=body).execute()
