import yandex_music, vk_api

YANDEX_LOGIN = 'YANDEX_LOGIN'
YANDEX_PASSWORD = 'YANDEX_PASSWORD'

VK_LOGIN = 'VK_LOGIN'
VK_PASSWORD = 'VK_PASSWORD'

if __name__ == '__main__':

    # авторизируемся в сервисах
    ya_client = yandex_music.Client().from_credentials(username=YANDEX_LOGIN, password=YANDEX_PASSWORD)
    vk = vk_api.VkApi(login=VK_LOGIN, password=VK_PASSWORD, app_id=6121396)
    vk.auth()

    # получаем информацию о треках из ВК
    user_id = vk.token.get('user_id')
    vk_response = vk.method("audio.get", {"count": 1, "owner_id": user_id})

    audio_count = vk_response.get('count', 0)
    if audio_count == 0:
        print('нет аудиозаписей')
        exit(1)
    vk_response = vk.method("audio.get", {"count": audio_count, "owner_id": user_id})

    # ищем и лайкаем треки в Яндекс.Музыка
    for track in vk_response['items']:
        track_text = ' - '.join([track.get('artist', 'None'), track.get('title', 'None')])
        search_result = ya_client.search(text=track_text)

        if search_result is not None:
            try:
                track = search_result.best.result
                is_like = ya_client.users_likes_tracks_add(track_ids=[track.track_id])
                try:
                    artist = track.artists[0].name
                except IndexError:
                    artist = 'Неизвестный исполнитель'

                if is_like:
                    print('лайкнули трек {} - {}'.format(artist, track.title))
                else:
                    print('трек {} - {} уже лайкнут'.format(artist, track.title))
            except AttributeError:
                print('не нашли {}'.format(track_text))
                continue
        else:
            print('не нашли {}'.format(track_text))
