import os, sys
from telegramBot import TelegramBot

directory = os.path.dirname(__file__)
chat_id = None
if len(sys.argv) > 1:
    filepath = sys.argv[1]
    if len(sys.argv) > 2:
        chat_id = sys.argv[1]
else:
    print "usage: "
    print "sendFile <filepath> [chat_id>]"
    sys.exit("No file provided")

if directory:
    filepath = os.path.join(directory, filepath)

if not os.path.isfile(filepath):
    sys.exit("File " + filepath + " does not exist")

myBot = TelegramBot(chat_id)
myBot.sendFile(filepath)
