from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import requests

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def insert_book_in_sheet(service, author_str, title, shelf, isbn):
    SPREADSHEET_ID = None
    if os.path.exists('sheet_id.txt'):
        with open('sheet_id.txt', 'r') as keyfile:
            SPREADSHEET_ID = keyfile.readline().strip()
    else:
        exit(-1)

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
    shelf = ""
    # shelf = input("Shelf #:\n")

    try:
        bookinfo = requests.get(f"https://openlibrary.org/isbn/{isbn}.json").json()
    except:
        print("unable to find {} in OpenLibrary".format(isbn))

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

    for a in authors:
        lastname_index = a.rfind(" ") + 1
        a = a[lastname_index:] + ", " + a[:lastname_index]
    author_str = "; ".join(authors)

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

    ### Use API key instead of OAuth token (doesn't work)
    # API_KEY = None
    # if os.path.exists('api_key.txt'):
    #     with open('api_key.txt', 'r') as keyfile:
    #         API_KEY = keyfile.readline()
    # service = build('sheets', 'v4', developerKey=API_KEY)

    while True:
        scan_book(service)

if __name__ == '__main__':
    main()