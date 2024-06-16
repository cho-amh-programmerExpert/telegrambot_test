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
TOKEN = '7361646280:AAF3rYMroas79FCxJcDiLTNGP7DjZzPvvxo'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot.')
    # update.message.reply_{SOMETHING}() -> To reply "SOMETHING" to the sent message
    # context.bot.send_{SOMETHING}() -> To send "SOMETHING"

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')

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
        user_to_ban = context.args[0]
        #user_to_ban = update.message.reply_to_message.from_user.id
        chat_id = update.message.chat_id
        try:
            # context.bot.ban_chat_member(chat_id, user_to_ban)
            context.bot.banChatMember(chat_id, user_to_ban)
            update.message.reply_text(f'User {user_to_ban} has been banned.')
        except BadRequest as e:
            update.message.reply_text(f'Error: {e}')
    else:
        update.message.reply_text('Please reply to the user you want to ban.')

def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    update.message.reply_text(f'your msg')

def send_file(update: Update, context: CallbackContext) -> None:
    if context.args:
        file_path = context.args[0] # Selecting the first parameter passed to the function
        chat_id = update.message.chat_id
        try:
            with open(file_path, 'rb') as f:
                context.bot.send_document(document=f, chat_id=chat_id)

        except FileNotFoundError:
            update.message.reply_text('File not found.')
        except Exception as e:
            update.message.reply_text(f'Error: {e}')
    else:
        update.message.reply_text('Please provide a file path.')

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("kick", kick_user))
    dispatcher.add_handler(CommandHandler("ban", ban_user))
    dispatcher.add_handler(CommandHandler("sendfile", send_file))

    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
