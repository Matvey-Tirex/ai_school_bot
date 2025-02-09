import requests
from env import *

def YandexrecognizeText(base64_photo):
  prompt = {
    "mimeType": "JPEG",
    "languageCodes": ["ru"],
    "model": "handwritten",
    "content": f"{base64_photo}"
  }

  url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_token_yandex}",
      "x-folder-id": f"{catalog_id_yandex}"
  }

  response = requests.post(url, headers=headers, json=prompt)
  print(response.json())
  return response.json()["result"]["textAnnotation"]["fullText"].replace("\n", " ")
  