import subprocess
import sys

from telegram import Update
from utils import is_server_on, kill_server


class Server:
    process: subprocess.Popen | None = None
    world_is_copied: bool = False
    copy_failed = False


async def status(update: Update) -> None:
    if is_server_on():
        await update.message.reply_text("De server is aan")
    else:
        await update.message.reply_text("De server is uit")


async def aan(update: Update) -> None:
    if Server.copy_failed:
        await update.message.reply_text("The world folder failed to copy!")
        return

    if not Server.world_is_copied:
        await update.message.reply_text("The world folder hasn't been copied yet!")
        return

    if is_server_on():
        await update.message.reply_text("Server is al aan!")
        return

    Server.process = subprocess.Popen(
        ["/server/start-server.sh"],
        cwd="/server/",
        stdout=sys.stdout,
        stderr=sys.stderr,
    )

    await update.message.reply_text("De server gaat aan")


async def uit(update: Update) -> None:
    if not is_server_on():
        await update.message.reply_text("Server is al uit!")
        return

    killed = await kill_server(Server.process)
    if killed:
        await update.message.reply_text("Server is dood gemaakt!")
    else:
        await update.message.reply_text("Het is niet gelukt de server te doden :(")
