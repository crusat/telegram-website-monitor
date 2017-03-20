import telegram
from settings import TELEGRAM_API_KEY
from data import Website
import requests


bot = telegram.Bot(token=TELEGRAM_API_KEY)

websites = (Website.select())

for website in websites:
    url = website.url
    r = requests.head(url)
    if r.status_code != website.last_status_code:
        website.last_status_code = r.status_code
        website.save()
        bot.sendMessage(chat_id=website.chat_id, text="Status code changed for %s. Current is %s." % (website.url, r.status_code))
