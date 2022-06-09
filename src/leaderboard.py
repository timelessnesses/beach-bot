import discord
from discord.ext import commands


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def me(self, ctx: commands.Context):
        """Displays your current level and XP."""
        self.bot.db: aiosqlite.Connection
        async with self.bot.db.execute(
            "SELECT * FROM leveling WHERE user_id = ?", (ctx.author.id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row is None:
                await self.bot.db.execute(
                    "INSERT INTO leveling (user_id, xp, level, last_level_update) VALUES (?, ?, ?, ?)",
                    (ctx.author.id, 0, 1, datetime.now()),
                )
                await self.bot.db.commit()
                await ctx.send(
                    embed=discord.Embed(
                        title=f"{ctx.author.name}'s Leveling",
                        description=f"Level: 1\nXP: 0",
                    )
                )
                return
            async with self.bot.db.execute(
                "SELECT * FROM leveling ORDER BY xp DESC LIMIT ?", (amount,)
            ) as cursor:
                rows = await cursor.fetchall()
                for i, row in enumerate(rows):
                    if row["user_id"] == ctx.author.id:
                        await ctx.send(
                            embed=discord.Embed(
                                title=f"{ctx.author.name}'s Leveling",
                                description=f"Level: {row['level']}\nXP: {row['xp']}\nRank: {self.prefix(i + 1)}",
                            )
                        )
                        return

    def prefix(self, n: int):
        return str(n) + (
            "th"
            if 4 <= n % 100 <= 20
            else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        )

    @commands.hybrid_command()
    async def top(self, ctx: commands.Context, *, amount: int = 10):
        """Displays the top X users by XP."""
        self.bot.db: aiosqlite.Connection
        async with self.bot.db.execute(
            "SELECT * FROM leveling ORDER BY xp DESC LIMIT ?", (amount,)
        ) as cursor:
            rows = await cursor.fetchall()
            if not rows:
                await ctx.send("No users have leveled up yet!")
                return
            await ctx.send(
                embed=discord.Embed(
                    title="Top Leveling",
                    description="\n".join(
                        f"{self.prefix(i + 1)}. {r['user_id']} - Level {r['level']} - {r['xp']} XP"
                        for i, r in enumerate(rows)
                    ),
                )
            )
