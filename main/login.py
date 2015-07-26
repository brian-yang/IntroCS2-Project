#!/usr/bin/python
# ========= HASHBANG LINE ABOVE IS MAGIC! =========
# ========= (Must be first line of file.) =========

# =================== IMPORTS ========================
import hashlib
import os
import random
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
#file to store users and their passwords:
userfile="../site_data/users.csv"

#file to store users currently logged in:
currentUsersFile="../site_data/usersOnline.csv"

#query string dictionary using CGI
fsd=cgiDeal.FStoD()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#validate user input
def valid():
    if not ('uname' in fsd) or not ('upass' in fsd):
        return False
    if fsd['uname'] == '':
        return False
    if fsd['upass'] == '':
        return False
    return True


#check for existence of a user in CSV file
def userExists(u):
    try:
        userlist = open(userfile,'r').readlines()
    except:
        return False
    for row in userlist:
        if row.strip().split(',')[0]==u:
            return True
    return False


#return True if a matching u/p combo exists in user file, False otherwise
def authenticate(u,p):
    try:
        userlist = open(userfile,'r').readlines()
    except:
        return False
    if not userExists(u):
        return False
    for row in userlist:
        if row.strip().split(',')[0]==u:
            if row.strip().split(',')[1]==hashlib.md5(p).hexdigest():
                return True
    return False


#write an entry to logged-in-users file
#returns True if success, False otherwise
def addToLoggedIn(u,uKey,uIP):
    remFrLoggedIn(u) #close any open sessions
    outTxt = u + ',' + uKey + ',' + uIP + '\n'
    try:
        outStream=open(currentUsersFile, 'a')
        outStream.write(outTxt)
        outStream.close()
    except:
        return False
    return True


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

        <!-- Custom stylesheets -->
        <link rel="stylesheet" type="text/css" href="../css/login.css">

        <!-- Latest compiled and minified JavaScript -->
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
    </head>
"""
htmlStr += "<body>"
# needs to have http link to image

# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~
if not valid():
    htmlStr += "Invalid input"
else:
    validated = authenticate( fsd['uname'], fsd['upass'] )
    ################################
    #diag HTML...
    #htmlStr += "<h4>Dictionary of form data:</h4>"
    #htmlStr += str( fsd )
    #htmlStr += "<br><br>"
    #htmlStr += "<br><br>" + "username entered: " + str( fsd['uname'] )
    #htmlStr += "<br>" + "password entered: " + str( fsd['upass'] )
    #htmlStr += "<br>user exists? --> " + str( userExists( fsd['uname'] ) )
    #htmlStr += "<br>pass matches?  "
    #htmlStr += str(validated)
    ################################
    if validated:
        #gen 9-digit number for this user for this session
        secretNum = str( random.randrange(100000000,1000000000) )

        #record visitor's IP address
        if "REMOTE_ADDR" in os.environ:
            userIP = os.environ["REMOTE_ADDR"]
        else:
            userIP = "999.999.999.999"

        #write user record to logged-in-users file
        addToLoggedIn( fsd['uname'], secretNum, userIP )

        #SITE MAP
        htmlStr += "<div class='wrap'>"

        #Successful login message
        htmlStr += "<h3>You've logged in.</h3><br>"
        htmlStr += "<p>Pick what you'd like to do next.</p>"

        #build link w querystring (username+"secret"num+IP)
        #UPLOAD IMAGES LINK
        htmlStr += '<a class="btn btn-success" href=\"' + "upload.py"
        htmlStr += "?uname=" + fsd['uname']
        htmlStr += "&usecret=" + secretNum
        htmlStr += "&uip=" + userIP + "\""
        htmlStr += ">Add Images</a><br><br>"

        #build link w querystring (username+"secret"num+IP)
        #CREATE DISPLAY LINK
        htmlStr += '<a class="btn btn-success" href=\"' + "select.py"
        htmlStr += "?uname=" + fsd['uname']
        htmlStr += "&usecret=" + secretNum
        htmlStr += "&uip=" + userIP + "\""
        htmlStr += ">Create Display</a><br><br>"

        #build link w querystring (username+"secret"num+IP)
        #GALLERY LINK
        htmlStr += '<a class="btn btn-success" href=\"' + "gallery.py"
        htmlStr += "?uname=" + fsd['uname']
        htmlStr += "&usecret=" + secretNum
        htmlStr += "&uip=" + userIP + "\""
        htmlStr += ">View Gallery</a><br><br>"

        #build link w querystring (username+"secret"num+IP)
        #PROFILE LINK
        htmlStr += '<a class="btn btn-success" href=\"' + "profiles.py"
        htmlStr += "?uname=" + fsd['uname']
        htmlStr += "&usecret=" + secretNum
        htmlStr += "&uip=" + userIP + "\""
        htmlStr += ">My Profile</a><br><br><br>"

        #HELP
        htmlStr += "<h4>Confused?</h4>"
        htmlStr += "<p><b>Add Images:</b> Save images on our site by providing us with URL links to your images!</p>"
        htmlStr += "<p><b>Create Display:</b> Select images from the ones you've uploaded to create your very own image exhibition!.</p>"
        htmlStr += "<p><b>View Gallery:</b> View some of the images that others on our site have uploaded. You may even see some of your images as well!</p>"
        htmlStr += "<p><b>My Profile:</b> Add an image of yourself and a description so others can know who you are.</p>"

        #LOGOUT
        htmlStr += '<a class="btn btn-success" href=\"' + "logout.py"
        htmlStr += "?uname=" + fsd['uname']
        htmlStr += "&usecret=" + secretNum
        htmlStr += "&uip=" + userIP + "\""
        htmlStr += ">Logout</a><br><br><br>"

        htmlStr += "</div>"


    else:
        htmlStr += "<p>Username and password don't match. Go back.</p>"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


htmlStr += "</body></html>"


print htmlStr
