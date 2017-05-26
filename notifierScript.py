import json, os, sys
from urlNotifier import UrlNotifier
from telegramBot import TelegramBot

chat_id = None
directory = os.path.dirname(__file__)
relJsonFile = "notifyURLs.json"
if len(sys.argv) > 1:
    #assume json file provided
    testJsonFile = sys.argv[1]
    if not os.path.isfile(testJsonFile):
        #if file doesn't exist, assume it's chat id
        child_id = testJsonFile

if len(sys.argv) > 2:
    chat_id = sys.argv[2]

jsonFile = os.path.join(directory, relJsonFile)

with open(jsonFile) as data_file:
    jsonUrlData = json.load(data_file)

jUrls = jsonUrlData["URLs"]
notifiers = []
for jUrl in jUrls:
    notifiers.append(UrlNotifier(jUrl))

for notifier in notifiers:
    notifier.sing()
    notifier.update()
    tgMsg = notifier.getMessage()

    if tgMsg:
        print "Will send Telegram Message: " + tgMsg
        myBot = TelegramBot(chat_id)
        myBot.sendMessage(tgMsg)
    else:
        print "Nothing new on page: " + notifier.name
