# Home Library Scanner

Pretty simple ISBN scan with Google Sheets integration. Made for my mom, who has so many books she sometimes buys another copy of a book without realizing she already owns it.

## Dependencies
- [A Google Cloud Platform project](https://developers.google.com/workspace/guides/create-project) with the [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python) enabled.
- The [`pip`](https://pypi.org/project/pip/) package manager
- [Heroku and its prereqs](https://devcenter.heroku.com/articles/getting-started-with-python)
    - Python 3.9
    - The Heroku CLI

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
I can't see my mom running Python from a terminal, so I'd like to rewrite this in Javascript and turn it into a browser plugin. The plugin should
- get the sheet ID from the current tab's URL
- always accept keyboard input in the background
- if it's an ISBN, look up the book data and add it to the spreadsheet

Even better, this could be constantly running on a dedicated Raspberry Pi.