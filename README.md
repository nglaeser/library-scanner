# Home Library Scanner

Pretty simple ISBN scan with Google Sheets integration. Made for my mom, who has so many books she sometimes buys a *second* copy of a book without realizing she already owns it.

## Dependencies
- [A Google Cloud Platform project](https://developers.google.com/workspace/guides/create-project) with the [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python) enabled.
- The [`pip`](https://pypi.org/project/pip/) package manager

## Setup
```
pip install -r requirements.txt
```

## Usage
```
python scan.py
```
Will continually prompt for ISBN (required) and shelf number. The idea is that you could hook up a handheld scanner, which functions as a keyboard input, and simply scan books in one after the other.

The ISBN is used to look up the book info, which is then appended to the Google Sheet specified by the sheet ID hardcoded into the file.

Example books:
```
Ender's Game:                   9780812550702
La realtà non è come ci appare: 9788860306418
A Man Called Ove:               9781476738024
```

## Todo
- I can't see my mom running Python from a terminal, so I'd like to have this running on a dedicated Raspberry Pi
- Wait a max time (3 seconds?) for shelf number