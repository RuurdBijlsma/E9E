import asyncio
import subprocess
import sys

from telegram import Update


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
            ["./server-start.sh"], stdout=sys.stdout, stderr=sys.stderr
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
    async def kill(delay=0.3) -> bool:
        Server.process.terminate()
        await asyncio.sleep(delay)
        if Server.process.poll() is not None:
            # Terminated successfully
            Server.process = None
            return True
        Server.process.kill()
        await asyncio.sleep(delay)
        if Server.process.poll() is not None:
            # Killed successfully
            Server.process = None
            return True
        return False

    @staticmethod
    def is_aan():
        if Server.process is None:
            return False
        return Server.process.poll() is None
