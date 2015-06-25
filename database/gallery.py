#!/usr/bin/python
# ========= HASHBANG LINE ABOVE IS MAGIC! =========
# ========= (Must be first line of file.) =========

#===================== IMPORT =======================

import cgi
import cgitb
#cgitb.enable()  #diag info --- comment out once full functionality achieved

import sys

sys.path.insert(0, '../cgiToDict/')
import cgiDeal

import random



# ~~~~~~~~~~~~~~~ auxiliary files ~~~~~~~~~~~~~~~~~
#file to store users and their passwords:
userfile="../site_data/users.csv"

#file to store users currently logged in:
currentUsersFile="../site_data/usersOnline.csv"

#pages to navigate to:
addForm="addForm.py"
profile="profiles.py"
dashboard="dashboard.py"

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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def galleryList(lines, L):

    # removes newlines
    pos = 0
    while pos < len(lines):
        lines[pos] = lines[pos][:-1]
        pos += 1

    # gets the images for each user
    for line in lines:
        if line.find(",") != -1:
            L.extend(line.split(",")[1:])
    return L

def getGallery():
    file = open('userImgs.csv', 'r')
    imgs = file.readlines()
    file.close()

    imgL = []

    imgL = galleryList(imgs, imgL)

    if imgL == []:
        return "Nothing to show today. Try again when you or others have uploaded pics."
    # --------------------------------------

    file = open('userCaps.csv', 'r')
    caps = file.readlines()
    file.close()

    capL = []

    capL = galleryList(caps, capL)

    if capL == []:
        return "Nothing to show today. Try again when you or others have uploaded pics."
    # --------------------------------------
    # imgL is the list of img URLS
    # capL is the list of captions

    s = ""

    for i in range(len(imgL)):
        randNum = random.randrange(len(imgL))
        s += "<img src='" + imgL[randNum].replace("~~",",") + \
        "' alt='" + capL[randNum].replace("~~",",") + "'/><br>\n"

    return s



# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========
fsd = cgiDeal.FStoD()

htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title>Gallery</title>"
htmlStr += """
        <link rel="stylesheet" type="text/css" href="../display.css">

        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

        <!-- Latest compiled and minified JavaScript -->
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
    </head>
"""
htmlStr += "<body>"

# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~

if not valid():
    htmlStr += "session string problem?"
else:
    validated = authSession()
    if validated:
        #header
        htmlStr += '<div class="jumbotron"><h1>Gallery</h1><br>'
        htmlStr += "<p>View others' images</p></div><br>"

        #gallery
        htmlStr += getGallery()
        htmlStr += "<br><br>"

        #links to other pages
        htmlStr += "<a href='" + profile + sessionStr() + "'>Your Profile</a><br>"
        htmlStr += "<a href='" + addForm + sessionStr() + "'>Add Items</a><br>"
        htmlStr += "<a href='" + dashboard + sessionStr() + "'>Dashboard</a><br>"

        #link to logout
        htmlStr += "<br>" + sessionLinkify(logoutPage,'Logout')
    else:
        #if user not logged in
        htmlStr += "<br>Logged in you are not. Click "
        htmlStr += '<a href="'+ loginPage + '">'
        htmlStr += "here</a> to remedy."
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

htmlStr += "</body></html>"


print htmlStr