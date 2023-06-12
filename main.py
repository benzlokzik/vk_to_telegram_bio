import time
import vk_api

from telethon import functions
from telethon.sync import TelegramClient

from dotenv import load_dotenv
import os


def get_track_from_vk(vk_access_token, vk_user_id):
    vk_session = vk_api.VkApi(token=vk_access_token)
    vk = vk_session.get_api()
    response = vk.status.get(user_id=vk_user_id)
    if 'text' in response and response['text']:
        return response['text']
    return None


def update_status(_current_playing, track, api_id, api_hash, default_status):
    if track:
        music_status = "🎧 VK Музыка | " + track

        if _current_playing != track:
            with TelegramClient('anon', api_id, api_hash) as client:
                client(functions.account.UpdateProfileRequest(about=music_status))
            print(f"🆗 Установил статус: «{music_status}»")

        return track

    if _current_playing is not None:
        with TelegramClient('anon', api_id, api_hash) as client:
            client(functions.account.UpdateProfileRequest(about=default_status))
        print(f"🆗 Установил статус: «{default_status}»")
        time.sleep(10)

    return None


def main():
    # Загружаю токены из переменных окружения
    load_dotenv(dotenv_path=".env")
    VK_USER_ID = os.getenv("VK_USER_ID")
    VK_ACCESS_TOKEN = os.getenv("VK_ACCESS_TOKEN")
    DEFAULT_STATUS = os.getenv("STATUS")
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    current_playing = ''

    print('🚀 Запускаем...')
    while True:
        try:
            time.sleep(5)
            current_track = get_track_from_vk(VK_ACCESS_TOKEN, VK_USER_ID)
            current_playing = update_status(current_playing, current_track, API_ID, API_HASH, DEFAULT_STATUS)
        except Exception as e:
            print(f'⚡ Ошибка: {str(e)}')


if __name__ == '__main__':
    main()
