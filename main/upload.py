#!/usr/bin/python
# ========= HASHBANG LINE ABOVE IS MAGIC! =========
# ========= (Must be first line of file.) =========

# ================= IMPORTS ====================
import os
import cgi
import cgitb
#cgitb.enable()  #diag info --- comment out once full functionality achieved

#import cgiDeal from another folder
import sys

sys.path.insert(0, '../cgiToDict/')
import cgiDeal



# ~~~~~~~~~~~~~~~ auxiliary files ~~~~~~~~~~~~~~~~~
#file to store users and their passwords:
userfile="../site_data/users.csv"

#file to store users currently logged in:
currentUsersFile="../site_data/usersOnline.csv"

#page to link to upon successful login:
upload="upload.py"
profile="profiles.py"
gallery="gallery.py"
display="display.py"
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



#-----------------CSV DEALING-------------------


#deal with commas in user input by replacing them with '~~'
#this can be undone later when the item is pulled up later
def commaDeal(item):
    if item.find(",") != -1:
        return item.replace(",", "~~")
    else:
        return item


#wrote to the csv files
def addEntry(item, isImg, isTag, isCap):
    username = fsd['uname']

    item = commaDeal(item) # HANDLES COMMAS IN USER INPUT

    if isTag:
        file = open('../site_data/userTags.csv', 'r')
        read = file.readlines()
        file.close()

        passed = False #have you passed the entry for this user?
        pre = "" #csv content pre-user
        entry = "" #csv user content
        post = "" #csv content post-user

        for i in read:
            if i.split(',')[0] == username or i.split(',')[0] == username + "\n":
                passed = True
                entry = i[:-1] + "," + item + "\n"
            elif passed:
                post += i
            elif not passed:
                pre += i
        file = open('../site_data/userTags.csv', 'w')
        file.write(pre + entry + post)
        file.close()

    # --------------------------------------

    elif isImg:
        file = open('../site_data/userImgs.csv', 'r')
        read = file.readlines()
        file.close()

        passed = False #have you passed the entry for this user?
        pre = "" #csv content pre-user
        entry = "" #csv user content
        post = "" #csv content post-user

        for i in read:
            if i.split(',')[0] == username or i.split(',')[0] == username + "\n":
                passed = True
                entry = i[:-1] + "," + item + "\n"
            elif passed:
                post += i
            elif not passed:
                pre += i
        file = open('../site_data/userImgs.csv', 'w')
        file.write(pre + entry + post)
        file.close()

    # --------------------------------------

    else:
        file = open('../site_data/userCaps.csv', 'r')
        read = file.readlines()
        file.close()

        passed = False #have you passed the entry for this user?
        pre = "" #csv content pre-user
        entry = "" #csv user content
        post = "" #csv content post-user

        for i in read:
            if i.split(',')[0] == username or i.split(',')[0] == username + "\n":
                passed = True
                entry = i[:-1] + "," + item + "\n"
            elif passed:
                post += i
            elif not passed:
                pre += i
        file = open('../site_data/userCaps.csv', 'w')
        file.write(pre + entry + post)
        file.close()


#write to the CSV file
def writeCSV():
    if formFilled():
        try:
            addEntry(fsd['tag'], False, True, False)
            if 'caption' not in fsd:
                addEntry(' ',False,False,True)
            else:
                addEntry(fsd['caption'], False, False, True)
            addEntry(fsd['img'], True, False, False)
            return True
        except:
            return False
    else:
        return False


#is form filled correctly?
def formFilled():
    if 'tag' not in fsd or 'img' not in fsd:
        return False
    else:
        return True


# ========= CONTENT-TYPE LINE REQUIRED. ===========
# ======= Must be beginning of HTML string ========
htmlStr = "Content-Type: text/html\n\n" #NOTE there are 2 '\n's !!!
htmlStr += "<html><head><title> Upload </title>"

# GETS THE CSS FILES FOR STYLING
htmlStr += """
        <!-- Bootstrap stylesheets must come before custom stylesheets! -->

        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

        <!-- Latest compiled and minified JavaScript -->
        <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>

        <link rel="stylesheet" type="text/css" href="../css/navbar.css">
        <link rel="stylesheet" type="text/css" href="../css/upload.css">
    </head>
"""
htmlStr += "<body style='text-align:center; background:url(\"bg-imgs/art.jpg\"); background-size:cover;'>"

# ~~~~~~~~~~~~~ HTML-generating code ~~~~~~~~~~~~~~

if not valid():
    htmlStr += "session string problem?"
else:
    validated = authSession()

    if validated:
        # hide session strings in hidden input fields
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
        htmlStr += "<h1>Add Images</h1></div>"

        # BEGINNING OF FORM - input fields for user to input imgs, img captions, and img tags
        htmlStr += "<div class='img-form'>"
        htmlStr += '<form class="form-horizontal" type="input" method="GET" action="upload.py">'
        htmlStr += session

        htmlStr += """
                    <div class="form-group">
                        <p class="col-sm-5 control-label">Image URL: </b></p>
                        <div class="col-sm-2"> <input class="form-control" type="text" style="width:110%;" name='img'> </div>
                    </div> <br>
                    <div class="form-group">
                        <p class="col-sm-5 control-label">Caption: </p>
                        <div class="col-sm-2"> <input class="form-control" type="text" style="width:110%;" name='caption'> </div>
                    </div> <br>
                    <div class="form-group">
                        <p class="col-sm-5 control-label">Tag: </p>
                        <div class="col-sm-2"> <input class="form-control" type="text" style="width:110%;" name='tag'> </div>
                    </div> <br><br>
                    <input class="btn btn-success" type="submit" value="Submit"> <br> <br>
                </form>
        """

        # instructions
        htmlStr += "<p>Please fill out the three boxes of the form above with a valid image URL<br>(you can right click on an image and select the option \
            to copy its URL),<br>a caption that will be displayed if the image fails, and a tag to organize your images. Captions are optional.</p><br>"

        # writes to CSVs and returns True if successful
        if writeCSV():
            htmlStr += "<p>Your input has been saved!<br>You may enter another entry.</p><br>"
        else:
            htmlStr += "<p>You did not fill the URL box and the tag. Do that now!</p><br>"

        htmlStr += "</div>"

    else:
        htmlStr += "<br>Logged in you are not. Click "
        htmlStr += '<a href="'+ loginPage + '">'
        htmlStr += "here</a> to remedy."
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

htmlStr += "</body></html>"


print htmlStr
