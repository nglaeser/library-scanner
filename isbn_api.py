import requests
import xml.etree.ElementTree as ET

def openlibrary(isbn):
    try:
        bookinfo = requests.get(f"https://openlibrary.org/isbn/{isbn}.json").json()
    except:
        print("unable to find {} in OpenLibrary".format(isbn))
        return -1, None, None

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

    return 0, author_str, title

def worldcat(isbn):
    try:
        xml = requests.get(f"http://classify.oclc.org/classify2/Classify?isbn={isbn}&summary=true")
        root = ET.fromstring(xml.content)
        bookinfo = root.find('./*{http://classify.oclc.org}work')
        # `./*` means any node below (not just direct children)
        if bookinfo == None:
            print("unable to find {} in WorldCat".format(isbn))
            return -1, None, None
    except:
        print("error querying ISBN API")
        return -1, None, None

    # get author(s)
    try:
        authors_raw = bookinfo.get('author').split("|")
        # TODO remove authors with "[*]" after their names (editor, translator, etc.) e.g. "Schwarz, Benjamin [Translator]"
        authors = []
        for a in authors_raw:
            if "[" not in a:
                first_comma = a.find(",")
                # case: "Bonnefoy, Jean, 1950-" 
                second_comma = a.find(",",first_comma+1)
                if second_comma != -1:
                    a = a[:second_comma]
                # case: "Adams, Douglas 1952-2001"
                first_digit = -1
                for i,c in enumerate(a):
                    if c.isdigit():
                        first_digit = i
                        break
                if first_digit != -1:
                    a = a[:first_digit]

                authors += [a]
    except:
        # no author info
        authors = ""
    authors = [a.strip() for a in authors]
    author_str = "; ".join(authors)

    # get title
    try:
        title = bookinfo.get('title')
    except:
        # no title info
        title = ""
    
    status = 1
    if author_str == "" or title == "":
        status = 0
    return status, author_str, title
