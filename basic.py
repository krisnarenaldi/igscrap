import mysql.connector
from mysql.connector import Error
#import requests

#koneksi
cnx = mysql.connector.connect(user='root', password='root', database='altera', port=8889)
cursor = cnx.cursor()


#fungsi
def key_exists(element,*keys):

    _element = element

    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

# def is_exist(url):
#     try:
#         req = requests.get(url)
#         #print(req.status_code)
#         if req.status_code == 200:
#             return True
#     except requests.exceptions.RequestException as er:
#         print(er)
#         return False
#     except requests.exceptions.ConnectionError as er2:
#         print("ERROR REQUESTS ConnectionError =",er2)
#         return False
#     except requests.exceptions.ReadTimeout as er3:
#         print("ERROR REQUEST ReadTimeout =",er3)
#         return False
#     except urllib3.exceptions.ReadTimeoutError as er4:
#         print("ERROR URLLIB3 ReadTimeoutError =",er4)
#         return False

def extract_url(url):
    url_list = url.lower().split(".")
    _url = ""

    if len(url_list) == 3:
        _url = url_list[1]+"."+url_list[2]
    else:
        _url = url

    return _url


def replaceChars(mainString,list_author):
    forbidden_chars = "!@#$%^&*()_+,<>/?~`:"
    newChar = ""
    # check apakah ada > 1 nama
    a_list = mainString.split(",")

    if len(a_list) == 1:
        for fc in forbidden_chars:
            if fc in mainString:
                mainString = mainString.replace(fc,newChar)
    else:
        mainString = a_list[0]

    mainString = mainString.strip()

    if mainString.lower() in list_author:
        mainString = "Unknown"

    return mainString

def getKompasAuthor(kompasauthor,url):
    a_list = kompasauthor.split(",")
    kompasiana_list = ["verified","unverified","trusted","untrusted"]

    _url = extract_url(url)

    for x in range(len(a_list)):
        if "kompas.com" in _url:
            if a_list[x].isdigit() == False and "kompas" not in a_list[x].lower():
                author = a_list[x]
        elif "kompasiana.com" in _url:
            if a_list[x].lower() not in kompasiana_list and a_list[x].lower() != _url:
                author = a_list[x]
        else:
            author = a_list[0]

    return author

def getWebAuthor(webauthor,url):
    a_list = webauthor.split(",")
    _url = extract_url(url)

    if len(a_list) != 1:
        for x in range(len(a_list)):
            if a_list[x].lower() !=  _url:
                author = a_list[x]
    else:
        author = a_list[0]

    return author

def isWebAuthor(author,url):
    _url = extract_url(url)

    if _url in author.lower():
        return True
    else:
        return False