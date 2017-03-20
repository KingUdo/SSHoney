#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Import GeoIP
from geoip import geolite2
import sqlite3
import datetime

#connect to Database:
connection = sqlite3.connect("/home/lars/ServerStuff/SSHoney/pw_us_drop.db")
cursor = connection.cursor()

#total Number:
cursor.execute("SELECT us FROM log")
TNumber = len(cursor.fetchall())

#number of Users:
cursor.execute("SELECT us FROM log GROUP BY us")
USNumber = len(cursor.fetchall())

#number of Passwords
cursor.execute("SELECT pw FROM log GROUP BY pw")
PWNumber = len(cursor.fetchall())

#Find IPs:
cursor.execute("SELECT ip FROM log GROUP BY ip")
IPNumber = len(cursor.fetchall())


#Extract all IPs
IPList = []
cursor.execute("SELECT ip FROM log GROUP BY ip")
for r in cursor.fetchall():
        IPList.append(r[0])


#Find top 10 User
USList = []
USNList = []
cursor.execute("SELECT us, count(us) as freq FROM log GROUP BY us ORDER BY freq DESC LIMIT 10")
for r in cursor.fetchall():
	USList.append(r[0])
	USNList.append(r[1])

#Find top 10 PassWD
PWList = []
PWNList = []
cursor.execute("SELECT pw, count(pw) as freq FROM log GROUP BY pw ORDER BY freq DESC LIMIT 10")
for r in cursor.fetchall():
       	PWList.append(r[0])
	PWNList.append(r[1])

#match IP's with coordinates:
LOCList = []

for i in IPList:
	match = geolite2.lookup(i)
	try:
		LOCList.append(match.location)
	except:
		print("No Match")


#create HTML:
file = open("/var/www/html/Projects/Web/SSHoney/index.html","w") 
file.write("<!DOCTYPE html><html><head><link type='text/css' rel='stylesheet' href='/css/style.css'/><link href='https://fonts.googleapis.com/css?family=Source+Code+Pro' rel='stylesheet'><style type='text/css'>#map {width: 700px ;height: 400px ;position: relative;max-width: 600px;max-heigh: 200px;}</style><script type='text/javascript' src='https://maps.googleapis.com/maps/api/js?key=AIzaSyDYwgxDPrbzfw2UxAGNu1Qar7Fz4XynHT8'></script><script type='text/javascript'>google.maps.event.addDomListener(window, 'load', init);function init() {var mapOptions = {zoom: 1,center: new google.maps.LatLng(0,0),styles: [{'featureType':'all','elementType':'labels.text.fill','stylers':[{'color':'#ffffff'}]},{'featureType':'all','elementType':'labels.text.stroke','stylers':[{'color':'#000000'},{'lightness':13}]},{'featureType':'administrative','elementType':'geometry.fill','stylers':[{'color':'#000000'}]},{'featureType':'administrative','elementType':'geometry.stroke','stylers':[{'color':'#144b53'},{'lightness':14},{'weight':1.4}]},{'featureType':'landscape','elementType':'all','stylers':[{'color':'#08304b'}]},{'featureType':'poi','elementType':'geometry','stylers':[{'color':'#0c4152'},{'lightness':5}]},{'featureType':'road.highway','elementType':'geometry.fill','stylers':[{'color':'#000000'}]},{'featureType':'road.highway','elementType':'geometry.stroke','stylers':[{'color':'#0b434f'},{'lightness':25}]},{'featureType':'road.arterial','elementType':'geometry.fill','stylers':[{'color':'#000000'}]},{'featureType':'road.arterial','elementType':'geometry.stroke','stylers':[{'color':'#0b3d51'},{'lightness':16}]},{'featureType':'road.local','elementType':'geometry','stylers':[{'color':'#000000'}]},{'featureType':'transit','elementType':'all','stylers':[{'color':'#146474'}]},{'featureType':'water','elementType':'all','stylers':[{'color':'#021019'}]}]};var mapElement = document.getElementById('map');var map = new google.maps.Map(mapElement, mapOptions);") 

for LOC in LOCList:
	file.write("var marker = new google.maps.Marker({position: new google.maps.LatLng" + str(LOC) +",map: map,});")

file.write("}</script></head><body><ul><li><a href='/index.html'>Home</a></li><li><a href='/Projects/Projects.html'>Projects</a></li><li><a href='/Intern/Intern.html'>Intern</a></li><li><a href='/Contact/Contact.html'>Contakt</a></li></ul><div class='main'><p class='medium'>SSH password fisher</p><br><p class='medium2'>Statistic:</p><p class='text'>Users: ")
file.write(str(USNumber))
file.write("<br/>Passwords: ")
file.write(str(PWNumber))
file.write("<br/>IPs: ")
file.write(str(len(IPList)))
file.write("<br/>Total: ")
file.write(str(TNumber))

file.write("<br/><br/>Refresh Time: ")
file.write(str(datetime.datetime.utcnow()))


file.write("</p><p class='medium2'>Map:</p><div id='map'></div><p class='medium2'>Top10-List:</p><div class='left'><p class='text'><b>Password:</b> <br/>")
for psw in PWList:
	file.write(str(psw) + "<br/>")
file.write("<br/><a href='pw.txt'>DOWNLOAD</a> <br/>")

file.write("</p></div><div class='right'><p class='text'><b>Username:</b> <br/>")
for usr in USList:
        file.write(str(usr) + "<br/>")
file.write("<br/><a href='us.txt'>DOWNLOAD</a> <br/>")

file.write("</p></div></div></body></html>")


##CREATE PW und US List

pw = open("/var/www/html/Projects/Web/SSHoney/pw.txt", "w")

cursor.execute("SELECT pw FROM log GROUP BY pw")
for pwall in cursor.fetchall():
	pw.write(str(pwall[0]) + " \n")

us = open("/var/www/html/Projects/Web/SSHoney/us.txt", "w")

cursor.execute("SELECT us FROM log GROUP BY us")
for usall in cursor.fetchall():
        us.write(str(usall[0]) + " \n")


connection.commit()
connection.close()

