# buttons_bot.py
import time
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler

import sys
import os
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import tqdm
from tqdm.notebook import tqdm

dict = {}
dict1 = {}
# Step 1. 크롬 웹브라우저 실행
path = "chromedriver.exe"  # 윈도우는 "chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument( '--headless' )
chrome_options.add_argument( '--log-level=3' )
chrome_options.add_argument( '--disable-logging' )
chrome_options.add_argument( '--no-sandbox' )
chrome_options.add_argument( '--disable-gpu' )

driver = webdriver.Chrome(path)
# 사이트 주소는 코로나바이러스감염증-19(COVID-19)
driver.get('http://ncov.mohw.go.kr/')
time.sleep(2)

# 일일확진자
one_day_COVID_19 = driver.find_element_by_class_name("tit")
one_day_COVID_19_text = one_day_COVID_19.text


BOT_TOKEN = 'self telegram token'

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher





def cmd_task_buttons(update, context):
    task_buttons = [[
        InlineKeyboardButton('1.일일확진자', callback_data=1)
        , InlineKeyboardButton('2.지역별', callback_data=2)
    ], [
        InlineKeyboardButton('3.취소', callback_data=3)
    ]]

    reply_markup = InlineKeyboardMarkup(task_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id
        , text='코로나 현황'
        , reply_markup=reply_markup
    )


def cb_button(update, context):
    query = update.callback_query
    data = query.data

    context.bot.send_chat_action(
        chat_id=update.effective_user.id
        , action=ChatAction.TYPING
    )

    if data == '3':
        context.bot.edit_message_text(
            text='작업이 취소되었습니다.'
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )
    else:
        context.bot.edit_message_text(
            text='[{}] 로딩중입니다.'.format(data)
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )

        if data == '1':
            for i in range(0, 2):
                # 코로나 확진자 정보
                COVID_19_text = driver.find_elements_by_css_selector("span.subtit")
                COVID_19_data = driver.find_elements_by_css_selector("span.data")
                # 코로나 발생자 domestic incidence / 해외유입 overseas inflow
                # COVID_19_text_inout = COVID_19_text[i].text
                # COVID_19_data_inout = COVID_19_data[i].text
            COVID_19_data_sum = COVID_19_text[0].text + ' ' + COVID_19_data[0].text + ' ' + COVID_19_text[1].text + ' ' + COVID_19_data[1].text
            context.bot.send_message(
                chat_id=update.effective_chat.id
                , text=COVID_19_data_sum
            )
        elif data == '2':
            for j in range(0, 18):
                city_data = driver.find_element_by_xpath("""//*[@id="main_maplayout"]/button[{}]""".format(j + 1))
                city_data_text = city_data.text
                context.bot.send_message(
                    chat_id=update.effective_chat.id
                    , text=city_data_text
            )




def crawl_navernews():
    time.sleep(5)
    print('일일확진자 로딩완료.')


def crawl_zigbang():
    time.sleep(5)
    print('지역별 로딩완료')


task_buttons_handler = CommandHandler('tasks', cmd_task_buttons)
button_callback_handler = CallbackQueryHandler(cb_button)

dispatcher.add_handler(task_buttons_handler)
dispatcher.add_handler(button_callback_handler)

updater.start_polling()
updater.idle()
