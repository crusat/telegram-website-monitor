import telegram
from settings import TELEGRAM_API_KEY
from data import Website
import requests


bot = telegram.Bot(token=TELEGRAM_API_KEY)

websites = (Website.select())

for website in websites:
    url = website.url
    try:
        r = requests.head(url)
        status_code = r.status_code
    except:
        status_code = 0
    if status_code != website.last_status_code:
        website.last_status_code = status_code
        website.save()
        bot.sendMessage(chat_id=website.chat_id,
                        text="Status code changed for %s. Current is %s." % (website.url, status_code))