# Home Library Scanner

Pretty simple ISBN scan with Google Sheets integration. Made for my mom, who has so many books she sometimes buys a *second* copy of a book without realizing she already owns it.

## Dependencies
- [A Google Cloud Platform project](https://developers.google.com/workspace/guides/create-project) with the [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python) enabled.
- The [`pip`](https://pypi.org/project/pip/) package manager

## Setup
```
pip install -r requirements.txt
echo "YOUR_SHEET_ID_HERE" > sheet_id.txt
```

You can find your sheet ID in the Google Sheet's URL: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/`.

## Usage
```
python scan.py
```
Will continually prompt for ISBN (required) and shelf number. The idea is that you could hook up a handheld scanner, which functions as a keyboard input, and simply scan books in one after the other.

The ISBN is used to look up the book info, which is then appended to the Google Sheet specified by the sheet ID in the file `sheet_id.txt`. Currently, we search for the ISBN in [OpenLibrary](https://openlibrary.org/) and use [WorldCat](https://www.worldcat.org/) as a fallback.

Example books:
```
Ender's Game:                               9780812550702
La realtà non è come ci appare:             9788860306418
A Man Called Ove:                           9781476738024
Il misterioso manoscritto di Nostratopus:   9788838455131
[Not found in either catalog]:              9788821557750
```

### Installing Micropython Packages

In the MicroPython REPL (launch with `./micropython`; Getting Started info [here](https://github.com/micropython/micropython/wiki/Getting-Started)):

```
import upip
upip.install("packagename")
```

For example, `upip.install("os")`.

## Todo
<<<<<<< HEAD
- [ ] Running on a dedicated Raspberry Pi
    - Cronjob that checks for new GH releases and downloads if there is a newer one?
- [ ] Shelf number? 
    - Wait a max time (3 seconds?) for shelf number
    - or recognize a different input format for shelf numbers and only input a shelf number when it needs to be changed (otherwise assume it's the previous shelf; maybe until a timeout)
- [x] Combine both ISBN APIs (first OpenLibrary, then WorldCat as fallback)
=======
- I can't see my mom running Python from a terminal, so I'd like to have this running on a dedicated Raspberry Pi
  - [Pushing to GSheets using MicroPython](https://github.com/artem-smotrakov/esp32-weather-google-sheets)
  - https://forum.micropython.org/viewtopic.php?f=15&t=8161
  - https://docs.micropython.org/en/latest/reference/packages.html#distribution-packages
  - https://medium.com/google-cloud/connecting-micropython-devices-to-google-cloud-iot-core-3680e632681e
  - [Raspberry Pi - Getting Started](https://www.raspberrypi.org/products/raspberry-pi-pico/)
- Wait a max time (3 seconds?) for shelf number
>>>>>>> worldcat
