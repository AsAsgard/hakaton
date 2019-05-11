#!/usr/bin/env python
# coding: utf-8

import sys
import vk_api
import bs4
import requests
import annoy
import pandas as pd
from ml_functions.predict import process_data
from threading import Timer
from datetime import datetime
from app.logger import Logger
from appconfig import token, SECRET_PHRASE
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint

authorized = set()
success = 0
fail = 0

annoy_model = annoy.AnnoyIndex(300)
annoy_model.load('annoy')

df = pd.read_csv('ProductsDataset.csv')

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# api
api = vk.get_api()

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randint(1, sys.maxsize)})


def successLog():
    Logger.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")};Success')


def failLog():
    Logger.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")};Fail')


def _clean_all_tag_from_str(string_line):

    """
    Очистка строки stringLine от тэгов и их содержимых
    :param string_line: Очищаемая строка
    :return: очищенная строка
    """

    result = ""
    not_skip = True
    for i in list(string_line):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True

    return result


def get_user_name_from_vk_id(user_id):
    request = requests.get("https://vk.com/id" + str(user_id))
    bs = bs4.BeautifulSoup(request.text, "html.parser")

    user_name = _clean_all_tag_from_str(bs.findAll("title")[0])

    return user_name.split()[0]


def process():
    # Основной цикл

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

            result = process_data(event.text, annoy_model, df)
            if not result:
                write_msg(event.user_id,
                          f"Я не могу понять, что ты мне хочешь сказать, {get_user_name_from_vk_id(event.user_id)}!")
                failLog()
                continue
            else:
                message = f"Вот что я смог найти для тебя, {get_user_name_from_vk_id(event.user_id)}:\n"
                for element in result:
                    message = "".join([message,
                                       f"Название: {element.get('title')}; "
                                       f"Индекс продукта: {element.get('product_id')}; "
                                       f"Ссылка на картинку:{element.get('image') if element.get('image') else ''}"])
                write_msg(event.user_id, message)
                successLog()
                continue
