from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
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

# Функция проверки объекта на картинки
def has_object_on_image(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)
    # Получаем файл в бинарном виде
    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)
    
    # Создаем объект запроса
    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        # Передаем свой файл
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])

    # Передаем данные на сервера Clarifai
    response = app.PostModelOutputs(request, metadata=metadata)
    #print(response)
    return check_responce_for_object(response, object_name)

# Функция пасинга результата Clarifai на успешность и результат
def check_responce_for_object(response, object_name):
    # Проверяем что status.code == SUCCESS
    if response.status.code == status_code_pb2.SUCCESS:
        # Проходим по полученым представлениям
        for concept in response.outputs[0].data.concepts:
            # Проверяем, что нейросеть уверена 
            if concept.name == object_name and concept.value >= 0.9:
                return True
    else:
        print(f"Ошибка распознавания: {response.outputs[0].status.details}")

    return False

if __name__ == "__main__":
    print(has_object_on_image('images/cat1.jpg', 'cat'))
    print(has_object_on_image('images/not_cat.jpg', 'dog'))