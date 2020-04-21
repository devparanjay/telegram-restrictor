import os, sys, pickle, logging, csv, pandas

from csv import DictReader, DictWriter
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# enabling logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# This bot has 2 MODEs, Development(dev) and Production(prod).
# TOKEN here refers to the API Key you recieve from BotFather after creating a new Bot.
# use_context=True for better compatibility.

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
    # logger.info("User {} has started the bot.".format(update.effective_user["id"]))
    logger.info("User {} has started the bot.".format(update.effective_user.id))
    # context.bot.can_read_all_group_messages=True
    context.bot.send_message(chat_id = update.effective_chat.id, text="This Bot will immediately restrict users if they send more messages than they are allowed in a particular time-frame. Add this bot to the Group, give it the required permissions, and send /startir to get the Bot working in your Group.")
    # loading existing members

# def for loading members

members = {}

def load_members(update, context):
    members_load = open("members_list", "rb")
    members = pickle.load(members_load)
    members_load.close



# def for unknown commands

def unknown(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "That command is invalid. Please check it before sending it. Use /help to know what commands are available.")

# -------- DELAYING MESSAGES --------

# def for /setdelayir command

# delay_value = int

# def set_delay(update, context):
#     reply_keyboard = [["1","10","60","86400"]]

#     update.message.reply_text(
#         "Please choose the Delay value - ",
#         reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True))

#     return delay_value

# def for setting slow mode delay to del

# def delay(update, context):
#     update.slow_mode_delay=delay_value
#     context.bot.send_message(chat_id = update.effective_chat.id, text = "Message Delay for each unauthorized user now set to {}.".format(delay_value))

# def for deleting messages

# def delete(update, context):
    # context.bot.delete_message(update.effective_chat.id, timeout=None)

# --------------------------------------

# def for /register command


def register(update, context):
    # members.append(Filters.chat.usernames)
    member_data = {
        "user_id": update.effective_user.id,
        "username": update.effective_user.username,
        "first_name": update.effective_user.first_name,
        "last_name": update.effective_user.last_name,
        "name": update.effective_user.name
        }
    # members["username"] = member_data

    # pickling
    members_file = open("members_list", "wb")
    pickle.dump(members, members_file)
    members_file.close()

    # writing to csv
    def append_to_csv(filename, dict_elements, fields):
        with open(filename, 'a+', newline='') as editing:
            writing = DictWriter(editing, fieldnames=fields)
            writing.writerow(dict_elements)
    fields = ['user_id', 'username', 'first_name', 'last_name', 'name']
    append_to_csv('members.csv', member_data, fields)




# def for restricting members
def restrict(update, context):
    m_id = update.message.from_user.id
    option = ""

    reply_keyboard = [["Yes", "No"]]

    update.message.reply_text(
        "Start restricting?",
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True))

    return option

    if option == "Yes":
        context.bot.restrict_chat_member(chat_id = update.effective_chat.id, user_id = m_id, can_send_other_messages = True, timeout = 86400)
    else:
        update.message.reply_text("Okay, process cancelled.")

# ------------------------------

# def for testing members database - ERROR: 2020-04-21T20:16:16.827542+00:00 app[web.1]: update.message.reply_text(usernames, "->" ,members_test[usernames]) # object not subscriptable
#                                           2020-04-21T20:16:16.827542+00:00 app[web.1]: TypeError: '_io.BufferedReader' object is not subscriptable
# def test_members(update, context):
#     members_test = open("members_list", "rb")
#     for usernames in members_test:
#         update.message.reply_text(usernames, "->" ,members_test[usernames])
#     members_test.close

# ------------------------------

# def for testing members variable

def test_variable(update, context):
    for key, value in list(members.items())[1:]:
        update.message.reply_text(str(value))

# def for testing csv file
def test_csv(update, context):
    fields = ['user_id', 'username', 'first_name', 'last_name', 'name']
    csv_data = pandas.read_csv('members.csv', names=fields)
    csv_data = csv_data.drop_duplicates()
    uns = csv_data.username.tolist()
    update.message.reply_text(uns)


# Command Handlers

# set_delay_handler = CommandHandler("setdelayir", set_delay)
# delay_handler = CommandHandler("delayir", delay)
# restrict_handler = MessageHandler(Filters.text, restrict)
# test_members_handler = CommandHandler("testmembers", test_members)
start_handler = CommandHandler("startir", start)
yes_handler = CommandHandler("yesir", yes)
unknown_handler = MessageHandler(Filters.command,unknown)
register_handler = CommandHandler("register", register, pass_user_data=True, pass_chat_data=True)
test_variable_handler = CommandHandler("testvariable", test_variable)
load_members_handler = CommandHandler("loadmembers", load_members, pass_user_data=True)
test_csv_handler = CommandHandler("testcsv", test_csv)

# main def

def main():
    logger.info("Starting the Bot")

    # dispatcher.add_handler(yes_handler)
    # dispatcher.add_handler(set_delay_handler)
    # dispatcher.add_handler(delay_handler)
    # dispatcher.add_handler(test_members_handler)
    # dispatcher.add_handler(restrict_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(register_handler)
    dispatcher.add_handler(load_members_handler)
    dispatcher.add_handler(test_variable_handler)
    dispatcher.add_handler(test_csv_handler)

    run(updater)

# running the bot

if __name__ == '__main__':
    main()