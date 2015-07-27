#!/usr/bin/python
# ========= HASHBANG LINE ABOVE IS MAGIC! =========
# ========= (Must be first line of file.) =========

# =================== IMPORTS ========================
import os
import cgi
import cgitb
#cgitb.enable()  #diag info --- comment out once full functionality achieved

#import cgiDeal from another folder
import sys

sys.path.insert(0, '../cgiToDict/')
import cgiDeal

 #####################################################
 ## Back-End Script for USER ACCOUNT AUTHENTICATION
 ## by
 ##   ___|  |             |
 ##  |      |  |   |   _` |   _ \
 ##  |      |  |   |  (   |   __/
 ## \____| _| \__, | \__,_| \___|
 ##  | ) __ __|__|/     |          _|   _|         | )
 ## V V     |    __ \   |  |   |  |    |    |   | V V
 ##         |    | | |  |  |   |  __|  __|  |   |
 ##        _|   _| |_| _| \__,_| _|   _|   \__, |
 ##   ___|  _)               |        _)   ____/
 ## \___ \   |  __ \    __|  |   _` |  |   __|
 ##       |  |  |   |  (     |  (   |  |  |
 ## _____/  _| _|  _| \___| _| \__,_| _| _|
 #####################################################

# ~~~~~~~~~~~~~~~ auxiliary files ~~~~~~~~~~~~~~~~~
#file to store users currently logged in:
currentUsersFile="../site_data/usersOnline.csv"

#login page:
loginPage="../index.html"

#query string dictionary using CGI
fsd=cgiDeal.FStoD()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#validate user input
def valid():
    if not ('uname' in fsd):
        return False
    if not ('usecret' in fsd):
        return False
    if not ('uip' in fsd):
        return False
    if fsd['uname'] == '':
        return False
    return True


#return True if user valid, False otherwise
def authSession():
    if not( valid() ):
        return False
    try:
        userlist = open(currentUsersFile,'r').readlines()
    except:
        return False
    for row in userlist:
        rowList=row.strip().split(',')
        if rowList[0]==fsd['uname']:
            if rowList[1]==fsd['usecret']:
                if rowList[2]==fsd['uip']:
                    return True
    return False


#remove an entry from logged-in-users file
#returns True if success, False otherwise
def remFrLoggedIn(u):
    currUserList=[]
    try:
        inStream=open(currentUsersFile, 'r')
        currUserList=inStream.readlines()
        inStream.close()
    except:
        return False
    outTxt=''
    for row in currUserList:
        if row.strip().split(',')[0] != u:
            outTxt += row
    try:
        outStream=open(currentUsersFile, 'w')
        outStream.write(outTxt)
        outStream.close()
    except:
        return False
    return True


# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========
htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title> Login Results </title>"
htmlStr += """
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

        <!-- Latest compiled and minified JavaScript -->
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>

        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
"""
htmlStr += "<body style='text-align:center;'>"

# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~
if not valid():
    htmlStr += "Session string problem?"
else:
    validated = authSession()
    #~~~~~~~~~~~~~~~~~~~ diag HTML... ~~~~~~~~~~~~~
    #htmlStr += "<h4>Dictionary of form data:</h4>"
    #htmlStr += str( fsd )
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if validated:
        htmlStr += "<h3>Logging out...</h3><br>"
        if remFrLoggedIn( fsd['uname'] ):
            htmlStr += "<h3>You have logged out.</h3>"
            htmlStr += '<br><a class="btn btn-success" href="'+ loginPage + '">'
            htmlStr += "Log In</a>"
    else:
        htmlStr += "<br><h3>You weren't logged in.</h3>"
        htmlStr += '<a href="'+ loginPage + '">'
        htmlStr += "Log In</a>"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


htmlStr += "</body></html>"


print htmlStr
