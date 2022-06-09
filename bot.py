import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

load_dotenv()
import os
import subprocess

import aiosqlite

bot = commands.Bot("b!", intents=discord.Intents.all())

logging.getLogger("discord").setLevel(logging.WARNING)  # shut up discord

formatting = logging.Formatter("[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s")

logging.basicConfig(
    level=logging.NOTSET,
    format="[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

observer = Observer()


def get_version():
    is_updated = subprocess.check_output("git status", shell=True).decode("ascii")

    if "modified" in is_updated:
        is_updated = None
    elif (
        "up to date" in is_updated
        or "nothing to commit, working tree clean" in is_updated
    ):
        is_updated = True
    else:
        is_updated = False

    if is_updated:
        bot.version_ = f"latest ({get_git_revision_short_hash()})"
    elif is_updated is None:
        bot.version_ = f"{get_git_revision_short_hash()} (modified)"
    else:
        bot.version_ = f"old ({get_git_revision_short_hash()}) - not up to date"


class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        log.info(f"File changed: {event.src_path}")
        if event.src_path.endswith(".py"):
            log.info("Reloading...")
            path = event.src_path.replace("\\", "/").replace("/", ".")[:-3]
            try:
                asyncio.run(bot.reload_extension(path))
                log.info(f"Reloaded {path}")
            except Exception as e:
                log.error(f"Failed to reload {path}")
                log.error(e)
                log.error(traceback.format_exc())


observer.schedule(FileHandler(), path="src", recursive=False)

log = logging.getLogger("BeachBot")
log.setLevel(logging.NOTSET)

try:
    os.mkdir("logs")
except FileExistsError:
    pass
with open("logs/bot.log", "w") as f:
    f.write("")
f = logging.FileHandler("logs/bot.log")
f.setFormatter(formatting)
log.addHandler(f)


@bot.event
async def on_ready():
    log.info("BeachBot is ready!")
    log.info(f"Logged in as {bot.user.name} ({bot.user.id})")
    log.info(f"Version: {bot.version_}")
    log.info(f"Discord.py version: {discord.__version__}")
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Game(name="b!"))
    observer.start()
    await bot.tree.sync()


async def start():
    async with bot:
        await bot.load_extension("src")
        log.info("Loaded extensions")
        bot.db = await aiosqlite.connect("db.sqlite")
        await bot.db.execute(open("src/utils/sql/starter.sql", "r").read())
        await bot.db.commit()
        log.info("Database created")
        await bot.start(os.getenv("BEACH_TOKEN"))
