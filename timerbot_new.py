#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

import os

#PORT = int(os.environ.get('PORT', 5000))
PORT = int(os.environ.get('PORT', 8443))
import logging
import random
import pandas as pd
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import datetime
import pytz
import time


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
messages = {}

class state:
    def __init__(self, rate=None, passages=None):
        self.time = 12
        self.rate = rate
        self.passages= passages

stat = state()
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext):
    context.job_queue.run_daily(more2, days =  (0, 1, 2, 3, 4, 5, 6), time = datetime.time(hour=12, minute = 00, second = 00, tzinfo=pytz.timezone('Europe/Moscow')), context = update)
    text = """Zen bot regulary at 12:00 gives out a passage from a Zen book by Allan Watts. Type /more if you want some zen-ness off schedule. Type /set if you want to change default time (type hour from 0 till 23)"""
    update.message.reply_text(text)
    data = pd.read_csv('concatenated_2.csv', sep = '&')
    stat.data = data.rate
    stat.passages = data.passage
   
def passage():
    text = random.choices(stat.passages, weights=(stat.rate), k =1)
    return text[0]

def more2(update: Update):
    text = passage()
    while len(text):
        try:
            update.message.reply_text(text = text[:4050], parse_mode='HTML')
            text = text[4050:]
            time.sleep(0.3)
        except:
            update.message.reply_text(text = text, parse_mode='HTML') 
            text = ''
    
def more(update: Update, context: CallbackContext):
    text = passage()
    while len(text) > 0:
        try:
            update.message.reply_text(text = text[:4050], parse_mode='HTML')
            text = text[4050:]
            time.sleep(0.3)
        except:
            update.message.reply_text(text = text, parse_mode='HTML') 
            text = ''
    
    
def set_timer(update: Update, context: CallbackContext):
    stat.time = int(context.args[0])
    chat_id = update.message.chat_id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in current_jobs:
        job.schedule_removal()
    context.job_queue.run_daily(more2, days =  (0, 1, 2, 3, 4, 5, 6), time = datetime.time(hour=12, minute = 00, second = 00, tzinfo=pytz.timezone('Europe/Moscow')), context = update)
    text = 'Successfully set!'
    update.message.reply_text(text)
    

def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1711952452:AAEjsoXJVKy-k7XRU1C3KKi1Q16W66ypcFA")
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("more", more))
    
    

    # Start the Bot
    updater.start_polling()
    '''updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path='1711952452:AAEjsoXJVKy-k7XRU1C3KKi1Q16W66ypcFA',
                          webhook_url='https://telegram-bot16453.herokuapp.com/1711952452:AAEjsoXJVKy-k7XRU1C3KKi1Q16W66ypcFA')
    '''
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
