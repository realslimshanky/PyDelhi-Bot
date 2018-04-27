from telegram.ext import Updater, CommandHandler
from telegram import ChatAction
from datetime import datetime, timedelta
from pytz import timezone
from time import sleep
import logging
import requests
import pytz
import re
import ast
import os
import json
import sys
import signal
import subprocess

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

"""
---Process ID Management Starts---
This part of the code helps out when you want to run your program in background using '&'. This will save the process id of the program going in background in a file named 'pid'. Now, when you run you program again, the last one will be terminated with the help of pid. If in case the no process exist with given process id, simply the `pid` file will be deleted and a new one with current pid will be created.
"""
currentPID = os.getpid()
if 'pid' not in os.listdir():
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
else:
    with open('pid', mode='r') as f:
        try:
            os.kill(int(f.read()), signal.SIGTERM)
            print("Terminating previous instance of " +
                  os.path.realpath(__file__))
        except ProcessLookupError:
            subprocess.run(['rm', 'pid'])
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
"""
---Process ID Management Ends---
"""

"""
---Token/Key Management Starts---
This part will check for the config.txt file which holds the Telegram and Meetup Token/Key and will also give a user friendly message if they are invalid. New file is created if not present in the project directory.
"""
configError = "Please open config.txt file located in the project directory and relace the value '0' of Telegram-Bot-Token with the Token you recieved from botfather and similarly for Meetup-API-Key"
if 'config.txt' not in os.listdir():
    with open('config.txt', mode='w') as f:
        json.dump({'Telegram-Bot-Token': 0, 'Meetup-API-Key': 0}, f)
        print(configError)
        sys.exit(0)
else:
    with open('config.txt', mode='r') as f:
        config = json.loads(f.read())
        if config["Telegram-Bot-Token"] or config["Meetup-API-Key"]:
            print("Token Present, continuing...")
            TelegramBotToken = config["Telegram-Bot-Token"]
            MeetupAPIKey = config["Meetup-API-Key"]
        else:
            print(configError)
            sys.exit(0)
"""
---Token/Key Management Ends---
"""

updater = Updater(token=TelegramBotToken)
dispatcher = updater.dispatcher

meetupApi = {'sign': 'true', 'key': MeetupAPIKey}

utc = pytz.utc

volunteer = {}

admins = ['anuvrat', 'piyushmaurya23', 'aktech',
          'akash47', 'Quanon', 'realslimshanky']

with open('volunteer.json', 'r') as fp:
    volunteer = ast.literal_eval(fp.read())

print("I'm On..!!")


def start(bot, update, args):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id, text='''
Hi! My powers are solely for the service of PyDelhi Community
Use /help to get /help''')


def mailing_list(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://bit.ly/pydelhi-mailinglist')


def website(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='https://pydelhi.org/')


def irc(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://bit.ly/pydelhi-irc')


def twitter(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://bit.ly/pydelhi-twitter')


def meetup(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://wwww.meetup.com/pydelhi')


def nextmeetup(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    r = requests.get('http://api.meetup.com/pydelhi/events', params=meetupApi)
    # print(r.json()[0])
    event_link = r.json()[0]['link']
    date_time = r.json()[0]['time']//1000
    utc_dt = utc.localize(datetime.utcfromtimestamp(date_time))
    indian_tz = timezone('Asia/Kolkata')
    date_time = utc_dt.astimezone(indian_tz)
    date_time = date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    if 'venue' in r.json()[0]:
        venue = r.json()[0]['venue']['name']
        address = r.json()[0]['venue']['address_1']
        bot.sendLocation(chat_id=update.message.chat_id, latitude=r.json()[
                         0]['venue']['lat'], longitude=r.json()[0]['venue']['lon'])
    else:
        venue = 'Venue is still to be decided'
        address = 'Address will be updated once venue is fixed'
    bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup
Date/Time : %s
Venue : %s
Address : %s
Event Page : %s
''' % (date_time, venue, address, event_link))


def nextmeetups(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    r = requests.get('http://api.meetup.com/pydelhi/events', params=meetupApi)
    #print(re.sub('</a>','',re.sub('<a href="','',re.sub('<br/>',' ',re.sub('<p>',' ',re.sub('</p>','\n',r.json()[0]['description']))))))
    bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup Schedule
%s
''' % (re.sub('</a>', '', re.sub('<a href="', '', re.sub('<br/>', ' ', re.sub('<p>', ' ', re.sub('</p>', '\n', r.json()[0]['description'])))))), parse_mode='HTML')


def facebook(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://bit.ly/pydelhi-facebook')


def github(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://github.com/pydelhi')


def invitelink(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='https://t.me/joinchat/AAAAAEK2nzPg0IlwbbAing')


#~ def socialmediateam(bot, update):
    #~ m = update.message.to_dict()
    #~ username = m['from']['username']
    #~ if username in admins:
        #~ team = '  '.join(volunteer['socialmedia'].split('-'))
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Social Media team
#~ """+team+"""
#~ You have been summoned by @"""+username+""". Please appear online.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one in this team yet.')
    #~ else:
        #~ v = [x[1:] for x in volunteer['socialmedia'].split('-')]
        #~ team = '  '.join(v)
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Social Media team
#~ """+team+"""
#~ Please use '@' at the start of each username to ping them.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one in this team yet.')


#~ def designteam(bot, update):
    #~ m = update.message.to_dict()
    #~ username = m['from']['username']
    #~ if username in admins:
        #~ team = '  '.join(volunteer['design'].split('-'))
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Design Team
#~ """+team+"""
#~ You have been summoned by @"""+username+""". Please appear online.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one in this team yet.')
    #~ else:
        #~ v = [x[1:] for x in volunteer['design'].split('-')]
        #~ team = '  '.join(v)
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Design Team
#~ """+team+"""
#~ Please use '@' at the start of each username to ping them.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one in this team yet.')


#~ def logisticsteam(bot, update):
    #~ m = update.message.to_dict()
    #~ username = m['from']['username']
    #~ if username in admins:
        #~ team = '  '.join(volunteer['logistics'].split('-'))
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Logistics Team
#~ """+team+"""
#~ You have been summoned by @"""+username+""". Please appear online.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one in this team yet.')
    #~ else:
        #~ v = [x[1:] for x in volunteer['logistics'].split('-')]
        #~ team = '  '.join(v)
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Logistics Team
#~ """+team+"""
#~ Please use '@' at the start of each username to ping them.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one in this team yet.')


#~ def websiteteam(bot, update):
    #~ m = update.message.to_dict()
    #~ username = m['from']['username']
    #~ if username in admins:
        #~ team = '  '.join(volunteer['website'].split('-'))
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Website Team
#~ """+team+"""
#~ You have been summoned by @"""+username+""". Please appear online.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one in this team yet.')
    #~ else:
        #~ v = [x[1:] for x in volunteer['website'].split('-')]
        #~ team = '  '.join(v)
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Website Team
#~ """+team+"""
#~ Please use '@' at the start of each username to ping them.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one in this team yet.')


#~ def vendorteam(bot, update):
    #~ m = update.message.to_dict()
    #~ username = m['from']['username']
    #~ if username in admins:
        #~ team = '  '.join(volunteer['vendor'].split('-'))
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Vendor Team
#~ """+team+"""
#~ You have been summoned by @"""+username+""". Please appear online.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='Noone on this team yet.')
    #~ else:
        #~ v = [x[1:] for x in volunteer['vendor'].split('-')]
        #~ team = '  '.join(v)
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Vendor Team
#~ """+team+"""
#~ Please use '@' at the start of each username to ping them.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='Noone on this team yet.')


#~ def venueteam(bot, update):
    #~ m = update.message.to_dict()
    #~ username = m['from']['username']
    #~ if username in admins:
        #~ team = '  '.join(volunteer['venue'].split('-'))
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Venue Team
#~ """+team+"""
#~ You have been summoned by @"""+username+""". Please appear online.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='Noone on this team yet.')
    #~ else:
        #~ v = [x[1:] for x in volunteer['venue'].split('-')]
        #~ team = '  '.join(v)
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Venue Team
#~ """+team+"""
#~ Please use '@' at the start of each username to ping them.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='Noone on this team yet.')


#~ def sponsorshipteam(bot, update):
    #~ m = update.message.to_dict()
    #~ username = m['from']['username']
    #~ if username in admins:
        #~ team = '  '.join(volunteer['sponsorship'].split('-'))
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Sponsorship Team
#~ """+team+"""
#~ You have been summoned by @"""+username+""". Please appear online.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one on this team yet.')
    #~ else:
        #~ v = [x[1:] for x in volunteer['sponsorship'].split('-')]
        #~ team = '  '.join(v)
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""Sponsorship Team
#~ """+team+"""
#~ Please use '@' at the start of each username to ping them.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one on this team yet.')


#~ def cfpteam(bot, update):
    #~ m = update.message.to_dict()
    #~ username = m['from']['username']
    #~ if username in admins:
        #~ team = '  '.join(volunteer['cfp'].split('-'))
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""CFP Team
#~ """+team+"""
#~ You have been summoned by @"""+username+""". Please appear online.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one on this team yet.')
    #~ else:
        #~ v = [x[1:] for x in volunteer['cfp'].split('-')]
        #~ team = '  '.join(v)
        #~ if team != '':
            #~ bot.sendMessage(chat_id=update.message.chat_id, text="""CFP Team
#~ """+team+"""
#~ Please use '@' at the start of each username to ping them.""")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='No one on this team yet.')


#~ def modifyteam(bot, update, args):
    #~ m = update.message.to_dict()
    #~ username = m['from']['username']
    #~ if username in admins:
        #~ if m['chat']['type'] == 'private':
            #~ if m['chat']['id'] == -90429051:
                #~ bot.sendMessage(chat_id=update.message.chat_id,
                                #~ text='You can only make changes from inside PyDelhi Group')
            #~ else:
                #~ if len(args) < 3:
                    #~ bot.sendMessage(chat_id=update.message.chat_id,
                                    #~ text='Please type /modifyteam <space> add/remove <space> socialmedia/design/website/vendor/logistics/sponsorship/cfp/venue <space> space seperated usernames.')
                #~ else:
                    #~ if args[0] == 'add' or args[0] == 'remove':
                        #~ if args[1] == 'socialmedia' or args[1] == 'website' or args[1] == 'vendor' or args[1] == 'logistics' or args[1] == 'design' or args[1] == 'sponsorship' or args[1] == 'venue' or args[1] == 'cfp':
                            #~ team = volunteer[args[1]].split('-')
                            #~ if args[0] == 'add':
                                #~ for x in args[2:]:
                                    #~ if x.startswith('@') == False:
                                        #~ bot.sendMessage(
                                            #~ chat_id=update.message.chat_id, text="Username '"+x+"' is invalid, please use @ properly.")
                                        #~ return
                                    #~ elif x in team:
                                        #~ args.remove(x)
                                        #~ bot.sendMessage(
                                            #~ chat_id=update.message.chat_id, text="Username '"+x+"' already exists on "+args[1]+" team, ignoring.")
                                #~ if len(args[2:]) != 0:
                                    #~ team.extend(args[2:])
                                    #~ volunteer[args[1]] = '-'.join(team)
                                    #~ try:
                                        #~ v = open('volunteer.json', 'w')
                                        #~ v.write(str(volunteer))
                                        #~ v.close()
                                        #~ bot.sendMessage(
                                            #~ chat_id=update.message.chat_id, text="Team Modified")
                                    #~ except:
                                        #~ bot.sendMessage(
                                            #~ chat_id=update.message.chat_id, text="Their might be some problem with the server, please try again later or contact @realslimshanky.")
                                #~ else:
                                    #~ bot.sendMessage(
                                        #~ chat_id=update.message.chat_id, text="Nothing to modify in team.")
                            #~ else:
                                #~ for x in args[2:]:
                                    #~ if x.startswith('@') == False:
                                        #~ bot.sendMessage(
                                            #~ chat_id=update.message.chat_id, text="Username '"+x+"' is invalid, please use @ properly.")
                                        #~ return
                                    #~ elif x not in team:
                                        #~ args.remove(x)
                                        #~ bot.sendMessage(
                                            #~ chat_id=update.message.chat_id, text="Username '"+x+"' doesn't exists on "+args[1]+" team, ignoring.")
                                #~ if len(args[2:]) != 0:
                                    #~ for x in args[2:]:
                                        #~ if x in team:
                                            #~ team.remove(x)
                                    #~ volunteer[args[1]] = '-'.join(team)
                                    #~ try:
                                        #~ v = open('volunteer.json', 'w')
                                        #~ v.write(str(volunteer))
                                        #~ v.close()
                                        #~ bot.sendMessage(
                                            #~ chat_id=update.message.chat_id, text="Team Modified")
                                    #~ except:
                                        #~ bot.sendMessage(
                                            #~ chat_id=update.message.chat_id, text="Their might be some problem with the server, please try again later or contact @realslimshanky.")
                                #~ else:
                                    #~ bot.sendMessage(
                                        #~ chat_id=update.message.chat_id, text="Nothing to modify in team.")
                        #~ else:
                            #~ bot.sendMessage(
                                #~ chat_id=update.message.chat_id, text="Please use on of these teams, socialmedia/design/website/vendor/logistics/sponsorship/cfp/venues")
                    #~ else:
                        #~ bot.sendMessage(
                            #~ chat_id=update.message.chat_id, text="Please 'add' or 'remove'")
        #~ else:
            #~ bot.sendMessage(chat_id=update.message.chat_id,
                            #~ text='You cannot edit team members in a private chat.')


#~ def teams(bot, update):
    #~ bot.sendChatAction(chat_id=update.message.chat_id,
                       #~ action=ChatAction.TYPING)
    #~ sleep(0.2)
    #~ bot.sendMessage(chat_id=update.message.chat_id, text='''
#~ /socialmediateam
#~ /logisticsteam
#~ /websiteteam
#~ /designteam
#~ /cfpteam
#~ /sponsorshipteam
#~ /vendorteam
#~ /venueteam
#~ ''')


def help(bot, update):
    # /teams - to get all the team names ( Depreciated )
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id, text='''
Use one of the following commands
/mailinglist - to get PyDelhi Mailing List link
/irc - to get a link to Pydelhi IRC channel
/twitter - to get Pydelhi Twitter link
/meetuppage - to get a link to PyDelhi Meetup page
/nextmeetup - to get info about next Meetup
/nextmeetupschedule - to get schedule of next Meetup
/facebook - to get a link to PyDelhi Facebook page
/github - to get a link to PyDelhi Github page
/invitelink - to get an invite link for PyDelhi Telegram Group of Volunteers

To contribute to|modify this bot : https://github.com/realslimshanky/PyDelhi-Bot
''')


dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
dispatcher.add_handler(CommandHandler('mailinglist', mailing_list))
dispatcher.add_handler(CommandHandler('website', website))
dispatcher.add_handler(CommandHandler('irc', irc))
dispatcher.add_handler(CommandHandler('twitter', twitter))
dispatcher.add_handler(CommandHandler('meetuppage', meetup))
dispatcher.add_handler(CommandHandler('nextmeetup', nextmeetup))
dispatcher.add_handler(CommandHandler('nextmeetupschedule', nextmeetups))
dispatcher.add_handler(CommandHandler('facebook', facebook))
dispatcher.add_handler(CommandHandler('github', github))
dispatcher.add_handler(CommandHandler('invitelink', invitelink))
#~ dispatcher.add_handler(CommandHandler('socialmediateam', socialmediateam))
#~ dispatcher.add_handler(CommandHandler('logisticsteam', logisticsteam))
#~ dispatcher.add_handler(CommandHandler('websiteteam', websiteteam))
#~ dispatcher.add_handler(CommandHandler('designteam', designteam))
#~ dispatcher.add_handler(CommandHandler('cfpteam', cfpteam))
#~ dispatcher.add_handler(CommandHandler('sponsorshipteam', sponsorshipteam))
#~ dispatcher.add_handler(CommandHandler('vendorteam', vendorteam))
#~ dispatcher.add_handler(CommandHandler('venueteam', venueteam))
#~ dispatcher.add_handler(CommandHandler('teams', teams))
#~ dispatcher.add_handler(CommandHandler(
    #~ 'modifyteam', modifyteam, pass_args=True))
#~ dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
