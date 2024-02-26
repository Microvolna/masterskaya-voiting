import telebot
from telebot import types
import random

import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    if config.variant_1['posted'] != True:
        btn1 = types.InlineKeyboardButton(config.variant_1['topic'], callback_data='btn1')
        markup.add(btn1)
    if config.variant_2['posted'] != True:
        btn2 = types.InlineKeyboardButton(config.variant_2['topic'], callback_data='btn2')
        markup.add(btn2)
    if config.variant_3['posted'] != True:
        btn3 = types.InlineKeyboardButton(config.variant_3['topic'], callback_data='btn3')
        markup.add(btn3)
    
    if message.chat.id == config.admin_id:
        bot.send_message(message.chat.id, config.message_text, reply_markup=markup)
        bot.send_message(config.chanel_id, config.message_text, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, '👋😌🌄У Вас нет прав.')

@bot.message_handler(commands=['github'])
def statistic_message(message):
    bot.send_message(message.chat.id, f'Ссылка на репозиторий: https://github.com/Microvolna/masterskaya-voiting')

@bot.message_handler(commands=['delete_data'])
def statistic_message(message):
    if message.chat.id == int(config.admin_id):
        config.variant_1['vote'] = []
        config.variant_2['vote'] = []
        config.variant_3['vote'] = []
        bot.send_message(message.chat.id, f'Данные очищены')
    else:
        bot.send_message(message.chat.id, '👋😌🌄У Вас нет прав.')

@bot.message_handler(commands=['statistic'])
def statistic_message(message):
    bot.send_message(message.chat.id, f'''
1. {config.variant_1['topic']} - {len(config.variant_1['vote'])}
2. {config.variant_2['topic']} - {len(config.variant_2['vote'])}
3. {config.variant_3['topic']} - {len(config.variant_3['vote'])}''')
    
@bot.message_handler(commands=['send_post'])
def send_post_message(message):
    if message.chat.id == config.admin_id:

        num_1 = 0
        num_2 = 0
        num_3 = 0

        if config.variant_1['vote'] != []:
            num_1 = len(config.variant_1['vote'])

        elif config.variant_2['vote'] != []:
            num_2 = len(config.variant_2['vote'])

        elif config.variant_3['vote'] != []:
            num_3 = len(config.variant_3['vote'])

        print(config.variant_1['vote'])
        print(config.variant_2['vote'])
        print(config.variant_3['vote'])


        if num_1 == num_2 and num_1 == num_3:
            random.choice([config.variant_1['text'], config.variant_2['text'], config.variant_3['text']])

        elif num_1 == num_3 and num_1 > num_2:
            b = random.choice([[config.variant_1['text']], config.variant_3['text']])

        elif num_2 == num_3 and num_2 > num_1:
            b = random.choice([[config.variant_2['text']], config.variant_3['text']])

        elif num_1 > num_2 and num_1 > num_3:
            b = config.variant_1['text']

        elif num_2 > num_1 and num_2 > num_3:
            b = config.variant_2['text']

        elif num_3 > num_1 and num_3 > num_2:
            b = config.variant_3['text']


        bot.send_message(config.chanel_id, b)
        bot.send_message(message.chat.id, f'''Сообщение отправлено в {config.chanel_id}

Текст поста:
                         
{b}''')
    else:
        bot.send_message(message.chat.id, '👋😌🌄У Вас нет прав.')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "btn1":
        if call.from_user.id in config.variant_1['vote'] or call.from_user.id in config.variant_2['vote'] or call.from_user.id in config.variant_3['vote']:
            pass
        else:
            config.variant_1['vote'].append(call.from_user.id)
            bot.send_message(config.admin_id, '1')
    if call.data == "btn2":
        if call.from_user.id in config.variant_1['vote'] or call.from_user.id in config.variant_2['vote'] or call.from_user.id in config.variant_3['vote']:
            pass
        else:
            config.variant_2['vote'].append(call.from_user.id)
            bot.send_message(config.admin_id, '2')
    if call.data == "btn3":
        if call.from_user.id in config.variant_1['vote'] or call.from_user.id in config.variant_2['vote'] or call.from_user.id in config.variant_3['vote']:
            pass
        else:
            config.variant_3['vote'].append(call.from_user.id)
            bot.send_message(config.admin_id, '3')

bot.infinity_polling()