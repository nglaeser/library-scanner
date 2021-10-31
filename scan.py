from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import requests
import xml.etree.ElementTree as ET

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
        xml = requests.get(f"http://classify.oclc.org/classify2/Classify?isbn={isbn}&summary=true")
        root = ET.fromstring(xml.content)
        bookinfo = root.find('./*{http://classify.oclc.org}work')
        # `./*` means any node below (not just direct children)
    except:
        print("unable to find {} in WorldCat".format(isbn))

    # get author(s)
    try:
        authors = bookinfo.get('author').split("|")
        # TODO remove authors with "[*]" after their names (editor, translator, etc.) e.g. "Schwarz, Benjamin [Translator]"
        # also remove years after author names (e.g. "Bonnefoy, Jean, 1950-")
    except:
        # no author info
        authors = ""
    authors = [a.strip() for a in authors]
    author_str = "; ".join(authors)

    # get title
    title = bookinfo.get('title')

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