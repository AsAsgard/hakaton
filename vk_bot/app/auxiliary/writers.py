#!/usr/bin/env python
# coding: utf-8

import sys
from datetime import datetime
from app.logger import Logger
from random import randint
from app.vk_vars import vk_a


def write_msg(user_id, message):
    vk_a.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randint(-sys.maxsize -1, sys.maxsize)})


def successLog():
    Logger.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")};Success')


def failLog():
    Logger.info(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")};Fail')
