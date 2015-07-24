#!/usr/bin/python
# ========= HASHBANG LINE ABOVE IS MAGIC! =========
# ========= (Must be first line of file.) =========

#===================== IMPORT =======================
# modules help verify if link is valid image
import imghdr # checks for proper image
import httplib # makes an HTTP connection to the URL
import cStringIO # reads strings from and writes strings to output

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
upload="upload.py"
gallery = "gallery.py"
select="select.py"

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

#create hidden inputs containing this user's session string to be submitted with the forms
def sessionForm():
    session = "<input type='hidden' name='uname' value='" + fsd['uname'] + "' readonly='readonly'>"
    session += "<input type='hidden' name='usecret' value='" + fsd['usecret'] + "' readonly='readonly'>"
    session += "<input type='hidden' name='uip' value='" + fsd['uip'] + "' readonly='readonly'>"
    return session

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GET LIST OF USERS FROM CSV FILES
def getUsers(username):
    userL = []

    file = open('../site_data/userProfiles.csv', 'r')
    lines = file.readlines()
    file.close()

    pos = 0
    while pos < len(lines):
        lines[pos] = lines[pos][:-1]
        if lines[pos].split(',')[0] != username:
            userL.append(lines[pos].split(",")[0])
            break
        pos += 1

    # generates a dropdown menu containing a list of users
    s = "<div class='dropdown_container'>"
    s += "<select class='form-control dropdown_class' id='dropdown_id' name='friend'>\n"

    for user in userL:
        s += "\t<option value='" + user + "'>" + user + "</option>\n"

    s += "</select>\n</div>\n<br>"

    return s

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GET AND WRITE PROFILE PIC PREFERENCES TO CSV FILES
def getPic(username):
    image = ""

    file = open('../site_data/userProfiles.csv', 'r')
    lines = file.readlines()
    file.close()

    pos = 0
    while pos < len(lines):
        lines[pos] = lines[pos][:-1]
        if lines[pos].split(',')[0] == username:
            image = lines[pos].split(',')[2]
            break
        pos += 1

    return "\t<img class='square' src='" + image.replace("~~",",") + "' />\t<br>\n"

def writePic(img):
    try:
        if img.startswith("https://"): #removes https:// from link due to imgs not appearing
            img = img[8:]
        if not img.startswith("http://"): #adds https:// to ensure img appears
            img = "http://" + img

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

#check if the img URL is valid
def validURL():
    url = fsd['profilePic']

    #remove the http:// prefix to the url
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]

    #split url into domain name and path
    if url.find("/") != -1:
        url = url.split("/", 1)
        main = url[0]
        path = url[1]
    else:
        main = url
        path = ""

    try:
        #make connection
        conn = httplib.HTTPConnection(main, timeout=60)
        conn.request('GET', '/' + path)

        #get response
        resp = conn.getresponse()

        #check image file type
        image_file_obj = cStringIO.StringIO(resp.read())
        image_type = imghdr.what(image_file_obj)
        if image_type is not None:
            return True
        else:
            return False
    except:
        return "error"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GET TAGS FROM CSV FILES
def getTags(username):
    L = []

    file = open('../site_data/userTags.csv', 'r')
    lines = file.readlines()
    file.close()

    pos = 0
    while pos < len(lines):
        lines[pos] = lines[pos][:-1]
        if lines[pos].split(",")[0] == username:
            L.extend(lines[pos].split(",")[1:])
            break
        pos += 1

    return L

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GET AND WRITE DESCRIPTIONS TO CSV FILES
def getDescription(username):
    desc = ""

    file = open('../site_data/userProfiles.csv', 'r')
    lines = file.readlines()
    file.close()

    # removes newlines
    pos = 0
    while pos < len(lines):
        lines[pos] = lines[pos][:-1]
        if lines[pos].split(",")[0] == username:
             desc = lines[pos].split(",")[1].replace("~~",",").replace("@@","<br>")
             break
        pos += 1

    return desc

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
# HTML GENERATOR FUNCTIONS
def profDescription():
    html = "<form name='desc' type='input' method='GET' action='profiles.py'>"
    html += "<div class='form-group'>"
    html += "<br><label for='description'>Update your description.</label><br>"
    html += "<textarea class='form-control col-md-offset-3 textarea' rows='5' name='description' placeholder='I am awesome!'></textarea><br>"
    html += sessionForm()
    html += "<input class='btn btn-success' type='submit' value='Submit'>"
    html += "</div>"
    html += "</form><br>"

    return html

def profImg():
    html = "<br><br>Change your profile picture by adding a URL!<br>"
    html += "<form name='profimg' type='input' method='GET' action='profiles.py'>"
    html += "<input class='form-control col-md-offset-4 prof-img' type='text' name='profilePic'><br>"
    html += sessionForm()
    html += "If your profile picture does not change, you may have entered in an invalid URL. <br>See "
    html += "<a href='https://docs.python.org/2/library/imghdr.html'>here</a>"
    html += " for acceptable image formats.<br>"
    html += "Please make sure that the URL you provide contains only the image, like "
    html += "<a href='http://www.quicksprout.com/images/foggygoldengatebridge.jpg'>this</a>.<br><br>"
    html += "<input class='btn btn-success' type='submit' value='Submit'>"
    html += "</form><br><br>"

    return html

def profile(user):
    html = "<div class='profile-content'>"
    # Profile image
    html += getPic(user)
    if 'friend' not in fsd:
        html += profImg()
    #Profile description
    html += tagify("<p>","Profile Description:") + tagify("<h3>",getDescription(user)) + "\n"
    if 'friend' not in fsd:
        html += profDescription()
    # User Tags
    html += displayTags(user)
    # View Friend
    html += viewFriend()
    html += "</div>"

    return html

def viewFriend():
    html = "<br><br>View other peoples' webpages.<br>"
    html += "<form name='webpage' type='input' method='GET' action='profiles.py'>"
    html += getUsers(fsd['uname'])
    html += sessionForm()
    html += "<input class='btn btn-success' type='submit' value='Submit'>"
    html += "</form><br><br>"

    return html

def displayTags(user):
    html = "<br><p>Tags:</p>"
    profTags = getTags(user)

    if profTags == []:
        html += "<h3>No tags found.</h3><br>"
    else:
        pos = 0
        while pos < len(profTags):
            profTags[pos] = profTags[pos].replace("~~",",")
            pos += 1
        profTags = set(profTags)
        html += "<p>" + ", ".join(profTags) + "</p>"

    return html

#----------------------------------------------
# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========

htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title>Profile</title>"
htmlStr += """
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

        <!-- Custom stylesheets -->
        <link rel="stylesheet" type="text/css" href="../css/profiles.css">
        <link rel="stylesheet" type="text/css" href="../css/navbar.css">

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
            htmlStr += "<li>" + sessionLinkify("upload.py","Add Images") + "</li>"
            htmlStr += "<li>" + sessionLinkify("select.py","Create Display") + "</li>"
            htmlStr += "<li>" + sessionLinkify("gallery.py","Gallery") + "</li>"
            htmlStr += "<li>" + sessionLinkify("profiles.py","My Profile") + "</li>"
            htmlStr += "<li>" + sessionLinkify("logout.py","Logout") + "</li>"
            htmlStr += "\t\t</ul>"
            htmlStr += """
                    </div><!-- /.navbar-collapse -->
                </div><!-- /.container-fluid -->
            </div>
            """
            htmlStr += '<div class="jumbotron"><h1>' + fsd['uname'] + "'s Profile</h1></div>"

            # UPDATE PROFILE
            if 'profilePic' in fsd:
                imgFound = validURL()
                if imgFound == True:
                    try:
                        writePic(fsd['profilePic'])
                    except:
                        htmlStr += "Change failed!\n"
                else:
                    htmlStr += str(imgFound)

            if 'description' in fsd:
                try:
                    writeDescription(fsd['description'])
                except:
                    htmlStr += "Change failed!\n"

            htmlStr += profile(fsd['uname'])

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
            htmlStr += '<div class="jumbotron"><h1>' + fsd['friend'] + "'s Profile</h1></div>"

            htmlStr += profile(fsd['friend'])

    else:
        #if user not logged in
        htmlStr += "<br>Logged in you are not. Click "
        htmlStr += '<a href="'+ loginPage + '">'
        htmlStr += "here</a> to remedy."
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

htmlStr += "</body></html>"


print htmlStr
