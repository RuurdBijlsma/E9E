from server import Server
from telegram import Update
from telegram.ext import ContextTypes


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Usage: /server aan|uit|status")


async def manage_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    msg_text = update.message.text
    args = msg_text.split(" ")[1:]
    print(f"Receive <{user.first_name}>: {msg_text}")

    match args:
        case ["aan"]:
            await Server.server_aan(update)
        case ["uit"]:
            await Server.server_uit(update)
        case ["status"]:
            await Server.status(update)
        case _:
            await update.message.reply_text("WRONG")
