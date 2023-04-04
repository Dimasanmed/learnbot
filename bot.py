# Импортируем нужные компоненты
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import ephem
from datetime import date


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log',
                    encoding='utf-8'
                    )

def planet(update, context):
        planet_name = str(update.message.text.split(" ")[1]).lower().capitalize()
        day = date.today()
        planet = getattr(ephem, planet_name)(day)
        const = ephem.constellation(planet)
        answer = f"На сегодняшнию дату {day} планета {planet_name} находится в созвездии {const}"
        update.message.reply_text(answer)


def greet_user(update, context):
        text = 'Вызван /start'
        logging.info(text)
        update.message.reply_text(text)

def talk_to_me(update, context):
        user_text = "Привет {}! Ты написал: {}".format(update.message.chat.first_name, update.message.text)
        logging.info("User: %s,Chat id: %s, Message: %s", update.message.chat.first_name,
                     update.message.chat.id, update.message.text)
        update.message.reply_text(user_text)


def main():
        mybot = Updater(settings.API_KEY)

        logging.info('Бот запускается')

        dp = mybot.dispatcher
        dp.add_handler(CommandHandler('start', greet_user))
        dp.add_handler(CommandHandler("planet", planet))
        dp.add_handler(MessageHandler(Filters.text, talk_to_me))


        mybot.start_polling()#ходить в telegram проверять сообщения
        mybot.idle()#работать бесконечно


main()
