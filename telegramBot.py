import urllib2, os, sys, requests, json

class TelegramBot(object):
    api_url = "https://api.telegram.org/bot"
    directory = os.path.dirname(__file__)

    def __init__(self, chat_id=None, botJson=None):
        self.chat_id = chat_id
        if botJson is None:
            botJson = "bot.json"
            botJson = os.path.join(self.directory, botJson)
        with open(botJson) as data_file:
            jsonBotData = json.load(data_file)

        jBot = jsonBotData["bot"]
        self.token = jBot["token"]
        self.name = jBot["name"]
        self.handle = jBot["handle"]
        if chat_id is None:
            self.chat_id = jBot["defaultChatId"]

    def setChatId(self, chat_id):
        self.chat_id = chat_id

    def sendMessage(self, msg):
        if self.chat_id is None:
            print "unable to send message, chat id not provided"
            return
        url = self.api_url + self.token + "/sendMessage?chat_id=" + str(self.chat_id) + "&text=" + msg
        print "url to send message: " + url
        urllib2.urlopen(url).read()

    def sendFile(self, pathToFile):
        if self.chat_id is None:
            print "unable to send file, chat id not provided"
            return
        url = self.api_url + self.token + "/sendDocument"
        files = {'document': open(pathToFile, 'rb')}
        data = {'chat_id': str(self.chat_id)}
        r = requests.post(url, files=files, data=data)
        print r.text
