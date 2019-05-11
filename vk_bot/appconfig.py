#!/usr/bin/env python
# coding: utf-8

import logging.config


token = '737ab1881a61171001a05d0127059d08f63f58d874f21672bdd9a1abdc91a6168472e6c32214713bb3219'
SECRET_PHRASE = "Я люблю ВК бота!"

# Конфигурация журналирования
LOGGING = {
    'version': 1,
    'formatters': {  # Форматирование сообщения
        'main': {
            'format': '[%(asctime)s] %(levelname)s %(module)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },

    'handlers': {  # Обработчикаи сообщений
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': '/tmp/trading.log',
            'formatter': 'main',
        },
        'streamlogger': {
            'class': 'logging.StreamHandler',
            'formatter': 'main',
        },
    },

    'loggers': {   # Логгеры
        'prod_logger': {
            'handlers': ['file_handler', 'streamlogger'],
            'level': 'INFO',
        },
        'devel_logger': {
            'handlers': ['file_handler', 'streamlogger'],
            'level': 'DEBUG',
        },
    },
}

logging.config.dictConfig(LOGGING)


# Базовая конфигурация
class Config(object):
    DEBUG = False
    LOGGER_NAME = 'devel_logger'


# Конфигурация выпуска
class ProductionConfig(Config):
    DEBUG = False
    LOGGER_NAME = 'prod_logger'


# Конфигурация разработки
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    LOGGER_NAME = 'devel_logger'


# Конфигурация тестирования
class TestConfig(Config):
    DEBUG = True
    TESTING = True
    LOGGER_NAME = 'devel_logger'

# Текущая конфигурация
# --------------------------------------------------
_currentConfig = DevelopmentConfig


def getConfig():
    return _currentConfig


def setConfig(config):
    global _currentConfig
    _currentConfig = config
# --------------------------------------------------