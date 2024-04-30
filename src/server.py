import asyncio
import pathlib
import subprocess
import sys
from asyncio import StreamReader

from telegram import Update
from utils import is_server_on, kill_server

test = False
WORKING_DIRECTORY = "/server"
if test:
    SERVER_SCRIPT = "/server/test-script.sh"
else:
    SERVER_SCRIPT = "/server/start-server.sh"


class Server:
    process: subprocess.Popen | None = None
    world_is_copied: bool = False
    copy_failed = False
    stdout_lines: list[str] = []
    players: set[str] = set()


async def status(update: Update) -> None:
    if is_server_on():
        online_gamers = (
            ", ".join(Server.players) if len(Server.players) > 0 else "NIEMAND"
        )
        await update.message.reply_text(
            "De server is aan, online spelers: " + online_gamers
        )
    else:
        await update.message.reply_text("De server is uit")


async def output(update: Update, lines: int) -> None:
    if not is_server_on():
        await update.message.reply_text("Server is niet aan, dus er is geen output!")
        return

    await update.message.reply_text(
        f"Laatste {min(len(Server.stdout_lines), lines)} regels output:\n```log\n"
        + "".join(Server.stdout_lines[-lines:])
        + "\n```",
        parse_mode="MarkdownV2",
    )


async def command(update: Update, cmd: str) -> None:
    if not is_server_on():
        await update.message.reply_text(
            "Server is niet aan, dan kan je geen commands sturen!"
        )
        return

    stdout_lines_len = len(Server.stdout_lines)
    Server.process.stdin.write(str.encode(cmd + "\n"))
    await asyncio.sleep(0.2)
    await update.message.reply_text(
        "Command ontvangen ✅\n```log\n"
        + "".join(Server.stdout_lines[stdout_lines_len:])
        + "\n```",
        parse_mode="MarkdownV2",
    )


async def buffer_lines(std_piped: StreamReader | None, update: Update):
    async for line in std_piped:
        line_str = line.decode("utf-8")
        print(line_str, end="")
        Server.stdout_lines.append(line_str)
        if "Sending reload packet to clients" in line_str:
            await update.message.reply_text(
                "De server is gereed, spelers kunnen er in."
            )
        if " joined the game" in line_str and "[minecraft/MinecraftServer]" in line_str:
            player = line_str.split(" joined the game")[0].split(" ")[-1]
            Server.players.add(player)
        if " left the game" in line_str and "[minecraft/MinecraftServer]" in line_str:
            player = line_str.split(" left the game")[0].split(" ")[-1]
            Server.players.remove(player)


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

    pathlib.Path(SERVER_SCRIPT).chmod(0o777)
    Server.process = await asyncio.create_subprocess_exec(
        SERVER_SCRIPT,
        cwd=WORKING_DIRECTORY,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        stdin=subprocess.PIPE,
    )

    _ = asyncio.create_task(buffer_lines(Server.process.stdout, update))

    await update.message.reply_text("De server gaat aan")


async def uit(update: Update) -> None:
    if not is_server_on():
        await update.message.reply_text("Server is al uit!")
        return

    killed = await kill_server(Server.process)
    if killed:
        await update.message.reply_text("Server is dood gemaakt!")
        Server.players = set()
    else:
        await update.message.reply_text("Het is niet gelukt de server te doden :(")
