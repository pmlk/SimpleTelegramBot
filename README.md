# Simple Telegram Bot
Designed for personal use, not interactive. Example: notify yourself when there are changes on a website.

## Setup Telegram Bot
1. register a Telegram bot, [follow the instructions]
(https://core.telegram.org/bots), keep your bot token safe
2. start a chat with your bot
3. find your personal `chat_id`, open `https://api.telegram.org/bot<bot_token>/getUpdates` in a browser or using `curl`:

```js
{
	"ok":true,
	"result":[
	{
		"update_id":59xxxxx05,
		"message":
		{
			"message_id":xxxx,
			"from":
			{
				"id":1xxxxxx4,
				"is_bot":false,
				"first_name":"John",
				"last_name":"Doe",
				"username":"jdoe",
				"language_code":"en-US"
			},
			"chat":
			{
---->			"id":1xxxxxx4,
				"first_name":"John",
				"last_name":"Doe",
				"username":"jdoe",
				"type":"private"
			},
			"date":1xxxxxxxx6,
			"text":"foo"
		}
	}]
}
```

## Installation using [`pipenv`](https://github.com/pypa/pipenv)

create a `.env` file with the follwing contents:

```
TELEGRAM_BOT_NAME=<your_bot_name>
TELEGRAM_BOT_TOKEN=<your_bots_secret_token>
TELEGRAM_BOT_HANDLE=@<handle>Bot
TELEGRAM_BOT_DEFAULT_CHAT_ID=<chat_id>
```

```bash
$ cd SimpleTelegramBot
$ pipenv install -e .
$ pipenv install
```

Note: On a RaspberryPi the creation of the virtual environment may take long enough to run into a timeout. To avoid this `export PIPENV_TIMEOUT=2400` before executing any `pipenv` commands.

## Usage Examples

### send yourself a message

```bash
$ pipenv shell
$ python3 utils/send_message.py "foo bar"
# or
$ pipenv run python3 utils/send_message.py "foo bar"
```

### send yourself a file

```bash
$ pipenv run python3 utils/send_file.py test.txt
```

### get notified about changes on websites

create a `urls.json` file containing websites you want to be notified about:

```js
{
  "URLs": [
    {
      "name": "Example",
      "URL": "https://www.example.com",
      "diffIgnore": ["<meta name=\"date\""]
    },
    {
      "name": "Google",
      "URL": "https://www.google.com",
      "diffIgnore": []
    }
  ]
}
```
Note the `diffIgnore` field. This can be used to ignore any changes that contain certain substrings. As in the example above, this can be useful for `<meta>` tags that may change with each request.

Periodically execute:

```bash
$ pipenv run python3 utils/url_notifier.py
```

**Cronjobs example**

```bash
$ crontab -e
# EDITOR
# ...
# execute every 15 minutes
*/15 * * * * bash -lc "cd /path/to/SimpleTelegramBot && /path/to/pipenv run python3 utils/url_notifier.py >> /path/to/SimpleTelegramBot/logs/log.txt 2>&1"
```
