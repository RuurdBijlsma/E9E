import os

import commands
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    app.add_handler(CommandHandler("server", commands.manage_server))

    app.add_handler(CommandHandler("help", commands.show_help))
    app.run_polling(allowed_updates=Update.ALL_TYPES)
