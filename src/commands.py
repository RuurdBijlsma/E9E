import server
from telegram import Update
from telegram.ext import ContextTypes

HELP_MESSAGE = "Usage: /server aan|uit|status"


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_MESSAGE)


async def manage_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    msg_text = update.message.text
    args = msg_text.split(" ")[1:]
    print(f"Receive <{user.first_name}>: {msg_text}")

    match args:
        case ["aan"]:
            await server.aan(update)
        case ["uit"]:
            await server.uit(update)
        case ["status"]:
            await server.status(update)
        case _:
            await update.message.reply_text(HELP_MESSAGE)
