import os
import errno
import sys
import json
import time
import urllib.parse
import urllib3
import difflib
from pprint import pprint

from bot.telegram_bot import TelegramBot, Config

urllib3.disable_warnings()


class UrlNotifier(object):
    # directory = os.path.dirname(__file__)
    directory = os.path.dirname(__file__)
    root_dir = os.path.dirname(directory + "/../")
    data_dir = os.path.dirname(root_dir + "/data/")

    if not os.path.isdir(data_dir):
        try:
            os.makedirs(data_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    tmpFileSuffix = "_tmp.html"

    def __init__(self, json_object):
        self.url = json_object["URL"]
        self.name = json_object["name"]
        ignores = []
        for ign in json_object["diffIgnore"]:
            ignores.append(str(ign))

        self.diffIgnore = ignores
        self.message = ""

    def get_notification_message(self):
        self.download()
        filtered_diffs = self.get_filtered_diffs()

        # diffs = self.getDiffs()
        # print "unfiltered diffs: "
        # pprint(diffs)

        msg = None
        if len(filtered_diffs) > 0:
            print("filtered diffs: ")
            pprint(filtered_diffs)
            msg = self.create_message()

        self.swap_tmp()
        return msg

    def download(self):
        filename = self.get_filename()
        tmp_filename = self.get_tmp_filename()
        if not os.path.isfile(filename):
            print("{} does NOT exist".format(filename))
            with open(filename, "w+") as f:
                f.write("new file\r\n")

        http = urllib3.PoolManager()
        r = http.request("GET", self.url)
        new_content = str(r.data)
        with open(tmp_filename, "w+") as f_tmp:
            f_tmp.write(new_content)

    def create_message(self):
        msg = "There are changes in {}\nCheck out:\n{}".format(self.name, self.url)
        return urllib.parse.quote(msg)

    def sing(self):
        print("url: {}".format(self.url))
        print("name: {}".format(self.name))
        print("diffIgnore: {}".format(self.diffIgnore))

    def get_filtered_diffs(self):
        unfiltered_diffs = self.get_diffs()
        diffs = []
        for diff in unfiltered_diffs:
            if not any(x in diff for x in self.diffIgnore):
                diffs.append(diff)
        return diffs

    def get_diffs(self):
        file1 = self.get_filename()
        file2 = self.get_tmp_filename()
        f1_lines = self.get_lines(file1)
        f2_lines = self.get_lines(file2)

        d = difflib.Differ()
        result = list(d.compare(f1_lines, f2_lines))

        diff = []
        for res in result:
            if res[0] == "+" or res[0] == "-":  # only care about changes (= lines starting with + or -)
                diff.append(res)
        return diff

    def get_filename(self):
        return os.path.join(self.data_dir, self.name + ".html")

    def get_tmp_filename(self):
        return os.path.join(self.data_dir, self.name + self.tmpFileSuffix)

    def get_lines(self, filename):
        return self.get_clean_contents(filename).splitlines()

    def swap_tmp(self):
        os.remove(self.get_filename())
        os.rename(self.get_tmp_filename(), self.get_filename())

    def get_clean_contents(self, filename):
        with open(filename) as f:
            clean_contents = f.read().replace('<', '\n<')
        return clean_contents


if __name__ == "__main__":

    print(time.strftime("%Y/%m/%d %H:%M:%S"))

    chat_id = Config.DEFAULT_CHAT_ID
    data_dir = os.path.dirname(__file__)
    url_json_filename = "urls.json"
    if len(sys.argv) > 1:
        # assume json file provided
        testJsonFile = sys.argv[1]
        if not os.path.isfile(testJsonFile):
            # if file doesn't exist, assume it's chat id
            child_id = testJsonFile

    if len(sys.argv) > 2:
        chat_id = sys.argv[2]

    url_json_file_path = os.path.join(UrlNotifier.root_dir, url_json_filename)

    with open(url_json_file_path) as data_file:
        json_url_data = json.load(data_file)

    jUrls = json_url_data["URLs"]
    notifiers = []
    for jUrl in jUrls:
        notifiers.append(UrlNotifier(jUrl))

    for notifier in notifiers:
        # notifier.sing()
        tg_msg = notifier.get_notification_message()
        if tg_msg:
            print("Will send Telegram Message: {}".format(tg_msg))
            myBot = TelegramBot(chat_id)
            myBot.send_message(tg_msg)
        else:
            print("Nothing new on page: {}".format(notifier.name))

    print("=====================")
    print()
