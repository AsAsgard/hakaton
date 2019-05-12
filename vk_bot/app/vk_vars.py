#!/usr/bin/env python
# coding: utf-8

import vk_api
from vk_api.longpoll import VkLongPoll
from appconfig import token

# авторизованные пользователи
authorized = set()

# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token)

# get api
vkapi = vk_session.get_api()

# Работа с сообщениями
longpoll = VkLongPoll(vk_a)

# загрузчик
upload = vk_api.VkUpload(vk_a)
