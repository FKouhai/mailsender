#!/usr/bin/python3
#
#Inspired by sshalert https://github.com/groovemonkey/sshalert

# The mail sender script was made by FKouhai
# This script reads the sudo.log and sends an email everytime it gets a new line

#Importing the needed packages
import os,time
import smtplib, ssl

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

port = 465
sender = "insertyourMailAddr"
receiver = "insertDestinationMailAddr"
#You need to export a env var or you could just hard code your email's password
pswd= os.getenv("GMAIL_PSWD")
#Creating the ssl context
context = ssl.create_default_context()

 #sendMail function made to send an email with the given args
def sendMail(last_line):

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
        server.login(sender, pswd)
        server.sendmail(sender, receiver, last_line)

#Found on stackoverflow lol creating an event handler that checks when the file is modified
class MyEventH(FileSystemEventHandler):
    def on_modified(self, event):
        print('event type: {event.event_type} path : {event.src_path}')
        with open("/var/log/sudo.log", "r") as fich:
            #Using readlines()[-1] gives you the last line of the file
            last_line = fich.readlines()[-1]
            sendMail(last_line)
        return super().on_modified(event)


if __name__ == "__main__":
    #Creating an observer that watches the /var/log directory
    event_handler = MyEventH()
    observer = Observer()
    observer.schedule(event_handler, path='/var/log', recursive=False)
    #Starting the observer
    observer.start()
    try:
        while True:

            time.sleep(1)
    except KeyboardInterrupt:
        #If clicking ctr+c or any kb interrupt it stops the observer
        observer.stop()
    observer.join()
