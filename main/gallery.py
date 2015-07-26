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
upload="upload.py"
profile="profiles.py"
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
    file = open('../site_data/userImgs.csv', 'r')
    imgs = file.readlines()
    file.close()

    imgL = []

    imgL = galleryList(imgs, imgL)

    if imgL == []:
        return "Nothing to show today. Try again when you or others have uploaded pics."
    # --------------------------------------

    file = open('../site_data/userCaps.csv', 'r')
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
        "' alt='" + capL[randNum].replace("~~",",") + "'/>\n"

    return s



# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========

htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title>Gallery</title>"
htmlStr += """
        <!-- Latest compiled and minified Bootstrap CSS -->
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

        <!-- Required Owl Carousel stylesheet -->
        <link rel="stylesheet" href="../owl-carousel/owl.carousel.css">

        <!-- Default Owl Carousel theme -->
        <link rel="stylesheet" href="../owl-carousel/owl.theme.css">

        <!-- Custom stylesheets -->
        <link rel="stylesheet" type="text/css" href="../css/gallery.css">
        <link rel="stylesheet" type="text/css" href="../css/navbar.css">

        <!-- jQuery plugin v1.11.3 -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

        <!-- Latest compiled and minified Bootstrap JavaScript -->
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>

        <!-- Owl Carousel minified JavaScript -->
        <script src="../owl-carousel/owl.carousel.min.js"></script>

        <!-- Owl Carousel initializer (calls js plugin) -->
        <script>
            $(document).ready(function() {
                $('.owl-carousel').owlCarousel({
                    autoPlay: 3000,
                    navigation: true,
                    slideSpeed: 300,
                    paginationSpeed: 400,
                    singleItem: true
                });
            });
        </script>
    </head>
"""
htmlStr += "<body>"

# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~

if not valid():
    htmlStr += "Session string problem?"
else:
    validated = authSession()
    if validated:

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
        htmlStr += '<div style="background:black; font-family:\'Verdana\'; font-weight:bold; color:white; !important" class="jumbotron"><h1>Gallery</h1><br>'
        htmlStr += "</div>"

        #gallery
        htmlStr += "<div class='gallery-content'>"
        htmlStr += "<div class='owl-carousel'>"
        htmlStr += getGallery()
        htmlStr += "</div>"
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
