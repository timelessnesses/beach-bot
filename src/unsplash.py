import discord
from discord.ext import commands

from .utils import apis


class Unsplash(commands.Cog, name="picture"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @property
    def display_emoji(self):
        return "🏖"

    @commands.hybrid_command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def random_beach_photo(self, ctx: commands.Context):
        """
        Some cool and relaxing beach pictures.
        """
        async with ctx.typing():
            photo = await apis.random_beach_photo()
            await ctx.send(file=discord.File(photo, "beach.jpg"))
