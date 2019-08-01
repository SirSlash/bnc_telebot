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


@bot.message_handler(commands=['Psize'])
def size(message):
    if is_not_spam(message.date):
        pbody = ""
        for length in range(random.randint(0, 10)):
            pbody += "="
        pines = "#3" + pbody + "D"
        if message.from_user.id == "533196112":
            who = "Puh"
        else:
            who = message.from_user.first_name

        bot.send_message(message.chat.id, who)
        bot.send_message(message.chat.id, pines)


# @bot.callback_query_handler
# def edit_bot_message(message):


# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, 'Hello World')
#     global last_message_id
#     last_message_id = message.message_id + 1
#     bot.delete_message(message.chat.id, message.message_id + 1)

# @bot.message_handler(commands=['zelen_suck'])
# def feed(message):
#     if is_not_spam(message.date) and message.from_user.first_name != "Pavel":
#         bot.send_message(message.chat.id, "Зелен -> :-D")
#         time.sleep(2)
#         bot.send_message(message.chat.id, ":-D")
#         time.sleep(2)
#         bot.send_message(message.chat.id, ":-D   e==3")
#         time.sleep(2)
#         bot.send_message(message.chat.id, ":-D  e==3")
#         time.sleep(2)
#         bot.send_message(message.chat.id, ":-D e==3")
#         time.sleep(2)
#         bot.send_message(message.chat.id, ":-De==3")
#         time.sleep(5)
#         bot.send_message(message.chat.id, ":-O==3")
#         time.sleep(2)
#         bot.send_message(message.chat.id, ":-O=3")
#         time.sleep(2)
#         bot.send_message(message.chat.id, ":-O3")
#         time.sleep(2)
#         bot.send_message(message.chat.id, ":-3)")
#
#
# @bot.message_handler(regexp="кто хуй")
# def send_who(message):
#     if is_not_spam(message.date):
#         answers = ["ты", "Зелен", "твой батя", "хуй", message.from_user.first_name, "Обама", "ты тупой?", "я", "Дуров", "«Хуй» — одно из основных слов русского мата, является в нём словообразующим для множества других слов и выражений. Используется в значении «мужской половой член» и многих других.",
#                    message.from_user.first_name + " хочет под хвост", message.from_user.first_name + " пидор",
#                    "Смирнов", "Коробкин", "Пух", "Серый", "Сервер", "Дороф", "Хамиль", "Юра", "Вова"]
#         answer = random.choice(answers)
#
#         bot.send_message(message.chat.id, answer)
#
#
# @bot.message_handler(regexp="зелен")
# def send_welcome(message):
#     if is_not_spam(message.date):
#         answers = ["Путин", "хуй", "жир", "красавчик", "ватник", "рептилойд", "не Зелен", "еврей",
#                    "художник", "змагар", "Смирнов", "норм", "очень гейен", "8===Э", "карасик", "был в твоей мамке"]
#         zelen = "Зелен — " + random.choice(answers)
#
#         bot.send_message(message.chat.id, zelen)


def is_not_spam(mesage_date):
    global last_date
    if last_date + 5 < mesage_date:
        last_date = mesage_date
        return True

# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_msg(message):
#     bot.send_message(message.chat.id, message.text)

#@bot.message_handler(commands=['start', 'help'])
#def send_welcome(message):
#    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "/start   Для запуска/перезапуска игры\n"
                                      "/show  Для просмотра ответа")

# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     bot.reply_to(message, message.text) interval=random.randint(0, 10)


bot.polling()
