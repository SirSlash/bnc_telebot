#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import random
import time
import misc
from collections import OrderedDict

bot = telebot.TeleBot(misc.token)

global last_date
last_date = 0
global all_id
all_id = {}
global last_message_id
last_message_id = ""


class Secret:
    def __init__(self, chat_id):
        self.tryes = 0
        self.secret = self.set_number()
        self.result_table = OrderedDict()
        self.chat_id = chat_id

    def set_number(self, flag=0, qnumber="1234"):
        self.tryes = 0
        while flag != 4:
            flag = 0
            qnumber = str(random.randint(1023, 9876))
            for i in range(0, 4):
                for y in range(0, 4):
                    if qnumber[i] == qnumber[y]:
                        flag += 1
        self.secret = qnumber
        return qnumber

    def inc_tryes(self):
        self.tryes += 1

#number = Secret()


def get_obj(chat_id):
    return all_id.get(chat_id)


@bot.message_handler(commands=["start"])
def set_secrets(message):
    global all_id
    global last_message_id
    number = Secret(message.chat.id)
    """Создание словаря чатИД : класс чата"""
    all_id[message.chat.id] = number
    result = "Число загадано"
    last_message_id = message.message_id + 1
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=["show"])
def show_secrets(message):
    number = all_id.get(message.chat.id)
    try:
        bot.send_message(message.chat.id, number.secret)
        time.sleep(0.5)
    except Exception:
        bot.send_message(message.chat.id, "Cначала загадай число!")
        time.sleep(2)
    finally:
        bot.delete_message(message.chat.id, message.message_id + 1)


# @bot.message_handler(regexp="set")
# def set_secret(message):
#     number.secret = message.text[-4:]
#     bot.send_message(message.chat.id, number.secret)


@bot.message_handler(regexp="^\d\d\d\d$")
def human_try(message):
    number = all_id.get(message.chat.id)
    number.inc_tryes()
    h_try = message.text[-4:]
    question = number.secret
    b = 0
    c = 0
    result = "Быки : Коровы"
    global last_message_id
    for i in range(0, 4):
        if h_try[i] in question:
            c += 1
        if h_try[i] == question[i]:
            b += 1
    number.result_table[h_try] = [b, c, number.tryes]
    for key, values in number.result_table.items():
        result += "\n" + str(values[2]) + ": " + key + " | " + str(values[0]) + ":" + str(values[1])
    if b == 4:
        result += "\nУра! Ты подебил! Количество попыток: " + str(number.tryes)
        number.result_table.clear()
        number.set_number()
    try:
        bot.delete_message(message.chat.id, last_message_id)
    finally:
        pass
    last_message_id = message.message_id + 1
    bot.send_message(message.chat.id, result)


def is_not_spam(mesage_date):
    global last_date
    if last_date + 5 < mesage_date:
        last_date = mesage_date
        return True


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "/start   Для запуска/перезапуска игры\n"
                                      "/show  Для просмотра ответа")


bot.polling()
