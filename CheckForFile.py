'''
*   Author: Nate Schreiner: 04/2016
*
*   Check to see if file at given path has been created
*   If file exists, and is from today, send email that everything is ok
*   if file does not exist or is not from today send a warning email
*
'''


import smtplib
import datetime
import os.path
from sys import exit
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

now = datetime.datetime.now()
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

if(now.month < 10):
    month = "0" + str(now.month)
else:
    month = str(now.month)

if(now.day < 10):
    day = "0" + str(now.day)
else:
    day = str(now.day)
    
todays_date = str(now.year) + '/' + str(month) + '/' + str(day)

file_name = 'SFTP-Americollect-Results.L1'

file_path = 'C:/Documents and Settings/train2/Desktop/Americollect/'+file_name

fromaddr = 'penmedautoemail@gmail.com'
toaddr = 'PIM@penmed.com'
testaddr = 'nateschreiner6@gmail.com'


if(os.path.isfile(file_path)):
    #check to see if it's from the current day
    date = modification_date(file_path)
    new_date = date.strftime('%Y/%m/%d')
    if(new_date == todays_date):
        #email SFTP file
        print("Date modified matched today's date....About to send confirmation email")
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = testaddr
        msg['Subject'] = 'SFTP Americollect File'
        body = 'Attached is the copy of the SFTP-Americollect-Results.L1 file which WAS modified today'
        msg.attach(MIMEText(body, 'plain'))
        print('this is being attached: ' + file_path)
        attachment = open(file_path, 'rb')
        print(attachment)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment: filename= %s' % file_name)
        msg.attach(part)
        
        

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, '')
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit
    else:
        #Send warning email
        print("Date modified did not match todays date....SENDING WARNING EMAIL")
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = testaddr
        msg['Subject'] = '**WARRNING** File: SFTP-Americollect-Results.L1 DOES NOT HAVE TODAYS DATE ON IT WHICH INDICATES IT DID NOT RUN TODAY'
        body = file_path + ' This file does not exist which indicates the query failed today'
        msg.attach(MIMEText(body, 'plain'))
    
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, '9s0mt1ngE')
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit

else:
    #Send warning email
    print("FILE DID NOT EXIST OR WAS NOT FOUND...About to send warning email")
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = testaddr
    msg['Subject'] = '**WARRNING** File: SFTP-Americollect-Results.L1 DOES NOT EXIST. CHECK QUERY PC'
    body = file_path + ' This file does not exist which indicates the query failed today'
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, '9s0mt1ngE')
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit
    

