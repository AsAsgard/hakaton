#!/usr/bin/env python
# coding: utf-8

from ml_functions.predict import process_data
from appconfig import SECRET_PHRASE
from vk_api.longpoll import VkEventType
from app.auxiliary.writers import successLog, failLog, write_msg
from app.auxiliary.parser import get_user_name_from_vk_id
from app.vk_vars import vk_a, upload, authorized, longpoll, vk_got_api
from random import randint
import sys
import requests


def process():
    # Основной цикл
    print("Bot started to handle requests")

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

            if event.text == SECRET_PHRASE and not event.user_id in authorized:
                authorized.add(event.user_id)
                write_msg(event.user_id, f"Привет, {get_user_name_from_vk_id(event.user_id)}! Рады тебя видеть!")
                successLog()
                continue
            elif event.text == SECRET_PHRASE:
                write_msg(event.user_id, f"Мы уже общаемся, {get_user_name_from_vk_id(event.user_id)}!")
                successLog()
                continue
            if not event.user_id in authorized:
                failLog()
                continue

            try:
                result = process_data(event.text)
            except KeyboardInterrupt:
                raise
            except:
                write_msg(event.user_id,
                          f"Прости, у меня не получилось найти для тебя подходящий ответ, "
                          f"{get_user_name_from_vk_id(event.user_id)}((")
                failLog()
                continue
            if not result:
                write_msg(event.user_id,
                          f"Извини, я не смог найти для тебя что-то подходящее, "
                          f"{get_user_name_from_vk_id(event.user_id)}((")
                failLog()
                continue
            else:
                write_msg(event.user_id, f"Вот что я смог найти для тебя, {get_user_name_from_vk_id(event.user_id)}:")
                for element in result:
                    message = f"Название: {element.get('title')}; \n"\
                              f"Индекс продукта: {element.get('product_id')}; \n"
                    if element.get('image'):
                        image = requests.get(element.get('image'), stream=True)
                        photo = upload.photo_messages(photos=image.raw)[0]
                        attachment = f"photo{photo['owner_id']}_{photo['id']}"
                        vk_got_api.messages.send(
                            user_id=event.user_id,
                            attachment=attachment,
                            message=message,
                            random_id=randint(-sys.maxsize -1, sys.maxsize)
                        )
                    else:
                        vk_got_api.messages.send(
                            user_id=event.user_id,
                            message=message,
                            random_id=randint(-sys.maxsize - 1, sys.maxsize)
                        )
                successLog()
                continue
