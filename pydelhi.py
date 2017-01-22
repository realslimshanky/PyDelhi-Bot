from telegram.ext import Updater,CommandHandler
from telegram import ChatAction
from datetime import datetime, timezone
import logging,requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

updater=Updater(token='BOT_API_KEY')
dispatcher=updater.dispatcher

meetupApi={'sign':'true','key':'MEETUP_API_KEY'}

def start(bot, update, args):
	bot.sendMessage(chat_id=update.message.chat_id,text='''
Hi! My powers are solely for the service of PyDelhi Community
Use /help to get /help''')

def mailing_list(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	time.sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id,text='http://bit.ly/pydelhi-mailinglist')

def website(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	time.sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id,text='https://pydelhi.org/')

def irc(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	time.sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id,text='http://bit.ly/pydelhi-irc')

def twitter(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	time.sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='http://bit.ly/pydelhi-twitter')

def meetup(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	time.sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id,text='http://wwww.meetup.com/pydelhi')

def nextmeetup(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	time.sleep(0.2)
	r=requests.get('http://api.meetup.com/pydelhi/events', params=meetupApi)
	event_link=r.json()[0]['link']
	date_time=r.json()[0]['time']//1000
	utc_time = datetime.fromtimestamp(int(date_time), timezone.utc)
	local_time = utc_time.astimezone()
	date_time = local_time.strftime("%Y-%m-%d %H:%M:%S (%Z)")
	if 'venue' in r.json()[0]:
		venue=r.json()[0]['venue']['address_1']
	else:
		venue='Venue is still to be decided'
	bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup
Date/Time : %s
Venue : %s
'''%(date_time, venue))

def facebook(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id, text='http://bit.ly/pydelhi-facebook')

def github(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id, text='http://github.com/pydelhi')

def invitelink(bot,update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id, text='https://telegram.me/joinchat/B90LyQVj1nswbAk2x4tJ6g')

def help(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id, text='''
Use one of the following commands
/mailinglist - to get PyDelhi Mailing List link
/irc - to get a link to Pydelhi IRC channel
/twitter - to get Pydelhi Twitter link
/meetuppage - to get a link to PyDelhi Meetup page
/nextmeetup - to get info about next Meetup
/facebook - to get a link to PyDelhi Facebook page
/invitelink - to get an invite link for PyDelhi Telegram Group of Volunteers

To contribute to|modify this bot : https://github.com/realslimshanky/PyDelhi-Bot
''')

start_handler = CommandHandler('start', start, pass_args=True)
mailing_list_handler = CommandHandler('mailinglist', mailing_list)
website_handler = CommandHandler('website', website)
irc_handler = CommandHandler('irc', irc)
twitter_handler = CommandHandler('twitter', twitter)
meetup_handler = CommandHandler('meetuppage', meetup)
nextmeetup_handler = CommandHandler('nextmeetup', nextmeetup)
facebook_handler = CommandHandler('facebook', facebook)
github_handler = CommandHandler('github', github)
invitelink_handler = CommandHandler('invitelink', invitelink)
help_handler = CommandHandler('help', help)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(mailing_list_handler)
dispatcher.add_handler(website_handler)
dispatcher.add_handler(irc_handler)
dispatcher.add_handler(twitter_handler)
dispatcher.add_handler(meetup_handler)
dispatcher.add_handler(nextmeetup_handler)
dispatcher.add_handler(facebook_handler)
dispatcher.add_handler(github_handler)
dispatcher.add_handler(invitelink_handler)
dispatcher.add_handler(help_handler)

updater.start_polling()
