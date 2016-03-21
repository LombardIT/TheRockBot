# @TheRockBot


Hello! This is the code used by [@therockbot](https://telegram.me/therockbot), through Telegram's Bot API. You can easily run your own @therockbot! Read this small tutorial.

----------

## Installing @therockbot

What you need:
 
 - Python, Pip and Git. 
 - Clone this repository.
 - `pip install -r requirements.txt`. 
 - A Bot API Token.
 - `cp settings.ini.sample settings.ini`, edit `settings.ini` with the bot's token.
 - Run `cd db/` and then `python createdb.py`.

----------

## Running the bot
 Running the bot: simplest way is with [`forever`](https://github.com/foreverjs/forever). Install `forever` through `npm` and then run `forever -e err.log -o out.log start -c python bot.py`.