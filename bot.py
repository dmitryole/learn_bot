# Импортируем нужные компоненты
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(filename='bot.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO,encoding='utf-8')

# Настройки прокси (неактуально)
"""
PROXY = {'proxy_url': settings.PROXY_URL',
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}
"""

def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    logging.info(user_text)
    update.message.reply_text(user_text)

def greet_user(update, context):
    print('Вызван /start')
    logging.info("Call /start")
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot start")
    # Командуем боту начать ходить в Telegram за сообщениями
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()

# Вызываем функцию main() - именно эта строчка запускает бота
if __name__ == "__main__":
    main()