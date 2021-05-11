import telebot

from config import config_dict


bot = telebot.TeleBot(config_dict["BOT_TOKEN"],
                      parse_mode="markdown", threaded=False, skip_pending=True)

from bot.callbacks import *
from bot.commands import *
from bot.text import *
