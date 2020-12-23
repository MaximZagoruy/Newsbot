import logging
from datetime import datetime
import os
from time import sleep

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler
from telegram.ext import messagequeue as mq

from db import db, get_or_create_user, create_news_items
from vkparser import get_feed


from bot import subscribers

def greet_user(update, context):
    text = 'Вызван старт'
    logging.info(text)
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    bot_text =  'Hi there! Do you want to see some fresh news? Press News on keyboard'
    update.message.reply_text(bot_text, reply_markup=get_keyboard())

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([['News']], resize_keyboard=True)
    return my_keyboard

def get_more_button():
    my_keyboard = ReplyKeyboardMarkup([['More']], resize_keyboard=True)
    return my_keyboard

def get_news(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    from_indx = int(user.get('last_seen', 0))
    if from_indx == db.news.count():
        update.message.reply_text("I will check for some fresh news. Wait for a while please", reply_markup=ReplyKeyboardRemove())
        text = get_feed()
        if 'all' in text:
            update.message.reply_text("No fresh posts in here. Come back later", reply_markup=get_keyboard())
            return None
    to_indx = from_indx + 5
    news = db.news.find().sort('id', 1).distinct('id')[from_indx:to_indx]
    for item in news:
        item_object = db.news.find_one({'id': item})
        date = datetime.fromtimestamp(item_object['date']).strftime("%m/%d/%Y, %H:%M:%S")
        message = f"Original link: https://vk.com/wall-36180072_{item}\nDate: {date}\n\n{item_object['text']}"
        update.message.reply_text(message, reply_markup=get_more_button())
    db.users.update({"user_id": user["user_id"]}, {'$set': {'last_seen': to_indx}})