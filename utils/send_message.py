from bot.telegram_bot import TelegramBot

if __name__ == "__main__":
    import sys
    bot = TelegramBot()

    if len(sys.argv) > 1:
        msg = ""
        for m in sys.argv[1:]:
            msg += "{} ".format(m)

        bot.send_message(msg)
