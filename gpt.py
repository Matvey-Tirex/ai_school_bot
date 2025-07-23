import requests
from env import *

def YandexcheckText(text, type_check):
    #"Ты умный ассистент по руссому языку. В тексте, заключенном в теге <text></text>, найди все орфографические, пунктуационные и грамматические ошибки. В ответе напиши слова, где были ошибки и их верный вариант. Если пропущена запятая, напиши где. Исправленный текст писать не надо в ответе.  Формат ответа MarkDown. Тег <text> в ответе не применяй"
    variants = ["Ты умный ассистент по руссому языку. В тексте, заключенном в теге <text></text>, найди все орфографические, пунктуационные и грамматические ошибки и отправь исправленый текс. Формат ответа MarkDown. Тег <text> в ответе не применяй", "Ты умный ассистент по руссому языку. В тексте, заключенном в теге <text></text>, найди все орфографические, пунктуационные и грамматические ошибки. В ответе напиши слова, где были ошибки и их верный вариант. Если пропущена запятая, напиши где. Исправленный текст писать не надо в ответе.В тексте иногда упущено тере не забывай. Формат ответа MarkDown. Тег <text> в ответе не применяй", "Ты умный ассистент по руссому языку. В тексте, заключенном в теге <text></text>, найди все орфографические, пунктуационные и грамматические ошибки и отправь исправленый текс. В ответе напиши слова, где были ошибки и их верный вариант. Если пропущена запятая, напиши где.Напиши правила которые надо повторить и к какому класу они относятся. Формат ответа MarkDown. Тег <text> в ответе не применяй"]
    prompt = {
        "modelUri": f"gpt://{catalog_id_yandex}/yandexgpt/rc",
        "completionOptions": {
            "stream": False,
            "temperature": 0,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": variants[type_check]
            },
            {
                "role": "user",
                "text": f"проверь текст:<text>{text}</text>"
            }
        ]
    }


    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token_yandex}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()["result"]["alternatives"][0]["message"]["text"]
    print(result)
    return result