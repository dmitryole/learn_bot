import settings
from emoji import emojize
from random import randint, choice
from telegram import ReplyKeyboardMarkup, KeyboardButton

# Функция получения смайлика
def get_smile(user_data):
    if 'emoji' not in user_data:
        # Выбор случайного смайлика
        smile = choice(settings.USER_EMOJI)
        # Получение нужного смайлика
        return emojize(smile)
    return user_data['emoji']

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

# Функция возврашения клавиатуры при ответе бота
def main_keyboard():
    return ReplyKeyboardMarkup([['Прислать котика', KeyboardButton('Мои координаты', request_location=True)]])