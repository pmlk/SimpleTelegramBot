import os
import sys
from bot.telegram_bot import TelegramBot, Config

if __name__ == "__main__":
    # directory = os.path.dirname(__file__)
    directory = os.getcwd()
    chat_id = Config.DEFAULT_CHAT_ID
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if len(sys.argv) > 2:
            chat_id = sys.argv[1]
    else:
        print("usage: ")
        print("sendFile <file_path> [chat_id>]")
        sys.exit("No file provided")

    if directory:
        file_path = os.path.join(directory, file_path)

    if not os.path.isfile(file_path):
        sys.exit("File " + file_path + " does not exist")

    myBot = TelegramBot(chat_id)
    myBot.send_file(file_path)
