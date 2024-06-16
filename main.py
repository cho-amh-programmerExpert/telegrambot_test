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

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '7101527978:AAF2Z0ayxQb8g6oDeDurXMsB0ekTggQAjfE'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello my friend!')
    # args = chat_id={update.message.chat_id}, {SOMETHING}={TO_SEND}
    # update.message.reply_{SOMETHING}({args}) -> To reply "SOMETHING" to the sent message
    # context.bot.send_{SOMETHING}({args}) -> To send "SOMETHING"

def help(update:Update, context: CallbackContext):
    context.bot.send_message(text="/send_cyrus >>> To send the picture of cyrus the grreat!", chat_id=update.message.chat_id)

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
    if "cyrus" in text.lower():
        update.message.reply_text("Good to know that you're talking about me.")
    
    if "china" in text.lower():
        update.message.delete()
        context.bot.send_message(chat_id=update.message.chat_id, text="NEVER SAY THE WORD 'CHINA' AGAIN!")

def send_file(update: Update, context: CallbackContext) -> None:

    chat_id = update.message.chat_id
    try:
        with open("ctg.jpg", 'rb') as f:
            update.message.reply_photo(chat_id=chat_id)

    except FileNotFoundError:
        update.message.reply_text('File not found.')
    except Exception as e:
        update.message.reply_text(f'Error: {e}')

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("kick", kick_user))
    dispatcher.add_handler(CommandHandler("ban", ban_user))
    dispatcher.add_handler(CommandHandler("sendcyrus", send_file))
    dispatcher.add_handler(CommandHandler("help", help))

    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
