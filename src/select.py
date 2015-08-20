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
upload="upload.py"
profile="profiles.py"
gallery="gallery.py"
display="display.py"

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


#=============== FORM GENERATION ===================

#generate the html for an option in a select form with a given value and text
def checkGen(name,value,text):
    return '<input type="checkbox" name="' + name + '" value="' + value.replace("~~", ",") + '">' + text.replace("~~", ",") + "<br>"


#generates a series of <option>s for the tag form
#includes all the different tags a user has, with no repeats
def genTagForm(username):
    file = open('../site_data/userTags.csv','r')
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

htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title> Create Display </title>"
htmlStr += """
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

        <!-- Custom stylesheets -->
        <link rel="stylesheet" type="text/css" href="../css/select.css">
        <link rel="stylesheet" type="text/css" href="../css/navbar.css">

        <!-- Latest compiled and minified JavaScript -->
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>

        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
"""
htmlStr += "<body>"

# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~

if not valid():
    htmlStr += "Session string problem?"
else:
    validated = authSession()
    if validated:

        #session
        session = "<input type='hidden' name='uname' value='" + fsd['uname'] + "' readonly='readonly'>"
        session += "<input type='hidden' name='usecret' value='" + fsd['usecret'] + "' readonly='readonly'>"
        session += "<input type='hidden' name='uip' value='" + fsd['uip'] + "' readonly='readonly'>"

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

        #header
        htmlStr += '<div class="jumbotron">'
        htmlStr += "<h1> Create Display </h1></div>"

        #form
        htmlStr += "<div class='select-form'>"
        htmlStr += "<form type='input' method='GET' action='" + display + "'/>"

        #choose a tag to show
        htmlStr += "<b>From which tags would you like to display content?<br> \
                    If there are no checkboxes below, you haven't added any entries.</b><br><br>"
        htmlStr += genTagForm(fsd['uname']) + "<br>"

        #show captions?
        htmlStr += "<b>Do you want to show picture captions?<br>"
        htmlStr += "Captions will appear if you hover over the images regardless, <br>"
        htmlStr += "but choosing to show caps will make them appear as text.</b><br>"
        htmlStr += "<input type='checkbox' name='showcap'>Show captions<br><br>"

        #most used tag
        htmlStr += "<b>Do you want to see the most popular tag?</b><br>"
        htmlStr += "<input type='checkbox' name='freqTag'>Show most popular tag<br><br>"

        #header color
        htmlStr += "<div class='form-group'>"
        htmlStr += "<div class='color-container'>"
        htmlStr += "<b>What color do you fancy today? (Please enter a hexadecimal representation)</b>"
        htmlStr += "<input class='form-control color-class' type='text' name='color'> <br>"
        htmlStr += "</div>"
        htmlStr += "</div>"

        #submit button
        htmlStr += session
        htmlStr += '<input class="btn btn-success" type="submit" value="Display"><br><br>'
        htmlStr += "</form>"
        htmlStr += "</div>"

    else:
        #if user not logged in
        htmlStr += "<br>Logged in you are not. Click "
        htmlStr += '<a href="'+ loginPage + '">'
        htmlStr += "here</a> to remedy."
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

htmlStr += "</body></html>"


print htmlStr
