import isbn_api
from sheets import insert_book_in_sheet

def scan_book(service):
    isbn = input("Scan ISBN:\n")
    shelf = ""
    # shelf = input("Shelf #:\n")
    author_str = ""
    title = ""

    statusOL, author_str, title = isbn_api.openlibrary(isbn)
    if statusOL != 1:
        statusWC, author_strWC, titleWC = isbn_api.worldcat(isbn)
        if statusWC == -1:
            print("Book not found! Inserting empty row (ISBN only).")
        # backfill from WC if OL infos are incomplete
        elif author_str == "":
            author_str = author_strWC
        elif title == "":
            title = titleWC

    insert_book_in_sheet(service, author_str, title, shelf, isbn)
