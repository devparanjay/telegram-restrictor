import os, sys, pickle, logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# enabling logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# This bot has 2 MODEs, Development(dev) and Production(prod).
# TOKEN here refers to the API Key you recieve from BotFather after creating a new Bot.

mode = os.getenv("MODE")
token = os.getenv("TOKEN")
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher

# bot functions for dev and prod

if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8779"))
        app_name = os.environ.get("app_name")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=token)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(app_name, token))
else:
    logger.error("No MODE specified.")
    sys.exit(1)

# members = Filters.user.user_ids
# members.append()

# def for /yesir command

def yes(update, context):
    update.message.reply_text("This Bot will immediately delete the messages from users if they send more messages than they are allowed in a particular time-frame. Add this bot to the Group, give it the required permissions, and send /ainzsama to get the Bot working in your Group. The settings can be configured in this chat with /config command.")

# def for /startir command

def start(update, context):
    logger.info("User {} has started the bot.".format(update.effective_user["id"]))
    context.bot.send_message(chat_id = update.effective_chat.id, text="This Bot will immediately delete the messages from users if they send more messages than they are allowed in a particular time-frame. Add this bot to the Group, give it the required permissions, and send /ainzsama to get the Bot working in your Group. The settings can be configured in this chat with /config command.")

# def for unknown commands

def unknown(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "That command is invalid. Please check it before sending it. Use /help to know what commands are available.")

# def for /setdelayir command

delay_value = int

def set_delay(update, context):
    reply_keyboard = [["1","10","60","86400"]]
    
    update.message.reply_text(
        "Please choose the Delay value - ",
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True))
    
    return delay_value

# def for setting slow mode delay to del

def delay(update, context):
    update.slow_mode_delay=delay_value
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Message Delay for each unauthorized user now set to {}.".format(delay_value))

# def for deleting messages

# def delete(update, context):
    # context.bot.delete_message(update.effective_chat.id, timeout=None)

# def for /register command

members = []

def register(update, context):
    members.append(Filters.chat.usernames)
    members_file = open("members_list", "wb")
    pickle.dump(members, members_file)
    members_file.close()

# Command Handlers

start_handler = CommandHandler("startir", start)
unknown_handler = MessageHandler(Filters.command,unknown)
set_delay_handler = CommandHandler("setdelayir", set_delay)
delay_handler = CommandHandler("delayir", delay)
register_handler = CommandHandler("register", register, pass_user_data=True, pass_chat_data=True)

# running the bot

if __name__ == '__main__':

    logger.info("Starting the Bot")

    # loading members
    members_file = open("members_list", "rb")
    members = pickle.load(members_file)
    members_file.close()

    # dispatcher.add_handler(CommandHandler("yes", yes))
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(set_delay_handler)
    dispatcher.add_handler(delay_handler)
    dispatcher.add_handler(register_handler)

    run(updater)