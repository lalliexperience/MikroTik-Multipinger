import email
from multiping import MultiPing
import time
import json
import sys
import os
import re
import argparse
from os.path import exists
import paramiko # https://stackoverflow.com/questions/42375396/automate-ssh-commands-with-python


# Email server and credentials for sending emails when somethig is not replying to pings
SMTPserver = 'somehost.com'         # Email SMTP Server
sender =     'user@somehost.com'    # Email From feild
USERNAME = "user@somehost.com"      # Email username
PASSWORD = "XXXXXXXX"               # Email password
subject="Sent from Python"          # Email subject

# The router where information will be collected
router = "172.16.0.1"               # Mikrotik Router address
p = 22                              # Mikrotik Router SSH port (default 22)
loginname = "admin"                 # Mikrotik username 
loginpass = "XXXXXXXX"              # Mikrotik password



emailsend = ""
content = ""
emailvalid = False
def sendemail():
    global emailvalid
    if emailvalid is False: return
    global content
    global emailsend
    if emailsend is False: return
    print("Sending email")


    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'

    from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
    # from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

    # old version
    # from email.MIMEText import MIMEText
    from email.mime.text import MIMEText

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject']=       subject
        msg['From']   = sender # some SMTP servers will do this automatically, not all

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, emailsend, msg.as_string())
        finally:
            conn.quit()

    except:
        sys.exit( "mail failed; %s" % "CUSTOM_ERROR" ) # give an error message


myDict = {}
def getreservations():
    global myDict


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #disble known host fingerprint checking USE CAUTION

    try:
        #make connection
        print("\u001b[37;1mMaking ssh connection to " + router + "\u001b[0m" )
        ssh.connect(router, port=p, username=loginname, password=loginpass, timeout=2, banner_timeout=200)

        print("Connected")

        stdin, stdout, stderr = ssh.exec_command('log warning "The Python script is getting dhcp reservation list."')

        stdin, stdout, stderr = ssh.exec_command('/ip dhcp-server export terse')

        for stdoutline in stdout.readlines():
            #print(stdoutline)
            stdoutline = stdoutline.replace('"', "")

            if "address=" and "mac-address=" and "comment=" in stdoutline:
                myDict[stdoutline.split(' ')[6].split('=')[1]] = stdoutline.split(' ')[4].split('=')[1]
                # print(stdoutline.split(' ')[4].split('=')[1])
                # print(stdoutline.split(' ')[6].split('=')[1])
        

    except Exception as e:
        if "11001" in str(e):
            print("\u001b[33;1mThe host " + router + " is not reachable\u001b[0m")
        else:
            print(e)





#validate email address
def check(email):
    global emailvalid
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        emailvalid = True
        return True
    else:
        emailvalid = False
        return False
        

print ("Run with -h for help")

parser = argparse.ArgumentParser(description="OPTIONS:",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-e", "--emailsend", help="Send email report to this address")
parser.add_argument("-r", "--reservations", help="Get a list of reservations with comments from the Mikrotik router. Enabling this disables JSON input requirement.", action='store_true')
parser.add_argument("inputfile", help="JSON File to check for IPs")
args = parser.parse_args()
config = vars(args)

# print("Received the following options:")
# print(config)

args = vars(parser.parse_args())
inputfile = args["inputfile"]
emailsend = args["emailsend"]
reservations = args["reservations"]

if emailsend:
    if check(emailsend) is False:
        quit("Invalid email address specified")

if reservations is False:
    if inputfile:
        file_exists = exists(inputfile)
        if file_exists is False:
            quit("The input file '" + inputfile + "' was not found")
        else:
            myDict = json.load(open(inputfile)) #load json as dicitonary
else:
    getreservations()

#myDict = {"101": "8.8.8.8", "102": "127.0.0.1", "103": "youtube.com", "104": "1.1.1.1", "105": "1.2.3.4"}
#json.dump(myDict, open("multiping.json",'w')) #save dictionary as json


print("Checking " + str(len(myDict)) +" addresses")
keys = list(myDict.keys())
values = list(myDict.values()) #convert the dict_values to list


try:
    # Create a MultiPing object to test three hosts / addresses
    mp = MultiPing(values)
except Exception as e:
    print("There was an error:")
    print(str(e))
    quit()


# Send the pings to those addresses
mp.send()

# With a 1 second timout, wait for responses (may return sooner if all
# results are received).
responses, no_responses = mp.receive(1)


try:

    # for addr, rtt in responses.items():
    #     print("%s responded in %f seconds" % (addr, rtt))

    count = 0

    if no_responses:
        #print("These addresses did not respond: %s" % ", ".join(no_responses))
        # Sending pings once more, but just to those addresses that have not
        # responded, yet. The MultiPing object 'mp' remembers the state of
        # which address has responded already, so that another call to
        # send() just generates packets to those hosts from which we haven't
        # heard back, yet.
        print("No response from something.. trying again")
        mp.send()
        responses, no_responses = mp.receive(2)

        content = "No responses:\n"
        for repsponseitem in no_responses:
            #print(repsponseitem) #print the no response item
            for value in values: #go though the original dictionary
                if value == repsponseitem:
                    newline = keys[count] + " at " + value + " is unreachable"
                    print(newline)
                    content = content + newline + "\n"
                count = count + 1
        if count > 0:
            sendemail()


    else:
        if count == 0:
            print("All addresses were found")

except Exception as e:
    print("There was an error:")
    print(str(e))
    quit()


