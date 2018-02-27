import os
import urllib3
import requests


class Config(object):
    BOT_NAME = os.environ["TELEGRAM_BOT_NAME"]
    BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
    BOT_HANDLE = os.environ["TELEGRAM_BOT_HANDLE"]
    DEFAULT_CHAT_ID = os.environ["TELEGRAM_BOT_DEFAULT_CHAT_ID"]


class TelegramBot(object):
    api_url = "https://api.telegram.org/bot"

    def __init__(self, chat_id=Config.DEFAULT_CHAT_ID):
        self.chat_id = chat_id or Config.DEFAULT_CHAT_ID
        self.token = Config.BOT_TOKEN
        self.name = Config.BOT_NAME
        self.handle = Config.BOT_HANDLE

    def send_message(self, msg):
        url = "{}{}/sendMessage?chat_id={}&text={}".format(self.api_url, self.token, str(self.chat_id), msg)
        print("url to send message: {}".format(url))
        http = urllib3.PoolManager()
        r = http.request("GET", url)
        # urllib3.urlopen(url).read()

    def send_file(self, path_to_file):
        url = "{}{}/sendDocument".format(self.api_url, self.token)
        files = {'document': open(path_to_file, 'rb')}
        data = {'chat_id': str(self.chat_id)}
        r = requests.post(url, files=files, data=data)
        print(r.text)
