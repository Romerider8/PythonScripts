'''
* Author: Nate Schreiner 12/2017
*
*   Scrapes page at given URL for certain tags.
*   Writes to two files in local directory
*   Reads in files to an array, sorts both arrays
*   then compares arrays for differences.  If differences
*   are found we send email to given ' toaddr '.   
*
'''

fromaddr = 'millionaire.trader8@gmail.com'
toaddr = ['nschrein@nmu.edu', 'nateschreiner6@gmail.com']
fromPass = ""

#pip install requests
import requests
from filecmp import cmp
#pip install bs4
from bs4 import BeautifulSoup
import smtplib
from sys import exit
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def formatEvent(eventSoupTag):
    return eventSoupTag.text+' : https://www.islandresortandcasino.com'+eventSoupTag.a['href']+'\n'

def emailError():
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = 'Error Raised in Python scraper script'
    body = 'There has been an error checking the HTML tag on the website!\n\n'
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, fromPass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit

def emailNew(theEvents):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    #msg['To'] = toaddr
    msg['To'] = ", ".join(toaddr)
    msg['Subject'] = 'New Event(s) Added - Island Resort and Casino'
    body = 'These event(s) have been added!\n\n'
    for i in reversed(theEvents):
        body = body+i
    body = body +"\nView them all here \n https://www.islandresortandcasino.com/entertainment/island-showroom"
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, fromPass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit

scapePath = 'https://www.islandresortandcasino.com/entertainment/island-showroom'
r = requests.get(scapePath)

#parse html and find events
soup = BeautifulSoup(r.text,'html.parser')
events = soup.findAll('h2', attrs={'class':'underline'})
if(len(events) == 0):
    emailError()
    exit()

#formated from soupTag to string "title : link"
formatedEvents = []
for i in events:
    #i are the website's Events Titles
    formatedEvents.append(formatEvent(i))


unreadEvents = []
with open('secondEvent.txt', 'w+') as rf:
    rf.truncate()
    for i in reversed(formatedEvents):
        rf.write(i)

check_file = open('checkFile.txt', 'r')
for line in check_file:
    unreadEvents.append(line)

check_file.close()
formatedEvents.sort()
unreadEvents.sort()
debugList = [x for x in formatedEvents if x not in unreadEvents]
with open('debugFile.txt', 'w+') as debug:
    for item in debugList:
        debug.write(item)

if(formatedEvents == unreadEvents):
    print("no new events")
else:
    check_file = open('checkFile.txt', 'w+')
    check_file.truncate()
    for i in reversed(formatedEvents):
        check_file.write(i)
    emailNew(formatedEvents)
