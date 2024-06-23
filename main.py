import logging
from telegram import Update, BotCommand
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from telegram.error import BadRequest
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = open("./token.txt")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am the glorious leader of Persia.')
    # args = chat_id={update.message.chat_id}, {SOMETHING}={TO_SEND}
    # update.message.reply_{SOMETHING}({args}) -> To reply "SOMETHING" to the sent message
    # context.bot.send_{SOMETHING}({args}) -> To send "SOMETHING"
    # update.message.delete() -> To delete the message that was sent.
    
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Click on the \"Slash\" button to see the commands available ☆ Also the bot reacts so some messages.")

def kick_user(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user_to_kick = update.message.reply_to_message.from_user.id
        chat_id = update.message.chat_id
        try:
            context.bot.kick_chat_member(chat_id, user_to_kick)
            update.message.reply_text(f'User {user_to_kick} has been kicked.')
        except BadRequest as e:
            update.message.reply_text(f'Error: {e}')
    else:
        update.message.reply_text('Please reply to the user you want to kick.')

def ban_user(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user_to_ban = update.message.reply_to_message.from_user.id
        chat_id = update.message.chat_id
        try:
            context.bot.ban_chat_member(chat_id, user_to_ban)
            update.message.reply_text(f'User {user_to_ban} has been banned.')
        except BadRequest as e:
            update.message.reply_text(f'Error: {e}')
    else:
        update.message.reply_text('Please reply to the user you want to ban.')

def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    target_words = {
        "china": "Don't say that word ever again!",
        "🇨🇳": "AntiChina triggered!",
        "soviet": "Long Live Soviet!! Союз нерушимый республик свободных - Сплотила навеки Великая Русь - Да здравствует созданный волей народов - Единый, могучий Советский Союз!",
        "☠️": "I also agree! ☠️",
        "hey cyrus": "Yes commando?",
        "hi cyrus": "Hello soldier! Wanna be recruited as a higher rank position? .... Jk",
        "hello cyrus": "Hello soldier! How was the training?",
        "good": "That's good to hear! Glad thats true.",
        "bad":"Oh no soldier! Medical Group (Helpers Group)!!! help him asap!"
    }
    triggers = target_words.keys()
    found = False
    found_word = ""
    for tri in triggers:
        if tri in text.lower():
            found = True
            found_word = tri
            break
    if found:
        update.message.reply_text(target_words[found_word])

def poll(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    context.bot.send_poll(chat_id=chat_id, question="The modern government of Iran is ****y, right?", options=["Yes", "No"], allows_multiple_answers=False)

def sendpic(update: Update, context:CallbackContext) -> None:
    pic_id = content.args[0]
    
    picid_pics = {
        "1": "1.png",
        "2": "2.png"
    }
    
    try:
        path = picid_pics[str(pic_id)]
    
        pic = open(path, "rb").read()
        update.message.reply_picture(chat_id=update.message.chat_id,  picture=pic)
    except:
        update.message.reply_text(f"Please provide a valid picture id /n {picid_pics.keys()}")

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("kick", kick_user))
    dispatcher.add_handler(CommandHandler("ban", ban_user))
    dispatcher.add_handler(CommandHandler("askpoll", poll))
    dispatcher.add_handler(CommandHandler("sendpic", sendpic))

    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
