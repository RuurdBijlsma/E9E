import os

import commands
from server import Server
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from utils import copy_world

if __name__ == "__main__":
    copied = copy_world()
    if copied:
        Server.world_is_copied = True
    else:
        Server.copy_failed = True

    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    app.add_handler(CommandHandler("server", commands.manage_server))

    app.add_handler(CommandHandler("help", commands.show_help))
    app.run_polling(allowed_updates=Update.ALL_TYPES)
