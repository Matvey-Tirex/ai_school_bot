import telebot
import base64
import json
import os
import requests
from telebot.types import BotCommand
from telebot import types
from gpt import YandexcheckText
from vision import YandexrecognizeText
from env import api_token_telegram
# Импортируем наужные быблиотеки

type_check = 1
bot = telebot.TeleBot(api_token_telegram)
file_path = os.path.dirname(os.path.abspath(__file__))
# Создаём три переменые тип-провреки, bot и путь до расположения этого проекта

# Создаём handler на команду /start
@bot.message_handler(commands=["start"])
def start_text_bot(message):
    main_menu_commands = [
        BotCommand(command='/start', description='Запуск бота'),
        BotCommand(command='/check', description='Изменить тип проверки'),
        BotCommand(command='/tokens', description='Покажет ваши токены')
    ]
    bot.set_my_commands(main_menu_commands)
    # Далее создаём меню с команды для удобства
    bot.reply_to(message, "Привет! Я бот-ассистент.\nТы можешь отправить мне фотографию с рукописным текстом, и я проверю, есть ли в нем ошибки!\nВот команды, которые ты можешь использовать:\n/start - Запуск бота\n/check - Изменение типа проверки\n/tokens - Покажет сколько у вас осталось токенов")
    # Не забываем про этикет и расказать что это за бот

# Функция для чтобы показать сколько у вас осталось токенов
@bot.message_handler(commands=["tokens"])
def tokens(message):
    #Создаём переменную в которой будет списко пользавателей
    json_file_names = [filename for filename in os.listdir(file_path + "/json/users") if filename.endswith('.json')]
    if str(message.from_user.id) + ".json" not in json_file_names:
        # Дальше мы провери есть ли пользаватель в этом списке
        bot.send_message(message.chat.id, "Извините вы не зарегестрированы\nМы вас зарегестрируем и зачислем 5 токенов")
        data = {"status": "user", "username": message.from_user.username, "tokens": 5}
        with open(file_path + "/json/users/" + str(message.from_user.id) + ".json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            # Мы сказали что пользователь зарегестрируют его и начислят 5 токенов

    else:
        with open (file_path + "/json/users/" + str(message.from_user.id) + ".json", "r", encoding="utf-8") as file:
            data = json.load(file)
            if data["status"] == "admin":
                bot.send_message(message.chat.id, "У вас неограниченное количество токенов")
            else:
                bot.send_message(message.chat.id, "У вас осталось: " + str(data["tokens"]) +" токенов")
            # Проверили статус пользователя и выводим количество токенов

# Здесь мы создали функцию в которая настраивает тип проверки текста
@bot.message_handler(commands=["check"])
def func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Отправит исправленный текст с выделенными и исправленными словами")
    btn2 = types.KeyboardButton("Выделит слова с ошибками")
    btn3 = types.KeyboardButton("Отправит текст, выделит слова с ошибками и выделит темы для повторения")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, "Выберите тип проверки", reply_markup=markup)
    # Создали кнопки для выбора и выводим их

@bot.message_handler(content_types=["text"])
def hard(message):
    global type_check
    if message.text == "Отправит исправленный текст с выделенными и исправленными словами": 
        type_check = 0
        bot.send_message(message.chat.id, "*Тип проверки обновлён", reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "Выделит слова с ошибками": 
        type_check = 1
        bot.send_message(message.chat.id, "*Тип проверки обновлён", reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "Отправит текст, выделит слова с ошибками и выделит темы для повторения":
        type_check = 2
        bot.send_message(message.chat.id, "*Тип проверки обновлён", reply_markup=types.ReplyKeyboardRemove())
    # Меняем тип проверки от выбора пользавателья 

# В этой функцие мы принимаем фото, отдаём неиронке и забираем текст
@bot.message_handler(content_types=["photo"])
def start_media_bot(message):
    photo_file_id = message.photo[-1].file_id
    correct_message = check_text(photo_file_id)
    # После отдаеём следущей неиронке с типом проверки который мы выбрали
    json_file_names = [filename for filename in os.listdir(file_path + "/json/users") if filename.endswith('.json')]
    print(json_file_names)
    # Проверяем есть ли пользователь в базе данных(списке)
    if str(message.from_user.id) + ".json" not in json_file_names:
        # Если нету то добавляем
        try:
            with open(file_path + "/json/users/" + str(message.from_user.id), "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        data = {"status": "user", "username": message.from_user.username, "tokens": 5}
        with open(file_path + "/json/users/" + str(message.from_user.id) + ".json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
    with open (file_path + "/json/users/" + str(message.from_user.id) + ".json", "r", encoding="utf-8") as file:
        data = json.load(file)
        print(data)
        message.from_user.id = str(message.from_user.id)
        # Проверка статуса
        if data["status"] == "admin":
            print(data["tokens"])
            bot.reply_to(message, correct_message)
        elif data["status"] == "user":
            # Есть ли у пользователя токены на запрос
            if data["tokens"] > 0:
                data["tokens"] = data["tokens"] - 1
                print(data["tokens"])
                bot.reply_to(message, correct_message)
                # Под конец мы проверяем есть ли у пользователя ещё токены и отсылаем ответ
                with open(file_path + "/json/users/" + str(message.from_user.id) + ".json", "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                print(data)
            else:
                # Отсылаем ошибку на недостаток токенов если их нету
                bot.reply_to(message, "Извините, у вас недостаточно токенов")
            message.from_user.id = int(message.from_user.id)

def getBase64FromFileId(file_id):
    message = bot.get_file(file_id)
    file_in_bytes = bot.download_file(message.file_path)
    file_in_base64 = base64.b64encode(file_in_bytes).decode("utf-8")
    # Преаброзуем файл
    return(file_in_base64)

def check_text(file_id):
    # Принимаем фото на фход
    global type_check
    base64_message = getBase64FromFileId(file_id)
    # Преобразуем в base64
    text = YandexrecognizeText(base64_message)
    # Дальше пропускаем через неиронку для получения текста
    checked_text = YandexcheckText(text, type_check)
    # Под конец выдаёт ответ под выбраный тип проверки
    return checked_text

bot.polling(none_stop=True)