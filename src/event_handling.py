from datetime import datetime

import aiosqlite
import discord
from discord.ext import commands


class EventHandling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):  # leveling
        if message.author.bot:
            return
        self.bot.db: aiosqlite.Connection
        async with self.bot.db.execute(
            "SELECT * FROM leveling WHERE user_id = ?", (message.author.id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                await self.bot.db.execute(
                    "INSERT INTO leveling (user_id, xp, level, last_level_update) VALUES (?, ?, ?, ?)",
                    (message.author.id, 0, 1, datetime.now()),
                )
                await self.bot.db.commit()
                return
            if row["level"] <= 10:
                xp = row["xp"] + 100
            elif row["level"] <= 20:
                xp = row["xp"] + 90
            elif row["level"] <= 30:
                xp = row["xp"] + 80
            elif row["level"] <= 40:
                xp = row["xp"] + 70
            elif row["level"] <= 50:
                xp = row["xp"] + 60
            elif row["level"] <= 60:
                xp = row["xp"] + 50
            else:
                xp = row["xp"] + 40
            level_count = xp // 1000
            print(level_count, row["level"])
            if level_count > row["level"]:
                await self.bot.db.execute(
                    "UPDATE leveling SET xp = ?, level = ?, last_level_update = ? WHERE user_id = ?",
                    (xp % 1000, level_count, datetime.now(), message.author.id),
                )
                await self.bot.db.commit()
                await message.channel.send(
                    f"{message.author.mention} has leveled up to level {level_count}!"
                )
            else:
                await self.bot.db.execute(
                    "UPDATE leveling SET xp = ? WHERE user_id = ?",
                    (xp % 1000, message.author.id),
                )
                await self.bot.db.commit()
