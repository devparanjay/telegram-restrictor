import logging
import os
import sys

from telegram.ext import Updater, CommandHandler

# enabling logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# This bot has 2 MODEs, Development and Production.
# TOKEN here refers to the API Key you recieve from BotFather after creating a new Bot.

mode = os.getenv("MODE")
token = os.getenv("TOKEN")

# bot functions

if mode == "dev":
    def run(Updater):
        Updater.start_polling()
elif mode == "prod":
    def run(Updater):
        PORT = int(os.environ.get("PORT", "8779"))
        app_name = os.environ.get("app_name")
        Updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=token)
        Updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(app_name, token))
else:
    logger.error("No MODE specified.")
    sys.exit(1)

# def for /start command

def start_handler(bot, update):
    logger.info("User {} has started the bot.".format(update.efective_user["id"]))
    update.message.reply_text("This Bot will immediately delete the messages from users if they send more messages than they are allowed in a particular time-frame."
    "Add this bot to the Group, give it the required permissions, and send /ainzsama to get the Bot working in your Group. The settings can be configured in this chat with /config command.")

#def for /config command