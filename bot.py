from glob import glob
import logging
from random import choice

from emoji import emojize
from datetime import date
import ephem
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log',
                    encoding='utf-8'
                    )


def greet_user(update, context):
        emo = get_user_emo(context.user_data)
        context.user_data['emo'] = emo
        text = 'Привет {}'.format(emo)
        my_keyboard = ReplyKeyboardMarkup([['Прислать котика', 'Сменить аватарку']])
        update.message.reply_text(text, reply_markup=my_keyboard)

def planet(update, context):
    try:
        planet_name = str(update.message.text.split(" ")[1]).lower().capitalize()
        day = date.today()
        planet = getattr(ephem, planet_name)(day)
        const = ephem.constellation(planet)
        answer = f"На сегодняшнию дату {day} планета {planet_name} находится в созвездии {const}"
    except AttributeError:
        answer = f"Планеты {planet_name} не существует"
    update.message.reply_text(answer)

def talk_to_me(update, context):
        emo = get_user_emo(context.user_data)
        user_text = "Привет {} {}! Ты написал: {}".format(update.message.chat.first_name, emo, update.message.text)
        logging.info("User: %s,Chat id: %s, Message: %s", update.message.chat.first_name,
                     update.message.chat.id, update.message.text)
        update.message.reply_text(user_text)

def send_cat_picture(update, context):
        cat_list = glob('images/cat*.jp*g')
        cat_pic = choice(cat_list)
        context.bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'))

def change_avatar(update, context):
    if 'emo' in context.user_data:
        del context.user_data['emo']
    emo = get_user_emo(context.user_data)
    update.message.reply_text(f'Готово: {emo}')

def get_user_emo(user_data):
        if 'emo' in user_data:
                return user_data['emo']
        else:
                user_data['emo'] = emojize(choice(settings.USER_EMOJI), language='alias')
                return user_data['emo']

def main():
        mybot = Updater(settings.API_KEY, use_context=True)

        logging.info('Бот запускается')

        dp = mybot.dispatcher
        dp.add_handler(CommandHandler('start', greet_user))
        dp.add_handler(CommandHandler("planet", planet))
        dp.add_handler(CommandHandler('cat', send_cat_picture))
        dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture))
        dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar))
        dp.add_handler(MessageHandler(Filters.text, talk_to_me))


        mybot.start_polling()#ходить в telegram проверять сообщения
        mybot.idle()#работать бесконечно


main()
