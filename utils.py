from urllib2 import urlopen, Request
from urllib import quote_plus
from json import loads
from os import urandom
from patterns import name_pattern, date_patterns, html_pattern, space_pattern
import requests, google, re

def getTextFromSearch(query):
    '''Returns a string containing all the text from the first 10 search results
    on google of a given query.

    All html tags and excess space has been removed, allowing for easy parsing.
    '''
    results = google.search(query, num = 10, start = 0, stop = 10)
    res = ""
    urls = []
    for i in results:
        urls.append(i)
    for url in urls:
        res += getTextFromPage(url)
    return res
    
def getTextFromPage(url):
    '''Returns a string of all the text found on the given url
    
    All html tags and excess spaces have been removed
    '''
    page = requests.get(url)
    raw = page.text
    lessRaw = re.sub(html_pattern, "", raw)
    finalText = re.sub(space_pattern, " ", lessRaw)
    return finalText

def who(query):
    '''Returns a substring of the query that is most likely to be a name.

    Handles any Unicode string, but will work best if the query only contains
    ASCII characters or characters in the Latin-1 Supplement Unicode block.

    If no name can be found, the entire query is returned.
    '''
    match = name_pattern.search(query)
    if match:
        return match.group(0)
    return query

def when(query):
    '''Returns a substring of the query that is most likely to be a date.

    Handles any Unicode string, but will work best if the query only contains
    ASCII characters or characters in the Latin-1 Supplement Unicode block.

    If no date can be found, the entire query is returned.
    '''
    for pattern in date_patterns:
        match = pattern.search(query)
        if match:
            return match.group(0)
    return query

def get_secret_key():
    '''Returns a key that may be used to secure a Flask session

    The key is a 32-character string generated with the os.urandom function.
    '''
    return urandom(32)
