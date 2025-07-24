import json
import os

file_path = os.path.dirname(os.path.abspath(__file__))
json_file_names = [filename for filename in os.listdir(file_path + "/json/users") if filename.endswith('.json')]

def tokens(message, bot):
    #Создаём переменную в которой будет списко пользавателей
    json_file_names = [filename for filename in os.listdir(file_path + "/json/users") if filename.endswith('.json')]
    if str(message.from_user.id) + ".json" not in json_file_names:
        check_account(message, bot)
    else:
        with open (file_path + "/json/users/" + str(message.from_user.id) + ".json", "r", encoding="utf-8") as file:
            data = json.load(file)
            # Проверили статус пользователя и выводим количество токенов
            if data["status"] == "admin":
                return("У вас неограниченное количество токенов")
            else:
                return("У вас осталось: " + str(data["tokens"]) +" токенов")

def check_account(message, bot):
    # Создаём новго пользователя
    if str(message.from_user.id) + ".json" not in json_file_names:
        # Говорим пользователю что ему завичислено 5 токенов и создаём фаил с информацией
        bot.send_message(message.chat.id, "Извините вы не зарегестрированы\nМы вас зарегестрируем и зачислем 5 токенов")
        data = {"status": "user", "username": message.from_user.username, "tokens": 5}
        with open(file_path + "/json/users/" + str(message.from_user.id) + ".json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    
def take_token(message):
    with open (file_path + "/json/users/" + str(message.from_user.id) + ".json", "r", encoding="utf-8") as file:
        data = json.load(file)
        print(data)
        message.from_user.id = str(message.from_user.id)
        # Проверка статуса
        if data["status"] == "admin":
            print(data["tokens"])
            return True
        elif data["status"] == "user":
            # Под конец мы проверяем есть ли у пользователя ещё токены и отсылаем true или false
            if data["tokens"] > 0:
                data["tokens"] = data["tokens"] - 1
                print(data["tokens"])
                with open(file_path + "/json/users/" + str(message.from_user.id) + ".json", "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                return True
            else:
                return False