#!/usr/bin/env python
import validators

bad_url_text = "Bad url. Please use next format: http://example.com"


def required_argument(fn):
    def wrapper(bot, update, args):
        if int(len(args)) == 0:
            bot.sendMessage(chat_id=update.message.chat_id, text=bad_url_text)
            return False
        return fn(bot, update, args)
    return wrapper


def valid_url(fn):
    def wrapper(bot, update, args):
        if not validators.url(args[0], public=True):
            bot.sendMessage(chat_id=update.message.chat_id, text=bad_url_text)
            return False
        return fn(bot, update, args)
    return wrapper
