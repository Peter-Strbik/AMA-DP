# -*- coding: utf-8 -*-
from re import compile, VERBOSE, UNICODE, DOTALL

# According to the UK Government Data Standards Catalogue
# (http://webarchive.nationalarchives.gov.uk/+/http://www.cabinetoffice.gov.uk/media/254290/GDS%20Catalogue%20Vol%202.pdf),
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
#                [A-Z][ ']  # a capital letter followed by a separator and an
#                [A-Z]?     # optional capital letter, for names like O'brien
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
#                [A-Z][ ']  #
#                [A-Z]?     #
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
#                [A-Z][ ']  #
#                [A-Z]?     #
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
                [a-z\u00DF-\u00F6\u00F8-\u00FF]{1,3}
                [ '][A-Z\u00C0-\u00D6\u00D8-\u00DE]
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
                [a-z\u00DF-\u00F6\u00F8-\u00FF]{1,3}
                [ '][A-Z\u00C0-\u00D6\u00D8-\u00DE]
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

# Modified version of regex posted by Alok Chaudhary at
# http://stackoverflow.com/questions/15491894/regex-to-validate-date-format-dd-mm-yyyy
# Works for dates of the form day-month-year:
# 22-11-15
# 29/Feb/2000
# 1.1.9999
date_pattern1 = compile(ur"""
    (?:                                  # start of "Date Boundary"
        ^                                # start of string
        |                                # or
        (?<=                             # start of positive lookbehind
            [\s!-/:-@\[-`{-~]|           # ASCII whitespace or punctuation
            [\u2000-\u206F\u2E00-\u2E7F] # Unicode whitespace or punctuation
            )                            # end of positive lookbehind
        )                                # end of "Date Boundary"
                                         # start of "Day under 29"
    (?:0?[1-9]|1\d|2[0-8])(/|-|\.)       # number in 1-28, then a separator
    (?:                                  # start of "Month after Day under 29"
        0?[1-9]                          # number in 1-9
        |                                # or
        1[0-2]                           # number in 10-12
        |                                # or
        Jan|Feb|Mar|Apr|May|Jun|         # 3-letter appreviation of the name
        Jul|Aug|Sep|Oct|Nov|Dec          # of any month
        )                                # end of "Month after Day under 29"
    \1                                   # repeat previous separator
    (?:[1-9]\d)?                         # optional first two digits of year
    \d\d                                 # last two digits of year
                                         # end of "Day under 29"
    |                                    # or
                                         # start of "Day 29, 30, or 31"
    (?:                                  # start of "Day and Month"
        (?:                              # start of "Day 29 or 30"
            (?:29|30)(/|-|\.)            # 29 or 30 followed by a separator
            (?:                          # start of "Month after Day 29 or 30"
                0?[13-9]                 # number in 1-9 except 2 (February)
                |                        # or
                1[0-2]                   # number in 10-12
                |                        # or
                Jan|Mar|Apr|May|Jun|     # 3-letter appreviation of the name
                Jul|Aug|Sep|Oct|Nov|Dec  # of any month other than February
                )                        # end of "Month after Day 29 or 30"
            \2                           # repeat previous separator
            )                            # end of "Day 29 or 30"
        |                                # or
        (?:                              # start of "Day 31"
            31(/|-|\.)                   # 31 followed by a separator
            (?:                          # start of "Month after Day 31"
                0?[13578]                # 1-digit month with 31 days
                |                        # or
                1[02]                    # 2-digit month with 31 days
                |                        # or
                Jan|Mar|May|Jul|Aug|     # 3-letter appreviation of the name
                Oct|Dec                  # of any month with 31 days
                )                        # end of "Month after Day 31"
            )                            # end of "Day 31"
        \3                               # repeat previous separator
        )                                # end of "Day and Month"
    (?:[1-9]\d)?                         # optional first two digits of year
    \d\d                                 # last two digits of year
                                         # end of "Day 29, 30, or 31"
    |                                    # or
    (?:                                  # start of "February 29th"
        29(/|-|\.)                       # 29 followed by a separator
        (?:0?2|Feb)                      # 2 (February)
        \4                               # repeat previous separator
        (?:                              # start of "Year after February 29th"
                                         # start of "Leap Year not ending in 00"
            (?:[1-9]\d)?                 # optional first two digits of year
            (?:                          # start of "2-digit number div. by 4"
                0[48]                    # 04 or 08
                |                        # or
                [2468][048]              # 20, 24, 28, 40, 44, 48, ...
                |                        # or
                [13579][26]              # 12, 16, 32, 36, 52, 56, ...
                )                        # end of "2-digit number div. by 4"
                                         # end of "Leap Year not ending in 00"
            |                            # or
                                         # start of "Leap Year ending in 00"
            (?:[13579][26]|[2468][048])  # 12, 16, 20, 24, 28, 32, ...
            00                           # last two digits of year
                                         # end of "Leap Year ending in 00"
            )                            # end of "Year after February 29th"
        )                                # end of "February 29th"
    (?:                                  # start of "Date Boundary"
        $                                # end of string
        |                                # or
        (?=                              # start of positive lookahead
            [\s!-/:-@\[-`{-~]|           # ASCII whitespace or punctuation
            [\u2000-\u206F\u2E00-\u2E7F] # Unicode whitespace or punctuation
            )                            # end of positive lookahead
        )                                # end of "Date Boundary"
    """, VERBOSE|UNICODE)

# Works for dates of the form month-day-year:
# 11-22-15
# Feb/29/2000
# 1.1.9999
date_pattern1 = compile(ur"""
    (?:                                  # start of "Date Boundary"
        ^                                # start of string
        |                                # or
        (?<=                             # start of positive lookbehind
            [\s!-/:-@\[-`{-~]|           # ASCII whitespace or punctuation
            [\u2000-\u206F\u2E00-\u2E7F] # Unicode whitespace or punctuation
            )                            # end of positive lookbehind
        )                                # end of "Date Boundary"
                                         # start of "Day under 29"
    (?:                                  # start of "Month after Day under 29"
        0?[1-9]                          # number in 1-9
        |                                # or
        1[0-2]                           # number in 10-12
        |                                # or
        Jan|Feb|Mar|Apr|May|Jun|         # 3-letter appreviation of the name
        Jul|Aug|Sep|Oct|Nov|Dec          # of any month
        )                                # end of "Month after Day under 29"
    (/|-|\.)(?:0?[1-9]|1\d|2[0-8])       # a separator, then a number in 1-28
    \1                                   # repeat previous separator
    (?:[1-9]\d)?                         # optional first two digits of year
    \d\d                                 # last two digits of year
                                         # end of "Day under 29"
    |                                    # or
                                         # start of "Day 29, 30, or 31"
    (?:                                  # start of "Day and Month"
        (?:                              # start of "Day 29 or 30"
            (?:                          # start of "Month after Day 29 or 30"
                0?[13-9]                 # number in 1-9 except 2 (February)
                |                        # or
                1[0-2]                   # number in 10-12
                |                        # or
                Jan|Mar|Apr|May|Jun|     # 3-letter appreviation of the name
                Jul|Aug|Sep|Oct|Nov|Dec  # of any month other than February
                )                        # end of "Month after Day 29 or 30"
            (/|-|\.)(?:29|30)            # a separator followed by 29 or 30
            \2                           # repeat previous separator
            )                            # end of "Day 29 or 30"
        |                                # or
        (?:                              # start of "Day 31"
            (?:                          # start of "Month after Day 31"
                0?[13578]                # 1-digit month with 31 days
                |                        # or
                1[02]                    # 2-digit month with 31 days
                |                        # or
                Jan|Mar|May|Jul|Aug|     # 3-letter appreviation of the name
                Oct|Dec                  # of any month with 31 days
                )                        # end of "Month after Day 31"
            )                            # end of "Day 31"
            (/|-|\.)31                   # a separator followed by 31
        \3                               # repeat previous separator
        )                                # end of "Day and Month"
    (?:[1-9]\d)?                         # optional first two digits of year
    \d\d                                 # last two digits of year
                                         # end of "Day 29, 30, or 31"
    |                                    # or
    (?:                                  # start of "February 29th"
        (?:0?2|Feb)                      # 2 (February)
        (/|-|\.)29                       # a separator followed by 29
        \4                               # repeat previous separator
        (?:                              # start of "Year after February 29th"
                                         # start of "Leap Year not ending in 00"
            (?:[1-9]\d)?                 # optional first two digits of year
            (?:                          # start of "2-digit number div. by 4"
                0[48]                    # 04 or 08
                |                        # or
                [2468][048]              # 20, 24, 28, 40, 44, 48, ...
                |                        # or
                [13579][26]              # 12, 16, 32, 36, 52, 56, ...
                )                        # end of "2-digit number div. by 4"
                                         # end of "Leap Year not ending in 00"
            |                            # or
                                         # start of "Leap Year ending in 00"
            (?:[13579][26]|[2468][048])  # 12, 16, 20, 24, 28, 32, ...
            00                           # last two digits of year
                                         # end of "Leap Year ending in 00"
            )                            # end of "Year after February 29th"
        )                                # end of "February 29th"
    (?:                                  # start of "Date Boundary"
        $                                # end of string
        |                                # or
        (?=                              # start of positive lookahead
            [\s!-/:-@\[-`{-~]|           # ASCII whitespace or punctuation
            [\u2000-\u206F\u2E00-\u2E7F] # Unicode whitespace or punctuation
            )                            # end of positive lookahead
        )                                # end of "Date Boundary"
    """, VERBOSE|UNICODE)

date_patterns = [date_pattern1]