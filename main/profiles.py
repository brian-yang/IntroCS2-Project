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
gallery = "gallery.py"
dashboard="dashboard.py"

#login page:
loginPage="../index.html"

#page to load to logout:
logoutPage="logout.py"

#query string dictionary using CGI
fsd=cgiDeal.FStoD()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#validate form input
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


#if user logged in, return session string, otherwise empty string
def sessionStr():
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
def getUsers(username):

    file = open('../site_data/userProfiles.csv', 'r')
    lines = file.readlines()
    file.close()

    userL = []

    for i in lines:
        if i.split(',')[0] != username and i.split(",")[0] != username + "\n":
            if i.split(",")[0][-1] == "\n":
                userL.append(i.split(",")[0][:-1])
            else:
                userL.append(i.split(",")[0])
    return userL

def userSelect(username):

    userL = getUsers(username)

    s = "<select name='friend'>\n"

    for user in userL:
        s += "<option value='" + user + "'>" + user + "</option>\n"

    s += "</select>"
    return s

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getPic(username):
    s = "<div class='square'>\n"

    image = ""

    file = open('../site_data/userProfiles.csv', 'r')
    lines = file.readlines()
    file.close()

    # removes newlines
    pos = 0
    while pos < len(lines):
        lines[pos] = lines[pos][:-1]
        pos += 1

    for i in lines:
        if i.split(',')[0] == username or i.split(",")[0] == username + "\n":
            image = i.split(',')[2]

    s += "<img src='" + image.replace("~~",",") + "' />"

    s += "</div><br>"
    return s

def writePic(img):
    try:
        file = open('../site_data/userProfiles.csv', 'r')
        lines = file.readlines()
        file.close()

        passed = False #have you passed the entry for this user?
        pre = "" #csv content pre-user
        entry = "" #csv user content
        post = "" #csv content post-user

        # writes to file
        for i in lines:
            if i.split(',')[0] == fsd['uname'] or i.split(",")[0] == fsd['uname'] + "\n":
                passed = True
                entry = i.split(",")[0] + "," + i.split(",")[1]
                entry += "," + img.replace(",","~~") + "\n"
            elif passed:
                post += i
            elif not passed:
                pre += i

        file = open('../site_data/userProfiles.csv', 'w')
        file.write(pre + entry + post)
        file.close()
    except:
        htmlStr += "ERROR!"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getTags(username):
    L = []

    file = open('../site_data/userTags.csv', 'r')
    lines = file.readlines()
    file.close()

    # removes newlines
    pos = 0
    while pos < len(lines):
        lines[pos] = lines[pos][:-1]
        pos += 1

    # gets the tags
    for line in lines:
        if line.split(",")[0] == username:
            L.extend(line.split(",")[1:])

    return L

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def getDescription(username):

    file = open('../site_data/userProfiles.csv', 'r')
    lines = file.readlines()
    file.close()

    # removes newlines
    pos = 0
    while pos < len(lines):
        lines[pos] = lines[pos][:-1]
        pos += 1

    # gets the tags
    for line in lines:
        if line.split(",")[0] == username:
            return line.split(",")[1].replace("~~",",").replace("@@","<br>")
    return ""

def writeDescription(description):
    try:
        file = open('../site_data/userProfiles.csv', 'r')
        read = file.readlines()
        file.close()

        passed = False #have you passed the entry for this user?
        pre = "" #csv content pre-user
        entry = "" #csv user content
        post = "" #csv content post-user

        # writes to file
        for i in read:
            if i.split(',')[0] == fsd['uname'] or i.split(",")[0] == fsd['uname'] + "\n":
                passed = True
                entry = i.split(",")[0] + ","
                entry += description.replace(",","~~").replace("\n","@@")
                entry += "," + i.split(",")[2][:-1] + "\n"
            elif passed:
                post += i
            elif not passed:
                pre += i

        file = open('../site_data/userProfiles.csv', 'w')
        file.write(pre + entry + post)
        file.close()
    except:
        htmlStr += "ERROR!"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def profDescription():
    session = "<input type='hidden' name='uname' value='" + fsd['uname'] + "' readonly='readonly'>"
    session += "<input type='hidden' name='usecret' value='" + fsd['usecret'] + "' readonly='readonly'>"
    session += "<input type='hidden' name='uip' value='" + fsd['uip'] + "' readonly='readonly'>"

    # form for description
    html = "<br><br>Update your description.<br>"
    html += "<form name='desc' type='input' method='GET' action='profiles.py'>"
    html += "<textarea name='description'>I am awesome!</textarea><br>"
    html += session
    html += "<input type='submit' value='Submit'>"
    html += "</form><br><br>"

    return html

def profImg():
    session = "<input type='hidden' name='uname' value='" + fsd['uname'] + "' readonly='readonly'>"
    session += "<input type='hidden' name='usecret' value='" + fsd['usecret'] + "' readonly='readonly'>"
    session += "<input type='hidden' name='uip' value='" + fsd['uip'] + "' readonly='readonly'>"

    # form for changing the profile image
    html = "<br><br>Change your profile picture by adding a URL!<br>"
    html += "<form name='profimg' type='input' method='GET' action='profiles.py'>"
    html += session
    html += "<input type='text' name='profilePic'>"
    html += "<input type='submit' value='Submit'>"
    html += "</form><br><br>"

    return html

def webpage():
    session = "<input type='hidden' name='uname' value='" + fsd['uname'] + "' readonly='readonly'>"
    session += "<input type='hidden' name='usecret' value='" + fsd['usecret'] + "' readonly='readonly'>"
    session += "<input type='hidden' name='uip' value='" + fsd['uip'] + "' readonly='readonly'>"

    # form for viewing other peoples' pages
    html = "<br><br>View other peoples' webpages.<br>"
    html += "<form name='webpage' type='input' method='GET' action='profiles.py'>"
    html += userSelect(fsd['uname'])
    html += session
    html += "<input type='submit' value='Submit'>"
    html += "</form><br><br>"

    return html

#----------------------------------------------
# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========

htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title>Profile</title>"
htmlStr += """
        <link rel="stylesheet" type="text/css" href="../css/profiles.css">
        <link rel="stylesheet" type="text/css" href="../css/navbar.css">

        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

        <!-- Latest compiled and minified JavaScript -->
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
    </head>

"""
htmlStr += "<body>"
# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~

#wrap an html tag around a string
def tagify(tag,s):
    return tag + s + "</" + tag[1:]


if not valid():
    htmlStr += "session string problem?"
else:
    validated = authSession()
    if validated:

        if 'friend' not in fsd: # display own page

            # links to other pages
            htmlStr += """
            <div class="navbar navbar-default">
                <div class="container-fluid">
                <!-- Brand and toggle get grouped for better mobile display -->

                    <!-- Collect the nav links, forms, and other content for toggling -->
                    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            """
            htmlStr += "\t\t<ul class='nav navbar-nav nav-justified'>\n"
            htmlStr += "<li>" + sessionLinkify("addForm.py","Add Images") + "</li>"
            htmlStr += "<li>" + sessionLinkify("dashboard.py","Dashboard") + "</li>"
            htmlStr += "<li>" + sessionLinkify("gallery.py","Gallery") + "</li>"
            htmlStr += "<li>" + sessionLinkify("profiles.py","My Profile") + "</li>"
            htmlStr += "<li>" + sessionLinkify("logout.py","Logout") + "</li>"
            htmlStr += "\t\t</ul>"
            htmlStr += """
                    </div><!-- /.navbar-collapse -->
                </div><!-- /.container-fluid -->
            </div>
            """

            #header
            htmlStr += '<div style="background:black; font-family:\'Verdana\'; font-weight:bold; color:white; !important" class="jumbotron"><h1>' + fsd['uname'] + "'s Profile</h1></div><br>"

            # PROFILE PICTURE
            if 'profilePic' in fsd:
                try:
                    writePic(fsd['profilePic'])
                except:
                    htmlStr += "Change failed!\n"

            htmlStr += getPic(fsd['uname'])

            htmlStr += tagify("<h3>","User:")
            htmlStr += tagify("<p>",fsd['uname']) + "<br>\n"

            # TAGS
            htmlStr += "<br><h3>Tags:</h3> "
            profTags = getTags(fsd['uname'])
            if profTags == []:
                htmlStr += "<br>No tags found.<br><br>"
            else:
                pos = 0
                while pos < len(profTags):
                    profTags[pos] = profTags[pos].replace("~~",",")
                    pos += 1
                tagList = ""
                usedTags = []
                for tag in profTags:
                    if tag not in usedTags:
                        tagList += tag + ", "
                        usedTags.append(tag)
                htmlStr += "<p>" + tagList + "</p>"
                htmlStr += "<br><br>"

            if 'description' in fsd:
                try:
                    writeDescription(fsd['description'])
                except:
                    htmlStr += "Update failed!\n"

            htmlStr += tagify("<h3>","Profile Description:") + "<br>\n" + tagify("<p>",getDescription(fsd['uname'])) + "\n"

            # UPDATE FORM
            htmlStr += profDescription()
            htmlStr += profImg()
            htmlStr += webpage()

        else: # display other person's page

            # links to other pages
            htmlStr += """
            <div class="navbar navbar-default">
                <div class="container-fluid">
                <!-- Brand and toggle get grouped for better mobile display -->

                    <!-- Collect the nav links, forms, and other content for toggling -->
                    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            """
            htmlStr += "\t\t<ul class='nav navbar-nav nav-justified'>\n"
            htmlStr += "<li>" + sessionLinkify("profiles.py","Return") + "</li>"
            htmlStr += "<li>" + sessionLinkify("logout.py","Logout") + "</li>"
            htmlStr += "\t\t</ul>"
            htmlStr += """
                    </div><!-- /.navbar-collapse -->
                </div><!-- /.container-fluid -->
            </div>
            """

            #header
            htmlStr += '<div style="background:black; font-family:\'Verdana\'; font-weight:bold; color:white; !important" class="jumbotron"><h1>' + fsd['friend'] + "'s Profile</h1></div><br>"

            htmlStr += "<span class='user'>User: " + fsd['friend'] + "</span><br>\n"

            # PROFILE PICTURE
            htmlStr += getPic(fsd['friend'])

            # TAGS
            htmlStr += "<br><h3>Tags:</h3> "
            profTags = getTags(fsd['friend'])
            if profTags == []:
                htmlStr += "<br>No tags found.<br><br>"
            else:
                pos = 0
                while pos < len(profTags):
                    profTags[pos] = profTags[pos].replace("~~",",")
                    pos += 1
                tagList = ""
                usedTags = []
                for tag in profTags:
                    if tag not in usedTags:
                        tagList += tag + ","
                        usedTags.append(tag)
                htmlStr += tagify("<p>",tagList) + "<br><br>"
            htmlStr += tagify("<p>","Profile Description:") + "<br>\n" + tagify("<p>",getDescription(fsd['friend'])) + "\n"
            htmlStr += webpage()

    else:
        #if user not logged in
        htmlStr += "<br>Logged in you are not. Click "
        htmlStr += '<a href="'+ loginPage + '">'
        htmlStr += "here</a> to remedy."
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

htmlStr += "</body></html>"


print htmlStr
