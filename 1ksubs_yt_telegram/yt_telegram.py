import telebot  # pip install pytelegrambotapi
import requests # used to query yt api

API_KEY = '<TELEGRAM API KEY>'
bot = telebot.TeleBot(API_KEY) #Init telebot w/ api key

key = '<YOUTUBE API KEY>'
channel_id = 'UCgF78i8PUYdKLgjpyeCJ7Qg' #Technotebook channel ID


@bot.message_handler(commands=['getsubscribers'])
def returnsubs(message):
    # YT Api Request
    r = requests.get(
        f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={key}')

    subs = r.json()['items'][0]['statistics']['subscriberCount']
    bot.reply_to(message, str(subs))


@bot.message_handler(commands=['getviews'])
def returnviews(message):
    # YT Api Request
    r = requests.get(
        f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={key}')

    subs = r.json()['items'][0]['statistics']['viewCount']
    bot.reply_to(message, str(subs))

# Tells bot to listen for msgs
bot.polling()
