# -*- coding: utf-8 -*-
from urllib2 import urlopen, Request
from urllib import quote_plus
from json import loads
from re import compile, VERBOSE
from os import urandom

# According to the UK Government Data Standards Catalogue
# (http://webarchive.nationalarchives.gov.uk/+/http://
# www.cabinetoffice.gov.uk/media/254290/GDS%20Catalogue%20Vol%202.pdf),
# English forenames and surnames should be up to 35 characters long.

# For typical American names:
# Dennis Yatunin
# Barack H. Obama
# Tasty Apple Cider
simple_name = compile(r"""
    \b                    # word boundary
    [A-Z][a-z]{1,34}\     # first name followed by space (35 char max)
    (?:                   # start of optional middle name (not captured)
        [A-Z][a-z]{1,34}\ # middle name followed by space (35 char max)
        |                 # or
        [A-Z]\.\          # middle initial followed by period and space
        )?                # end of optional middle name
    [A-Z][a-z]{1,34}      # last name (35 char max)
    \b                    # word boundary
    """, VERBOSE)

# For non-typical names with ASCII letters and possibly periods,
# apostrophes, or hyphens:
# Luther O'Neil McCormick
# Baron Wolfgang von Strucker
# His Royal Highness Q. Q. Oh-So-Tasty Apple Cider
complex_name = compile(r"""
    \b                     # word boundary
    (?:                    # start of "name element" (not captured)
        (?:                # start of "initial element" (not captured)
            [A-Z]\.        # initial followed by a period
            )              # end of "initial element"
        |                  # or
        (?:                # start of "full element" (not captured)
            (?:            # start of "full element prefix" (not captured)
                [A-Z]      # just a capital letter, for ordinary names
                |          # or
                [A-Z]      # a capital letter followed by a separator and an
                [ '][A-Z]? # optional capital letter, for names like O'brien
                |          # or
                [a-z]{1,3} # a 1-3 letter preposition, then a separator
                [ '][A-Z]  # and a capital letter, for names like du Bourg
                )          # end of "full element prefix"
            [a-z]{1,34}    # up to 34 lowercase letters
            )              # end of "full element"
        [ -]               # a space or a hyphen
        )                  # end of "name element"
    {1,9}                  # anywhere from 1-9 "name elements" are allowed
    (?:                    # start of "final name element" (2-10 in total)
        (?:                # start of "initial element" (same as before)
            [A-Z]\.        #
            )              # end of "initial element"
        |                  # or
        (?:                # start of "full element" (same as before)
            (?:            #
                [A-Z]      #
                |          #
                [A-Z]      #
                [ '][A-Z]? #
                |          #
                [a-z]{1,3} #
                [ '][A-Z]  #
                )          #
            [a-z]{1,34}    #
            )              # end of "full element" (no space or hyphen now)
        )                  # end of "final name element"
    \b                     # word boundary
    """, VERBOSE)

# For many international names with ASCII letters or letters in the Latin-1
# Supplement Unicode block, and possibly periods, apostrophes, or hyphens:
# Björk Guðmundsdóttir
# José Eduardo Santos Tavares-Silva
# Dies Ist Äußerst Köstliche Apfelwein
international_name = compile(r"""
    \b
    (?:
        (?:[A-Z\u00C0-\u00D6\u00D8-\u00DE]\.)|
        # U+007B (after z) through U+00BF are symbols and control characters
        # U+00D7 is the division symbol
        (?:
            (?:
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]|
                [A-Z\u00C0-\u00D6\u00D8-\u00DE][ ']
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]?|
                [a-z\u00DF-\u00F6\u00F8-\u00FF]+[ ']
                # there is no limit on lengths of prepositions
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]
                )
            [a-z\u00DF-\u00F6\u00F8-\u00FF]+
            # U+00F7 is the multiplication symbol
            # there is no limit on lengths of "full elements"
            )[ -]
        )+ # there is no limit on the number of "name elements"
    (?:
        (?:[A-Z\u00C0-\u00D6\u00D8-\u00DE]\.)|
        (?:
            (?:
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]|
                [A-Z\u00C0-\u00D6\u00D8-\u00DE][ ']
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]?|
                [a-z\u00DF-\u00F6\u00F8-\u00FF]+[ ']
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]
                )
            [a-z\u00DF-\u00F6\u00F8-\u00FF]+
            )
        )
    \b
    """, VERBOSE)

# For many more international names with ASCII letters or letters in the
# Latin-1 Supplement Unicode block, the Latin Extended-A block, the Latin
# Extended-B block, the IPA Extensions block, the Spacing Modifier Letters
# block, or the Latin Extended Additional block, and possibly commas,
# periods, apostrophes, or hyphens:
# ʻĂḇēḏ-nəḡô
# Nguyễn Tấn Dũng
# ʞunɹp ɹǝʌǝ ǝʌɐɥ ı ɹǝpıɔ ǝןddɐ ʇsǝq ǝɥʇ ʎןǝʇnןosqɐ sı sıɥʇ poɓ ʎɯ ɥo
very_international_name = compile(r"""
    \b
    [A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u1E00-\u1EFF ,.'-]+
    \b
    """, VERBOSE)

# For all other garbage:
# 王宜成
# .-../--/.-/---//..../.-/..../.-////
# 49 20 6c 69 6b 65 20 41 70 70 6c 65 20 43 69 64 65 72
garbage_name = compile('.*')

patterns = [
    simple_name,
    complex_name,
    international_name,
    very_international_name,
    garbage_name
    ]

def who(query):
    for pattern in patterns:
        match = pattern.match(query)
        if match:
            return match.group(0)

def get_secret_key():
    '''Returns a key that may be used to secure a Flask session

    The key is a 32-character string generated with the os.urandom function.
    '''
    return urandom(32)
