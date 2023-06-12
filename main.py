import time
import vk_api

from telethon import functions
from telethon.sync import TelegramClient

import bd

api_id = bd.api_id
api_hash = bd.api_hash
default_status = bd.status
current_playing = ''


def get_track_from_vk():
    vk_session = vk_api.VkApi(token=bd.vk_access_token)
    vk = vk_session.get_api()
    response = vk.status.get(user_id=bd.vk_user_id)
    if 'text' in response and response['text']:
        return response['text']
    return None


def update_status(_current_playing):
    track = get_track_from_vk()

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


if __name__ == '__main__':
    print('🚀 Запускаем...')
    while True:
        try:
            time.sleep(5)
            current_playing = update_status(current_playing)
        except Exception as e:
            print(f'⚡ Ошибка: {str(e)}')
