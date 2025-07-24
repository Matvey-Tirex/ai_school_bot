# Импортируем нужные библиотеки
import telebot
import base64
from telebot.types import BotCommand
from telebot import types
from gpt import YandexcheckText
from vision import YandexrecognizeText
from env import api_token_telegram
from users import *

# Создать две переменные тип-проверки и бот
type_check = 1
bot = telebot.TeleBot(api_token_telegram)

# Создаём handler на команду /start
@bot.message_handler(commands=["start"])
def start_text_bot(message):
    # Далее создаём меню с команды для удобства
    main_menu_commands = [
        BotCommand(command='/start', description='Запуск бота'),
        BotCommand(command='/check', description='Изменить тип проверки'),
        BotCommand(command='/tokens', description='Покажет ваши токены')
    ]
    bot.set_my_commands(main_menu_commands)
    # Не забываем про этикет и рассказать что это за бот
    bot.reply_to(message, "Привет! Я бот-ассистент.\nТы можешь отправить мне фотографию с рукописным текстом, и я проверю, есть ли в нем ошибки!\nВот команды, которые ты можешь использовать:\n/start - Запуск бота\n/check - Изменение типа проверки\n/tokens - Покажет сколько у вас осталось токенов")

# Функция для чтобы показать сколько у вас осталось токенов
@bot.message_handler(commands=["tokens"])
def check_tokens(message):
    if check_tokens(message, bot) != "":
        bot.send_message(message.chat.id, check_tokens(message, bot))

# Здесь мы создали функцию в которая настраивает тип проверки текста
@bot.message_handler(commands=["check"])
def func(message):
    # Создаём кнопки для выбора ..
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Отправит исправленный текст с выделенными и исправленными словами")
    btn2 = types.KeyboardButton("Выделит слова с ошибками")
    btn3 = types.KeyboardButton("Отправит текст, выделит слова с ошибками и выделит темы для повторения")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    # .. и выводим их
    bot.send_message(message.chat.id, "Выберите тип проверки", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def hard(message):
    # Меняем тип проверки от выбора пользователя
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

# В этой функцией мы принимаем фото, отдаём нейронке и забираем текст
@bot.message_handler(content_types=["photo"])
def start_media_bot(message):
    photo_file_id = message.photo[-1].file_id
    # После отдаем следующей нейронке с типом проверки который мы выбрали
    correct_message = check_text(photo_file_id)
    # Проверяем есть ли пользователь базе данных 
    init_account(message, bot)
    # Проверяем есть ли токены у пользователя
    # И заодно вычитаем с аккаунта запрос
    if use_token(message.from_user.ids) == True:
        bot.reply_to(message, correct_message)
    else:
        bot.reply_to(message, "Извините, у вас недостаточно токенов")

# Преобразуем файл
def getBase64FromFileId(file_id):
    message = bot.get_file(file_id)
    file_in_bytes = bot.download_file(message.file_path)
    file_in_base64 = base64.b64encode(file_in_bytes).decode("utf-8")
    return(file_in_base64)

# Принимаем фото на вход
def check_text(file_id):
    global type_check
    # Преобразуем в base64
    base64_message = getBase64FromFileId(file_id)
    # Дальше пропускаем через нейронку для получения текста
    text = YandexrecognizeText(base64_message)
    # Под конец выдаёт ответ под выбранный тип проверки
    checked_text = YandexcheckText(text, type_check)
    return checked_text

bot.polling(none_stop=True)