from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests

SPREADSHEET_ID = '1rzfovc6kHtEPigCBpLA8JYxmyB9uYQh4MN2sNkdWOJo'
#SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def insert_book_in_sheet(service, author_str, title, shelf, isbn):
    # Call the Sheets API
    sheet = service.spreadsheets()
    entry = [author_str, title, shelf, isbn]
    body = {
        'values': [entry]
    }
    result = sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                    range='Sheet1',valueInputOption='RAW',body=body).execute()

def scan_book(service):
    isbn = input("Scan ISBN:\n")
    # Ender's Game: 9780812550702
    # La realtà non è come ci appare: 9788860306418
    # A Man Called Ove: 9781476738024
    shelf = input("Scaffale:\n")

    bookinfo = requests.get(f"https://openlibrary.org/isbn/{isbn}.json").json()

    # get author
    authors = []
    try:
        authors_json = bookinfo['authors']
    except:
        authors_json = []
    for a in authors_json:
        try:
            authors.append(requests.get(f"https://openlibrary.org/{a['key']}.json").json()['name'])
        except:
            pass

    author_str = ""
    for a in authors:
        lastname_index = a.rfind(" ") + 1
        author_str += a[lastname_index:] + ", " + a[:lastname_index]

    # get title
    try:
        title = bookinfo['title']
    except: 
        title = ""

    insert_book_in_sheet(service, author_str, title, shelf, isbn)

def main():
    ### Login/authorization
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    while True:
        scan_book(service)

if __name__ == '__main__':
    main()