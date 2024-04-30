import server
from telegram import Update
from telegram.ext import ContextTypes

HELP_MESSAGE = "Usage: /server aan | uit | status | output"


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_MESSAGE)


async def manage_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    msg_text = update.message.text
    split_msg = msg_text.split(" ")
    if len(split_msg) == 1:
        await update.message.reply_text(HELP_MESSAGE)
        return
    args = split_msg[1:]
    print(f"Receive <{user.first_name}>: {msg_text}")

    try:
        if args[0].startswith("/"):
            return await server.command(update, " ".join(args))

        match args:
            case ["aan"]:
                await server.aan(update)
            case ["uit"]:
                await server.uit(update)
            case ["status"]:
                await server.status(update)
            case ["output", lines_str]:
                await server.output(update, int(lines_str))
            case ["output"]:
                await server.output(update, 5)
            case _:
                await update.message.reply_text(HELP_MESSAGE)
    except Exception as e:
        print("ERROR! " + str(e))
