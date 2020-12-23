import logging

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, RegexHandler

from handlers import *
import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log'
                    )

def main():
    mybot = Updater(settings.API_KEY, use_context=True);
    logging.info('Бот запустился.')

    dp = mybot.dispatcher

    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(News)$'), get_news, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(More)$'), get_news, pass_user_data=True))

    # Start
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
