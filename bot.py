# Импортируем нужные компоненты
import logging
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
from random import randint, choice
from glob import glob
from emoji import emojize

# Конфигурация логов
logging.basicConfig(filename='bot.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO,
                    encoding='utf-8')

# Настройки прокси (неактуально)
"""
PROXY = {'proxy_url': settings.PROXY_URL',
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}
"""
# Функция получения смайлика
def get_smile(user_data):
    if 'emoji' not in user_data:
        # Выбор случайного смайлика
        smile = choice(settings.USER_EMOJI)
        # Получение нужного смайлика
        return emojize(smile)
    return user_data['emoji']

# Функция "эхо"
def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    logging.info(user_text)
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f'{user_text} {context.user_data["emoji"]}')

# Функция приветствия пользователя при /start
def greet_user(update, context):
    print('Вызван /start')
    logging.info("Call /start")
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f'Hello user {context.user_data["emoji"]}! You called the command /start')

# Функция вывода созвездия введеной планеты сейчас (ПЕРЕПИСАТЬ ПЛОД context.args)
def get_planet(update, context):
    try:
        print('Вызван /planet')
        user_message = update.message.text.split()
        #Получаем now из библиотеки datetime, возможно в переменной context есть дата
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        #Вытаскиваем название планеты из сообщения
        user_planet = user_message[1].capitalize()
        logging.info(f"Call /planet {user_planet}")
        #Присваиваем переменную name planet в атрибут
        ephem_name_planet = getattr(ephem, user_planet)
        #Получить координаты планеты
        planet = ephem_name_planet(now)
        #Запрос созвездия
        constellation = (ephem.constellation(planet))[1]
        update.message.reply_text(f'{user_planet} in the constellation {constellation}')
    except AttributeError:
        update.message.reply_text(f'Check planet name')

# Функция генерации рандомного числа и сравнение с пользовательским
def play_ramdome_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        massage = f"Ваше число {user_number}, мое число {bot_number}, вы выйграли!"
    elif user_number == bot_number:
        massage = f"Ваше число {user_number}, мое число {bot_number}, ничья!"
    else:
        massage = f"Ваше число {user_number}, мое число {bot_number}, вы проиграли!"
    return massage

# Функция игры с пользователем при /guess
def guess_number(update, context):
    print (context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            massage = play_ramdome_numbers(user_number)
        except (TypeError, ValueError):
            massage = 'Введите целое число'
    else:
        massage = 'Введите число'
    update.message.reply_text(massage)   

# Функция отправки картинки при /cat
def send_cat_picture (update, context):
    # Список всех картинак
    cat_photos_list = glob('images/cat*.jp*g')
    # Выбор случайной картинки
    cat_pic_filename = choice(cat_photos_list)
    # Определяем чат пользователя
    chat_id = update.effective_chat.id
    # Функция оптравки картинки
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'))

# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)
    
    # Обработчики
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", get_planet))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot start")
    # Командуем боту начать ходить в Telegram за сообщениями
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()

# Вызываем функцию main() - именно эта строчка запускает бота
if __name__ == "__main__":
    main()