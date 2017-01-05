import time, subprocess, sys
from twython import Twython, TwythonError
# This program is an attempt to make my computer insecure using command line from Twitter
# Author: batycoon, Jan 3 2017
# Cannot currently change directory. May look into keyword pass to implement Context Manager like http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
# Bug: Program will pause indefinitely at user prompt for password if not given in some "echo pw | sudo -S cmd" form

# Placeholders for config_var
#APP_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
#APP_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
#OAUTH_TOKEN = 'xxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
#OAUTH_TOKEN_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Comment following line out if you intend to fill above for a single file program.
from config_var_a import *

core = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
data = core.get_direct_messages(count=2)
compvar = data[0]['created_at']
# N = Max multi-number of messages read if more than one input found. (Max 199)
N = 10
# t = standard wait time, tshort = shortest wait time
t = 15
tshort = 3

class call:
    def cmd(text):
        #potential: if some keyword in text, run python command instead.
        subprocess.call(text, shell=True)

# query 2. if no new messages, sleep. if more than one message, query N+1. if more than N messages, release  all. execute messages in cronological order, sleep.
while 1:
    try:
        data = core.get_direct_messages(count=2)
        if (data[0]['created_at'] == compvar):
            time.sleep(t)
        else:
            if (data[1]['created_at'] != compvar):
                print '\nmultiscript detected, comparing up to '+str(N)+' scripts' 
                try:
                    data = core.get_direct_messages(count=N+1)
                except TwythonError as e:
                    print e
                count = 0
                for n in range(0,len(data)): #zero is most recent message, more may exist
                    if (data[n]['created_at'] == compvar):
                        count = n
                if (count == 0):
                    print 'too many lost scripts, releasing all scripts\n'
                    compvar = data[0]['created_at']
                    time.sleep(tshort)
                else:
                    compvar = data[0]['created_at']
                    for i in reversed(range(count)):
                        print 'Script sent by '+data[i]['sender']['name']+''
                        try:
                            print data[i]['text']
                            call.cmd(data[i]['text'])
                        except OSError as e:
                            print e
                    time.sleep(tshort)
            else:
                compvar = data[0]['created_at']
                print 'Script sent by '+data[0]['sender']['name']+''
                try:
                    print data[0]['text']
                    call.cmd(data[0]['text'])
                except OSError as e:
                    print e
                time.sleep(t)
    except KeyboardInterrupt as e:
        print '\nquitting'
        sys.exit()

