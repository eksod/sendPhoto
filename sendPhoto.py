# -*- coding: utf-8 -*-
__author__ = 'Eduardo Simioni <eduardo.simioni@gmail.com>'

import android
from xml.dom.minidom import parse, parseString

fileXML = "/sdcard/sendPhoto.xml" 
xmlData = parse(fileXML)
droid = android.Android()

# turn on GPS while photo is taken
droid.startLocating()

for node in xmlData.getElementsByTagName('picturePath'):
  picturePath = node.toxml().replace('<picturePath>','').replace('</picturePath>','')

# takes picture
# picturePath must be in this format: "/directory/file"
droid.cameraInteractiveCapturePicture(picturePath)

deviceLocation = droid.getLastKnownLocation().result
if deviceLocation['gps']:
  latitude = deviceLocation['gps']['latitude']
  longitude = deviceLocation['gps']['longitude']
  accuracy = deviceLocation['gps']['accuracy']
else:
  latitude = deviceLocation['network']['latitude']
  longitude = deviceLocation['network']['longitude']
  accuracy = deviceLocation['network']['accuracy']

# if GPS got something great, otherwise let's move on
droid.stopLocating()

# reads data from xml for sendEmail()
emailAddress = ""
for node in xmlData.getElementsByTagName('email'):  # visit every node <email />
  emailAddress += node.toxml().replace('<email>','').replace('</email>','') + "; "

emailSubject = ""
for node in xmlData.getElementsByTagName('subject'):
  emailSubject += node.toxml().replace('<subject>','').replace('</subject>','')

emailMessage = ""
for node in xmlData.getElementsByTagName('message'):
  emailMessage += node.toxml().replace('<message>','').replace('</message>','') + "\n"

emailMessage += "\n\nThe device is currently at:\n"

for node in xmlData.getElementsByTagName('mapURL'):
  emailMessage += node.toxml().replace('<mapURL>','').replace('</mapURL>','')

emailMessage += str(latitude) + ",+" + str(longitude)

emailMessage += "\n\nLocation provided by "
if deviceLocation['gps']:
  emailMessage += deviceLocation['gps']['provider'] + ", "
else:
  emailMessage += deviceLocation['network']['provider'] + ", "
emailMessage += "with an accuracy of " + str(accuracy) + " meters."

# sendEmail() attach needs to be in this format: "file:///directory/file"
sendEmailPath = "file://" + picturePath
droid.sendEmail(emailAddress, emailSubject, emailMessage, sendEmailPath)

droid.exit()