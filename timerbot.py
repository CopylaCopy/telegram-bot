#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.

This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os

PORT = int(os.environ.get('PORT', 8443))
import logging
import random
import codecs
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
#import telegram
#telegram.constants.PARSEMODE_HTML

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
messages = {}



class passage:
    def __init__(self):
        self.rate = None
        self.proposed_raw_passages = []
        self.text = ''
        self.useful = None
        self.id = 1
    def merge(self, *args):

        *numbers, self.rate = args[0]
        self.useful = len(numbers)
        numbers = [int(number) - 1 for number in numbers]
        self.text = '\n'.join([self.proposed_raw_passages[number] for number in numbers])
        self.id +=1
        with engine.connect() as connection:
            connection.execute(text(f"insert into passages2 values({self.id}, {self.rate}, '{self.text}')"))
                
    def clean(self):
        self.proposed_raw_passages = []
        self.text = ''
        
        
 
class state:
    """global state for that user"""
    def __init__(self):
        self.pas = passage()
        self.cur_key, self.cur_index = self.load_init_state()
        self.html = None
        self.html_iter = None
    def load_init_state(self):
        #with open('state.txt', 'r') as f:
            #num = f.read()
        with engine.connect() as connection:
            result = connection.execute(text("select * from status where key=(select max(key) from status)"))
            result = result.fetchall()[0]
            return [int(i) for i in result]
        return int(result)
    def clean_and_up(self):
        self.cur_index += self.pas.useful
        self.cur_key +=1

        with engine.connect() as connection:
            connection.execute(text(f"insert into status values({stat.cur_key}, {stat.cur_index})"))

        self.html_iter = iter(self.html[self.cur_index:])
        print('hash was cleaned, iterator updated')
        
        
stat = state()
    
    
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext):
    text = """This bot is in the state of forming DB of passages.
    You can help boost the process. 
    Type /more to get the passage, after that type /more,
    if you think that current passage is too small, 
    or doesn't contain the complete message. 
    After that, rate the passage. To do it, type the numbers of passages you want to merge,
    and type the number from 1 to 9. If you  think that this passage
    doesn't contain any zen-ness, just type 0. Example: /rate 12347; /rate 120"""
    update.message.reply_text(text)
    with codecs.open('tet.txt', 'r', 'utf-8') as f:
        html = f.read()
    stat.html = html.split('&*&')
    stat.html_iter = iter(stat.html[stat.cur_index:])
    
    
def rate(update: Update, context: CallbackContext):
    numbers = context.args[0]
    print(numbers)
    try: 
        check(numbers)
        
        stat.pas.merge(numbers)
        stat.clean_and_up()
        stat.pas.clean()
        update.message.reply_text(text = 'passage successfully saved!')
    except ValueError as e:
        update.message.reply_text(text = str(e))
        
def check(numbers):
    if len(numbers) < 2:
        raise ValueError('Error: you should type at least two numbers: the number of passage and its rating')
    if len(numbers[:-1]) > 9:
        raise ValueError('Error: you can\'t merge more than 9 passages')
    if len(numbers[:-1]) > len(stat.pas.proposed_raw_passages):
        raise ValueError('Error: you can\'t merge more passages than you have read')
    if numbers[:-1] != ''.join(str(i)for i in list(range(1, len(numbers)))):
        raise ValueError('Error: you can only merge passages that follow each other')



def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    text=replicas()
    context.bot.send_message(job.context, text = text)
    
def more(update: Update, _: CallbackContext):
    text = replicas()
    update.message.reply_text(text = text)

def more2(update: Update, _: CallbackContext):
    text = next(stat.html_iter) 
    update.message.reply_text(text = text, parse_mode='HTML')
    stat.pas.proposed_raw_passages.append(text)
    


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


'''def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

        #text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')'''
        
def set_timer_mine(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    context.job_queue.run_once(alarm, 43200, context=chat_id, name=str(chat_id))
    


'''def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)'''
    
    
def replicas():
    max_val = max(messages.values(), key=lambda val: val[0])
    av = [[num,replica] for num, replica in messages.items() if replica[0] == max_val[0]]
    choosed_replica = random.choice(av)
    choosed_num = choosed_replica[0]
    new_prob = [messages[choosed_num][0] - 0.5, messages[choosed_num][1]]
    messages[choosed_num] = new_prob
    for i in messages.keys():
        if i != choosed_num:
            new_prob = [messages[i][0] + 0.1, messages[i][1]]
    return choosed_replica[1][1]
    
'''def check_2(update: Update, _: CallbackContext):
    with open('state.txt', 'r') as f:
        num = f.read()
        print(num)'''  
    


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("1711952452:AAEjsoXJVKy-k7XRU1C3KKi1Q16W66ypcFA")
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_timer_mine))
    dispatcher.add_handler(CommandHandler("more", more2))
    dispatcher.add_handler(CommandHandler("rate", rate))
    

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path='1711952452:AAEjsoXJVKy-k7XRU1C3KKi1Q16W66ypcFA',
                          webhook_url='https://sheltered-thicket-28654.herokuapp.com/1711952452:AAEjsoXJVKy-k7XRU1C3KKi1Q16W66ypcFA')

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
