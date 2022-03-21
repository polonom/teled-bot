from mongodb import mdb, search_or_save_user, save_user_vote
from utils import print_gist, get_gists, get_keyboard, Point
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler


def sms(bot, update):
    user = search_or_save_user(mdb, bot.effective_user, bot.message)
    print(str(user['first_name'])+' '+str(user['last_name']))
    #print('Кто-то отправил команду /start. Что мне делать?')
    bot.message.reply_text('Здравствуйте, {}!'.format(bot.message.chat.first_name),
                           reply_markup=get_keyboard())

def parrot(bot, update):
    #print(bot.message.text)
    bot.message.reply_text('Напишите /start, чтобы начать')

def hist_what(bot, update):
    bot.message.reply_text("Добро пожаловать в бот для оценки похожести двух фигур!"
                           "\nКогда вы нажмете голосовать, вам нужно будет выбрать один из вариантов ответа:"
                           "\nПохожи, Не Похожи или Не Знаю."
                           "\nСтарайтесь избегать ответа Не знаю"
                           "\nДля сравнения обращайте внимание на количество пиков"
                           "\nи их взаимное расположение. "
                           ""
                           "",
                           reply_markup=get_keyboard())

def hist_begin_vote(bot, update):
    list_of_hists = get_gists()
    picture = print_gist(list_of_hists)
    update.bot.send_photo(chat_id=bot.message.chat.id, photo=picture)
    if 'hist1' not in update.user_data:
        update.user_data.update({'hist1': []})
    if 'hist2' not in update.user_data:
        update.user_data.update({'hist2': []})
    if 'Sim' not in update.user_data:
        update.user_data.update({'Sim': []})
    if 'NonSim' not in update.user_data:
        update.user_data.update({'NonSim': []})
    if 'Dont Know' not in update.user_data:
        update.user_data.update({'Dont Know': []})
    if 'Date' not in update.user_data:
        update.user_data.update({'Date': []})
    if 'Time' not in update.user_data:
        update.user_data.update({'Time': []})

    update.user_data['hist1'].append("{}_{}".format(list_of_hists[0], list_of_hists[1]))
    update.user_data['hist2'].append("{}_{}".format(list_of_hists[2], list_of_hists[3]))
    update.user_data['Sim'].append(0)
    update.user_data['NonSim'].append(0)
    update.user_data['Dont Know'].append(0)

    reply_keyboard = [["Похожи", "Не похожи"], ["Не знаю,\nно этого ответа нужно избегать"]]
    bot.message.reply_text('Эти фигуры похожи?',
                           reply_markup=ReplyKeyboardMarkup(
                               reply_keyboard, resize_keyboard=False, one_time_keyboard=True))

    temple = bot.message.date#2021-04-18T18:27:12.000+00:00
    temple = temple.timetuple()
    year = str(temple[0])
    month = str(temple[1])
    day = str(temple[2])
    hour = str(temple[3]+3)
    minute = str(temple[4])
    second = str(temple[5])
    update.user_data['Date'].append(year+'-'+month+'-'+day)
    update.user_data['Time'].append(hour+':'+minute+':'+second)
    return "answer"

def hist_get_answer(bot, update):
    if bot.message.text == "Похожи":
        update.user_data['Sim'][-1] = 1
    elif bot.message.text == "Не похожи":
        update.user_data['NonSim'][-1] = 1
    else:
        update.user_data['Dont Know'][-1] = 1
    user = search_or_save_user(mdb, bot.effective_user, bot.message)
    vote_result = save_user_vote(mdb, user, update.user_data)
    #print(vote_result)
    update.user_data.update({'hist1': [], 'hist2': [], 'Sim': [], 'NonSim': [], 'Dont Know': [], 'Date': [], 'Time': []})
    reply_keyboard = [['Голосовать!', "Закончить"]]
    bot.message.reply_text('Помогите нам собрать больше результатов!'
                           '\nНажмите Голосовать!',
                           reply_markup=ReplyKeyboardMarkup(
                                        reply_keyboard, resize_keyboard=False,  one_time_keyboard=True))
    return "end?"

def hist_end(bot, update):
    bot.message.reply_text("Спасибо вам за помощь в сборе данных!", reply_markup=get_keyboard())
    return ConversationHandler.END

def dontknow(bot, update):
    bot.message.reply_text("Я вас не понимаю")