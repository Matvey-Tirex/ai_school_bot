import telebot
import base64
from telebot import types
from gpt import YandexcheckText
from vision import YandexrecognizeText
from env import api_token_telegram

type_check = 1
bot = telebot.TeleBot(api_token_telegram)

@bot.message_handler(content_types=["photo"])
def start_media_bot(message):
    photo_file_id = message.photo[-1].file_id
    correct_message = check_text(photo_file_id)
    bot.reply_to(message, correct_message)

@bot.message_handler(commands=["start"])
def start_text_bot(message):
    bot.reply_to(message, "Привет! Я бот-ассистент по русскому языку. Ты можешь отправить мне фото с рукописным текстом, а в ответе я напишу есть ли в нем ошибки!")

@bot.message_handler(commands=["check"])
def func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Отправит исправленый текс")
    btn2 = types.KeyboardButton("Выделит слова с ошибками")
    btn3 = types.KeyboardButton("Отправит исправленый текс ,выделит слова с ошибками и выделит темы для повторения")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    bot.send_message(message.chat.id, "выберете проверку", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def hard(message):
    global type_check
    if message.text == "Отправит исправленый текс": type_check = 0
    elif message.text == "Отправит слова с ошибками": type_check = 1
    elif message.text == "Отправит исправленый текс ,выделит слова с ошибками и выделит темы для повторения": type_check = 2

def getBase64FromFileId(file_id):
    message = bot.get_file(file_id)
    file_in_bytes = bot.download_file(message.file_path)
    file_in_base64 = base64.b64encode(file_in_bytes).decode("utf-8")
    return(file_in_base64)

def check_text(file_id):
    global type_check
    base64_message = getBase64FromFileId(file_id)
    text = YandexrecognizeText(base64_message)
    checked_text = YandexcheckText(text, type_check)
    return checked_text

bot.polling(none_stop=True)