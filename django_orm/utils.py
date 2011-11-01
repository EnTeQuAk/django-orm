# -*- coding: utf-8 -*-

import unicodedata

def remove_diacritic(input):
    '''
    Accept a unicode string, and return a normal string (bytes in Python 3)
    without any diacritical marks.
    '''
    return unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore')
