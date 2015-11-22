# -*- coding: utf-8 -*-
from urllib2 import urlopen, Request
from urllib import quote_plus
from json import loads
from re import compile, VERBOSE, UNICODE, DOTALL
from os import urandom

# According to the UK Government Data Standards Catalogue
# (http://webarchive.nationalarchives.gov.uk/+/http://
# www.cabinetoffice.gov.uk/media/254290/GDS%20Catalogue%20Vol%202.pdf),
# English forenames and surnames should be up to 35 characters long.

# Simplest Name Regex
# Works for typical American names:
# - Dennis Yatunin
# - Barack H. Obama
# - Tasty Apple Cider
#
#    \b                    # word boundary
#    [A-Z][a-z]{1,34}\     # first name followed by space (35 char max)
#    (?:                   # start of optional middle name (not captured)
#        [A-Z][a-z]{1,34}\ # middle name followed by space (35 char max)
#        |                 # or
#        [A-Z]\.\          # middle initial followed by period and space
#        )?                # end of optional middle name
#    [A-Z][a-z]{1,34}      # last name (35 char max)
#    \b                    # word boundary

# Advanced Name Regex
# Works for non-typical names with ASCII letters and possibly periods,
# apostrophes, or hyphens:
# - Luther O'Neil McCormick
# - Baron Wolfgang von Strucker
# - His Royal Highness Q. Q. Oh-So-Tasty Apple Cider
#
#    \b                     # word boundary
#    (?:                    # start of "first name element" (not captured)
#        (?:                # start of "initial element" (not captured)
#            [A-Z]\.        # initial followed by a period
#            )              # end of "initial element"
#        |                  # or
#        (?:                # start of "full element" (not captured)
#            (?:            # start of "full element prefix" (not captured)
#                [A-Z]      # just a capital letter, for ordinary names
#                |          # or
#                [A-Z]      # a 2-3 letter preposition (a capital letter
#                [a-z]{1,2} # followed by 1-2 lowercase letters), then a
#                [A-Z]      # capital letter, for names like MacDonald
#                |          # or
#                [A-Z]      # a capital letter followed by a separator and an
#                [ '][A-Z]? # optional capital letter, for names like O'brien
#                )          # end of "full element prefix"
#            [a-z]{1,34}    # up to 34 lowercase letters
#            )              # end of "full element"
#        [ -]               # a space or a hyphen
#        )                  # end of "first name element"
#    (?:                    # start of "central name element" (not captured)
#        (?:                # start of "initial element" (same as first elem.)
#            [A-Z]\.        #
#            )              # end of "initial element"
#        |                  # or
#        (?:                # start of "full element" (similar to first elem.)
#            (?:            # start of "full element prefix"
#                [A-Z]      #
#                |          #
#                [A-Z]      #
#                [a-z]{1,2} #
#                [A-Z]      #
#                |          #
#                [A-Z]      #
#                [ '][A-Z]? #
#                |          # or (in addition to "prefixes" in first elem.)
#                [a-z]{1,3} # a lowercase preposition, then a separator
#                [ '][A-Z]  # and a capital letter, for names like du Bourg
#                )          # end of "full element prefix"
#            [a-z]{1,34}    #
#            )              # end of "full element"
#        [ -]               #
#        )                  # end of "central name element"
#    {,8}                   # up to 8 "central name elements" are allowed
#    (?:                    # start of "final name element" (2-10 in total)
#        (?:                # start of "initial element" (same as first elem.)
#            [A-Z]\.        #
#            )              # end of "initial element"
#        |                  # or
#        (?:                # start of "full element" (same as central elem.)
#            (?:            #
#                [A-Z]      #
#                |          #
#                [A-Z]      #
#                [a-z]{1,2} #
#                [A-Z]      #
#                |          #
#                [A-Z]      #
#                [ '][A-Z]? #
#                |          #
#                [a-z]{1,3} #
#                [ '][A-Z]  #
#                )          #
#            [a-z]{1,34}    #
#            )              # end of "full element" (no space or hyphen now)
#        )                  # end of "final name element"
#    \b                     # word boundary

# Very Advanced Name Regex (Advanced Name Regex modified to handle non-ASCII
# letters)
# Works for many names with ASCII letters or letters in the Latin-1
# Supplement Unicode block, and possibly periods, apostrophes, or hyphens:
# - Björk Guðmundsdóttir
# - José Eduardo Santos Tavares-Silva
# - Dies Ist Äußerst Köstliche Apfelwein

name_pattern1 = compile(ur"""
    \b
    (?:
        (?:[A-Z\u00C0-\u00D6\u00D8-\u00DE]\.)|
        (?:
            (?:
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]|
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]
                [a-z\u00DF-\u00F6\u00F8-\u00FF]{1,2}
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]|
                [A-Z\u00C0-\u00D6\u00D8-\u00DE][ ']
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]?
                )
            [a-z\u00DF-\u00F6\u00F8-\u00FF]{1,34}
            )[ -]
        )
    (?:
        (?:[A-Z\u00C0-\u00D6\u00D8-\u00DE]\.)|
        (?:
            (?:
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]|
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]
                [a-z\u00DF-\u00F6\u00F8-\u00FF]{1,2}
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]|
                [A-Z\u00C0-\u00D6\u00D8-\u00DE][ ']
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]?|
                [a-z\u00DF-\u00F6\u00F8-\u00FF]{1,3}[ ']
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]
                )
            [a-z\u00DF-\u00F6\u00F8-\u00FF]{1,34}
            )[ -]
        ){,8}
    (?:
        (?:[A-Z\u00C0-\u00D6\u00D8-\u00DE]\.)|
        (?:
            (?:
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]|
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]
                [a-z\u00DF-\u00F6\u00F8-\u00FF]{1,2}
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]|
                [A-Z\u00C0-\u00D6\u00D8-\u00DE][ ']
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]?|
                [a-z\u00DF-\u00F6\u00F8-\u00FF]{1,3}[ ']
                [A-Z\u00C0-\u00D6\u00D8-\u00DE]
                )
            [a-z\u00DF-\u00F6\u00F8-\u00FF]{1,34}
            )
        )
    \b
    """, VERBOSE|UNICODE)

# Foreign Name Regex
# Works for many foreign names with ASCII letters or letters in the
# Latin-1 Supplement Unicode block, the Latin Extended-A block, the Latin
# Extended-B block, the IPA Extensions block, the Spacing Modifier Letters
# block, or the Latin Extended Additional block, and possibly commas,
# periods, apostrophes, or hyphens:
# - ʻĂḇēḏ-nəḡô
# - Nguyễn Tấn Dũng
# - ʞunɹp ɹǝʌǝ ǝʌɐɥ ı ɹǝpıɔ ǝןddɐ ʇsǝq ǝɥʇ ʎןǝʇnןosqɐ sı sıɥʇ poɓ ʎɯ ɥo

name_pattern2 = compile(ur"""
    \b
    [A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u1E00-\u1EFF ,.'-]+
    \b
    """, VERBOSE|UNICODE)

# "Just Give Up" Regex
# Works for all other junk:
# - 王宜成
# - .-../--/.-/---//..../.-/..../.-////
# - 49 20 6c 69 6b 65 20 41 70 70 6c 65 20 43 69 64 65 72
name_pattern3 = compile('.*', DOTALL)

name_patterns = [name_pattern1, name_pattern2, name_pattern3]

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
