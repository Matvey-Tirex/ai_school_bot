import requests
from env import *

def YandexcheckText(text):

    prompt = {
        "modelUri": f"gpt://{catalog_id_yandex}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты умный ассистент по руссому языку. В тексте, заключенном в теге <text></text>, найди все орфографические, пунктуационные и грамматические ошибки. В ответе напиши только места, где были ошибки. Если пропущена запятая, напиши где. Исправленный текст писать не надо в ответе.  Формат ответа MarkDown. Тег <text> в ответе не применяй"
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