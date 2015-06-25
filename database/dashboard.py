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


# ~~~~~~~~~~~~~~~ auxiliary files ~~~~~~~~~~~~~~~~~
#file to store users and their passwords:
userfile="../site_data/users.csv"

#file to store users currently logged in:
currentUsersFile="../site_data/usersOnline.csv"

#pages to navigate to:
addForm="addForm.py"
profile="profiles.py"
gallery="gallery.py"
display="display.py"

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


#=============== FORM GENERATION ===================

#generate the html for an option in a select form with a given value and text
def checkGen(name,value,text):
    return '<input type="checkbox" name="' + name + '" value="' + value.replace("~~", ",") + '">' + text.replace("~~", ",") + "<br>"


#generates a series of <option>s for the tag form
#includes all the different tags a user has, with no repeats
def genTagForm(username):
    file = open('userTags.csv','r')
    read = file.readlines()
    file.close()

    html = "" #store form html

    for i in read:
        if i.split(',')[0] == username or i.split(",")[0] == username + "\n":
            tags = (i[:-1].split(","))[1:]
            usedTags = []
            pos = 1
            for eachTag in tags:
                if eachTag not in usedTags:
                    html += checkGen(str(pos),eachTag,eachTag)
                    usedTags.append(eachTag)
                    pos += 1
    return html



# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========
fsd = cgiDeal.FStoD()

htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title> " + fsd['uname'] + "'s Dashboard </title>"
htmlStr += """
        <link rel="stylesheet" type="text/css" href="../dashboard.css">

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

        #session
        session = "<input type='hidden' name='uname' value='" + fsd['uname'] + "' readonly='readonly'>"
        session += "<input type='hidden' name='usecret' value='" + fsd['usecret'] + "' readonly='readonly'>"
        session += "<input type='hidden' name='uip' value='" + fsd['uip'] + "' readonly='readonly'>"

        #header
        htmlStr += '<div class="jumbotron">'
        htmlStr += '<h1>' + fsd['uname'] + "'s Dashboard</h1></div>"

        #form
        htmlStr += "<form type='input' method='GET' action='" + display + "'/>"


        #most used tag
        htmlStr += "<span class='standalone'><input type='checkbox' name='freqTag'>Tell me which tag users use most</span><br><br>"

        #header color
        htmlStr += "<span class='question'>What color header would you like? (Please enter a hexadecimal representation) </span>"
        htmlStr += "<input type='text' name='color'> <br><br>"

        #choose a tag to show
        htmlStr += "<span class='question'>From which tags would you like to display content?</span><br> \
                    If there are no checkboxes below, you haven't added any entries.<br><br>"
        htmlStr += genTagForm(fsd['uname']) + "<br>"

        #show captions?
        htmlStr += "<span class='question'>Do you want to show picture captions?</span><br>"
        htmlStr += "If you choose to and not all of your images have captions, you might not have any to see.<br>"
        htmlStr += "<input type='checkbox' name='showcap'>Show captions<br><br>"

        #submit button
        htmlStr += session
        htmlStr += '<input class="btn btn-info" type="submit" value="Submit"><br><br>'
        htmlStr += "</form>"

        #links to other pages
        htmlStr += "<a href='" + profile + sessionStr() + "'>Your Profile</a><br>"
        htmlStr += "<a href='" + addForm + sessionStr() + "'>Add Items</a><br>"
        htmlStr += "<a href='" + gallery + sessionStr() + "'>Gallery</a><br>"

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