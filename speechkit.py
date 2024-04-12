import requests
import os
from dotenv import load_dotenv

load_dotenv()


# Функция генерация голосовых сообщений по тексту
async def text_to_speech(text):
    headers = {
        'Authorization': f'Bearer {os.getenv('iam_token')}',
    }
    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'filipp',
        'folderId': os.getenv('folder_id'),
    }
    response = requests.post(os.getenv('URL'), headers=headers, data=data)
    if response.status_code == 200:
        result = response.content
        with open(os.getenv('file'), 'wb') as f:
            f.write(result)
        return result
    else:
        result1 = "При запросе в SpeechKit возникла ошибка"
        return result1
