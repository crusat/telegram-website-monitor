from telegram.ext import Updater, CommandHandler
from settings import TELEGRAM_API_KEY
from data import Website
import requests
import validators


help_text = """
/help - This help.
/list - Show yours added urls.
/add <url> - Add new url for monitoring.
/del <url> - Remove exist url.
/test <url> - Test current status code for url right now.

Url format is http[s]://host.zone/path?querystring
For example: https://crusat.ru

For any issues: https://github.com/crusat/telegram-website-monitor/issues
"""


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello!\nThis is telegram bot to check that the site is alive.\n%s" % help_text)


def show_help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="%s" % help_text)


def add(bot, update, args):
    url = args[0]
    if not validators.url(url, public=True):
        bot.sendMessage(chat_id=update.message.chat_id, text="Bad url")
        return False
    website_count = (Website.select().where((Website.chat_id == update.message.chat_id) & (Website.url == url)).count())
    if website_count == 0:
        website = Website(chat_id=update.message.chat_id, url=url)
        website.save()
        bot.sendMessage(chat_id=update.message.chat_id, text="Added %s" % url)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Website %s already exists" % url)


def delete(bot, update, args):
    url = args[0]
    if not validators.url(url, public=True):
        bot.sendMessage(chat_id=update.message.chat_id, text="Bad url")
        return False
    website = Website.get((Website.chat_id == update.message.chat_id) & (Website.url == url))
    if website:
        website.delete_instance()
        bot.sendMessage(chat_id=update.message.chat_id, text="Deleted %s" % url)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Website %s is not exists" % url)


def url_list(bot, update):
    websites = (Website.select().where(Website.chat_id == update.message.chat_id))
    out = ''
    for website in websites:
        out += "%s (last status code: %s)\n" % (website.url, website.last_status_code)
    if out == '':
        bot.sendMessage(chat_id=update.message.chat_id, text="List empty")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="%s" % out)


def test(bot, update, args):
    url = args[0]
    if not validators.url(url, public=True):
        bot.sendMessage(chat_id=update.message.chat_id, text="Bad url")
        return False
    try:
        r = requests.head(url)
        if r.status_code == 200:
            bot.sendMessage(chat_id=update.message.chat_id, text="Url %s is alive (status code 200)" % url)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Status code of url %s is %s" % (url, r.status_code))
    except:
        bot.sendMessage(chat_id=update.message.chat_id, text="Error for url %s" % url)



updater = Updater(TELEGRAM_API_KEY)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler("add", add, pass_args=True))
updater.dispatcher.add_handler(CommandHandler("del", delete, pass_args=True))
updater.dispatcher.add_handler(CommandHandler("list", url_list))
updater.dispatcher.add_handler(CommandHandler("test", test, pass_args=True))
updater.dispatcher.add_handler(CommandHandler("help", show_help))

print('Telegram bot started')

updater.start_polling()
updater.idle()