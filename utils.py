from urllib2 import urlopen, Request
from urllib import quote_plus
from json import loads
from os import urandom
from patterns import name_patterns

def who(query):
    '''Returns a substring of the query that is most likely to be a name.

    Handles any Unicode string, but will work best if the query only contains
    ASCII characters or characters in the Latin-1 Supplement Unicode block.

    If no name can be found, the entire query is returned.
    '''
    for pattern in name_patterns:
        match = pattern.search(query)
        if match:
            return match.group(0)

def get_secret_key():
    '''Returns a key that may be used to secure a Flask session

    The key is a 32-character string generated with the os.urandom function.
    '''
    return urandom(32)
