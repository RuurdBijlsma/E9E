import asyncio
import signal
import subprocess
import sys

from telegram import Update
from utils import check_java_processes, kill_java_processes


class Server:
    process: subprocess.Popen | None = None

    @staticmethod
    async def status(update: Update) -> None:
        if Server.is_aan():
            await update.message.reply_text("De server is aan")
        else:
            await update.message.reply_text("De server is uit")

    @staticmethod
    async def server_aan(update: Update) -> None:
        if Server.is_aan():
            await update.message.reply_text("Server is al aan!")
            return

        Server.process = subprocess.Popen(
            ["/server/start-server.sh"],
            cwd="/server/",
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

        await update.message.reply_text("De server gaat aan")

    @staticmethod
    async def server_uit(update: Update) -> None:
        if not Server.is_aan():
            await update.message.reply_text("Server is al uit!")
            return

        killed = await Server.kill()
        if killed:
            await update.message.reply_text("Server is dood gemaakt!")
        else:
            await update.message.reply_text("Het is niet select de server te doden :(")

    @staticmethod
    async def kill(kill_timeout=5) -> bool:
        Server.process.terminate()
        kill_java_processes()
        waited = 0
        while True:
            if not Server.is_aan():
                return True
            await asyncio.sleep(0.05)
            waited += 0.05
            if waited >= kill_timeout:
                return False

    @staticmethod
    def is_aan():
        if Server.process is None:
            return False
        return Server.process.poll() is None and check_java_processes()
