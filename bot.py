import requests
import misc
from time import sleep

token = misc.token

URL = 'https://api.telegram.org/bot' + token + '/'

global last_update_id
last_update_id = 0


def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()


def get_message():
    data = get_updates()

    last_object = data['result'][-1]
    current_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != current_update_id:

        last_update_id = current_update_id

        chat_id = last_object['message']['chat']['id']
        who_name = last_object['message']['from']['first_name']
        message_text = ''
        try:
            message_text = last_object['message']['text']
        except:
            pass

        message = {'chat_id': chat_id,
                   'who_name': who_name,
                   'text': message_text}

        return message
    return None


def send_message(chat_id, text='Чего, блять?'):
    #url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, who_name + ', ' + text)
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.get(url)


def main():


    while True:
        answer = get_message()

        if answer != None:
            chat_id = answer['chat_id']
            #who_name = answer['who_name']
            text = answer['text']

            if 'зелен' in text.lower() or 'кто' in text.lower()\
                    or 'хуй' in text.lower():
                send_message(chat_id, 'Зелен - хуй.')
        else:
            continue

        sleep(2)


if __name__ == '__main__':
    main()
