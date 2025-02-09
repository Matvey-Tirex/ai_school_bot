import telebot
import base64
from gpt import YandexcheckText
from vision import YandexrecognizeText
from env import api_token_telegram

bot = telebot.TeleBot(api_token_telegram)

@bot.message_handler(content_types=["photo"])
def start_media_bot(message):
    photo_file_id = message.photo[-1].file_id
    correct_message = check_text(photo_file_id)
    bot.reply_to(message, correct_message)

@bot.message_handler(content_types=["text"])
def start_text_bot(message):
    bot.reply_to(message, "Привет! Я бот!")


def getBase64FromFileId(file_id):
    message = bot.get_file(file_id)
    file_in_bytes = bot.download_file(message.file_path)
    file_in_base64 = base64.b64encode(file_in_bytes).decode("utf-8")
    return(file_in_base64)

def check_text(file_id):
    base64_message = getBase64FromFileId(file_id)
    text = YandexrecognizeText(base64_message)
    checked_text = YandexcheckText(text)
    return checked_text

bot.polling(none_stop=True)