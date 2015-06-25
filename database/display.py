#!/usr/bin/python
# ========= HASHBANG LINE ABOVE IS MAGIC! =========
# ========= (Must be first line of file.) =========


#================= IMPORTS =====================

import os
import cgi
import cgitb
#cgitb.enable()  #diag info --- comment out once full functionality achieved

import time

import sys

sys.path.insert(0, '../cgiToDict/')
import cgiDeal

# ~~~~~~~~~~~~~~~ auxiliary files ~~~~~~~~~~~~~~~~~
#file to store users and their passwords:
userfile="../site_data/users.csv"

#file to store users currently logged in:
currentUsersFile="../site_data/usersOnline.csv"

#pages to navigate to:
addForm="addForm.py"
dashboard="dashboard.py"
gallery="gallery.py"
profile="profiles.py"

#login page:
loginPage="../index.html"

#page to load to logout:
logoutPage="logout.py"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#validate form input
def valid():
    fsd=cgiDeal.FStoD()
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
    fsd=cgiDeal.FStoD()
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


#if user logged in, return session string, otherwise empty string
def sessionStr():
    fsd=cgiDeal.FStoD()
    if not(valid()):
        return ''
    u=fsd['uname']
    s=fsd['usecret']
    i=fsd['uip']
    return '?uname='+u+'&usecret='+s+'&uip='+i


#build an HTML hyperlink containing this user's session string
#destination: dst, display text: visText
def sessionLinkify(dst,visText):
    retStr = '<a href="'+ dst
    retStr += sessionStr()
    retStr += '">'
    retStr += visText
    retStr += "</a>"
    return retStr


# =================== DATA ANALYSIS =====================


#grab cgi data
fsd = cgiDeal.FStoD()


#returns the most used tag
def mostUsedTag():
    username = fsd['uname']
    tags = open('userTags.csv','r')
    rtags = tags.readlines()
    tags.close()

    buckets = {}

    for eachLine in rtags:
        tagL = eachLine[:-1].split(",")[1:]
        for tag in tagL:
            if tag in buckets:
                buckets[tag] += 1
            else:
                buckets[tag] = 1
    if buckets == {}:
        return "No hashtags found"
    maxValue = max(buckets.values())
    for key in buckets:
        if maxValue == buckets[key]:
            return key

# =================== HELPER FUNCTIONS =====================


#wraps a div with the appropriate class around the given string
def divIt(type,s):
    if type == "txt":
        return '<div class="txt">' + s + '</div>'
    elif type == "img":
        return '<div class="img">' + s + '</div>'
    elif type == "link":
        return '<div class="img">' + s + '</div>'

#checks whether the input is a hex-formatted color
def isHex(bgrColor):
    if bgrColor[0] == "#" and (len(bgrColor) == 7 or len(bgrColor) == 4):
        try:
            bgrColor = int(bgrColor[1:], 16) # convert from str to hex
            return True
        except:
            return False
    elif len(bgrColor) == 6 or len(bgrColor) == 3:
        try:
            bgrColor = int(bgrColor, 16) # convert from str to hex
            return True
        except:
            return False
    return False

# =================== FUNCTIONS FOR DISPLAYING DATA =====================

#deal with commas in user input by replacing them with '~~'
#this can be undone later when the item is pulled up later
def commaDeal(item):
    if item.find(",") != -1:
        return item.replace(",", "~~")
    else:
        return item


#get given tag's corresponding image
def getImgs(tag):

    file = open('userTags.csv', 'r')
    lines = file.readlines()
    file.close()

    markL = []
    tagList = []

    for line in lines:
        if line.split(",")[0] == fsd['uname'] or line.split(",")[0] == fsd['uname'] + "\n":
            tagList = line[:-1].split(",")[1:]
    pos = 0
    while pos < len(tagList):
        if tagList[pos].replace("~~", ",") == tag:
            markL.append(pos)
        pos += 1

    # --------------------------------------

    file = open('userImgs.csv', 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        if line.split(",")[0] == fsd['uname'] or line.split(",")[0] == fsd['uname'] + "\n":
            capsList = line[:-1].split(",")[1:]

    corrL = []
    try:
        for mark in markL:
            corrL.append(capsList[mark])
    except:
        return corrL
    return corrL


#get given tag's corresponding caption
def getCaps(tag):

    file = open('userTags.csv', 'r')
    lines = file.readlines()
    file.close()

    markL = []
    tagList = []

    for line in lines:
        if line.split(",")[0] == fsd['uname'] or line.split(",")[0] == fsd['uname'] + "\n":
            tagList = line[:-1].split(",")[1:]
    pos = 0
    while pos < len(tagList):
        if tagList[pos].replace("~~", ",") == tag:
            markL.append(pos)
        pos += 1

    # --------------------------------------

    file = open('userCaps.csv', 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        if line.split(",")[0] == fsd['uname'] or line.split(",")[0] == fsd['uname'] + "\n":
            imgList = line[:-1].split(",")[1:]

    corrL = []
    try:
        for mark in markL:
            corrL.append(imgList[int(mark)])
    except:
        return corrL
    return corrL

#returns the maximum number of tags
def maxTags():
    file = open('userTags.csv', 'r')
    lines = file.readlines()
    file.close()

    number = 0

    for line in lines:
        if line.split(",")[0] == fsd['uname'] or line.split(",")[0] == fsd['uname'] + "\n":
            tags = line[:-1].split(",")[1:]
            number = len(tags)
    return number

# =================== CLOCK WIDGET =====================

#calc time
def clock():
    timeElapsed = time.time() # the time elapsed since the epoch (aka the starting day) began
    currentTime = time.localtime(timeElapsed) # converts timeElapsed to actual dates
    return formatTime(currentTime)

#format time to print
def formatTime(timeStr):
    currentTime = time.asctime(timeStr) # converts localtime to a more readable format

    date = currentTime[:11]
    hrMin = currentTime[11:16]
    year = currentTime[20:]

    if date[8] == "":
        date = date[:8] + date[9]

    hour = int(hrMin[:2])
    if hour == 0:
        hrMin = '12' + hrMin[2:] + " AM "
    elif hour < 12:
        hrMin = str(hour) + hrMin[2:] + " AM "
    elif hour == 12:
        hrMin = hrMin + " PM "
    elif hour > 12:
        hrMin = str((hour % 12)) + hrMin[2:] + " PM "

    return date + hrMin + year

#----------------------------------------------
# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========
fsd = cgiDeal.FStoD()

htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title>" + fsd['uname'] + "'s Display </title>"
htmlStr += """
        <link rel="stylesheet" type="text/css" href="../display.css">

        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

        <!-- Latest compiled and minified JavaScript -->
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
    </head>
"""
htmlStr += "<body>"

#color the jumbotron's background based on the input
if 'color' in fsd and isHex(fsd['color']):
    htmlStr += "<style> .jumbotron { background-color:" + fsd['color'] + "; text-align:center;} </style>"


# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~
if not valid():
    htmlStr += "session string problem?"
else:
    validated = authSession()

    if validated:

        #header
        htmlStr += '<div class="jumbotron" ><h1>' + fsd['uname'] + "'s Display</h1></div>"
        htmlStr += '<div class="clock">' + clock() + "<br></div>"

        #links to other pages/navigation
        htmlStr += "<a href='" + profile + sessionStr()+ "'>Your Profile</a><br>"
        htmlStr += "<a href='" + addForm + sessionStr() + "'>Add Items</a><br>"
        htmlStr += "<a href='" + dashboard + sessionStr()+ "'>Dashboard</a><br>"
        htmlStr += "<a href='" + gallery + sessionStr()+ "'>Gallery</a><br>"
        htmlStr += "<br>" + sessionLinkify(logoutPage,'Logout') + "<br><br>"

        #data analysis to display
        if 'freqTag' in fsd:
            htmlStr += "Most used tags: " + mostUsedTag() + "<br>"

        # PRINT CHOSEN TAG'S CAPTION AND IMAGE

        number = maxTags()
        for i in range(1, number + 1):
            if str(i) in fsd:

                capL = getCaps(fsd[str(i)])
                imgL = getImgs(fsd[str(i)])

                pos = 0
                while pos < len(capL):
                    htmlStr += "<div class='imgandcap'><img src='"
                    htmlStr += imgL[pos].replace("~~",",") + "'" + " alt='"
                    htmlStr += capL[pos].replace("~~",",") + "'/><br>"
                    if 'showcap' in fsd:
                        htmlStr += "<div class='cap'>" + capL[pos].replace("~~",",") + "</div><br><br>"
                    htmlStr += "</div>"
                    pos += 1

        #    htmlStr += "You have not selected any preferences yet." + \
        #    "Go to the dashboard to select items to display on this page."

    else:
        #if user not logged in
        htmlStr += "<br>Logged in you are not. Click "
        htmlStr += '<a href="'+ loginPage + '">'
        htmlStr += "here</a> to remedy."
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

htmlStr += "</body></html>"


print htmlStr