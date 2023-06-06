import logging
from glob import glob
import os
from random import choice
import ephem
import datetime

from utils import get_smile, play_ramdome_numbers, main_keyboard, has_object_on_image

# Функция приветствия пользователя при /start
def greet_user(update, context):
    print('Вызван /start')
    logging.info("Call /start")
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f'Hello user {context.user_data["emoji"]}! You called the command /start',
        reply_markup=main_keyboard()
        )

# Функция "эхо"
def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    logging.info(user_text)
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f'{user_text} {context.user_data["emoji"]}')

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
    update.message.reply_text(massage, reply_markup=main_keyboard())

# Функция отправки картинки при /cat
def send_cat_picture (update, context):
    print('Вызван /cat')
    # Список всех картинак
    cat_photos_list = glob('images/cat*.jp*g')
    # Выбор случайной картинки
    cat_pic_filename = choice(cat_photos_list)
    # Определяем чат пользователя
    chat_id = update.effective_chat.id
    # Функция оптравки картинки
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'), reply_markup=main_keyboard())

# Функция возвращающая координаты
def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    print(coords)
    massage = f"Ваши координаты {coords['latitude']} и {coords['longitude']}"
    update.message.reply_text(massage, reply_markup=main_keyboard())

# Функция вывода созвездия введеной планеты сейчас (ПЕРЕПИСАТЬ ПЛОД context.args???)
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

def check_user_photo(update, context):
    update.message.reply_text('Обрабатывем фото')
    # Создаем деректорию downloads, если ее еще нет
    os.makedirs('downloads', exist_ok=True)
    # Получаем файл из списка файлов
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    # Сохранием файл в созданой деректории
    file_name = os.path.join('downloads', f'{photo_file.file_id}.jpg')
    # Скачиваем файл из деректории
    photo_file.download(file_name)
    update.message.reply_text("Файл сохранен")
    if has_object_on_image(file_name, 'cat'):
        update.message.reply_text("Обноружен котик, сохраняю в библеотеку")
        new_filename = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        # Переменовываем и перемешаем картинку в папку
        os.rename(file_name, new_filename)
    else:
        # Удаляем файл
        os.remove(file_name)
        update.message.reply_text("Тревога, котик не обнаружен!")