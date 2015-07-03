#!usr/bin/python

'''
ABOUT THIS FILE:
 - this file contains functions that deal with cgi inputs

LEFT TO DO:
 - comments
 - comment out cgitb
'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~

import cgi
import cgitb

cgitb.enable() #comment out when done editing

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def FStoD():
    '''
    Converts cgi.FieldStorage() return value into a standard dictionary
    '''
    d = {}
    formData = cgi.FieldStorage()
    for k in formData.keys():
        d[k] = formData[k].value
    return d
