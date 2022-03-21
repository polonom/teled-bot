from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
from settings import TG_TOKEN
from handlers import *
import logging

'''logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )
                    '''

def main():
    my_bot = Updater(TG_TOKEN)
    logging.info('Start bot')

    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Как сравнивать?'), hist_what))
    my_bot.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('Голосовать!'), hist_begin_vote)],
            states={
                        "answer": [MessageHandler(Filters.regex("Похожи|Не похожи|Не знаю,\nно этого ответа нужно избегать"), hist_get_answer)],
                        "end?": [MessageHandler(Filters.regex("Закончить"), hist_end)],
                    },
            fallbacks=[MessageHandler(
                                Filters.text | Filters.video | Filters.photo | Filters.document, dontknow)],
            allow_reentry=True)
        )

    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()
    my_bot.idle()

if __name__=="__main__":
    main()