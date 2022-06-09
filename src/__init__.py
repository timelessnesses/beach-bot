from discord.ext import commands

from . import error_handling, event_handling, help, leaderboard, stuff, unsplash


async def setup(bot: commands.Bot):
    await bot.load_extension("jishaku")
    await bot.add_cog(stuff.Stuff(bot))
    await bot.add_cog(unsplash.Unsplash(bot))
    await bot.add_cog(leaderboard.Leaderboard(bot))
    await bot.add_cog(help.Help(bot))
    await bot.add_cog(error_handling.ErrorHandling(bot))
    await bot.add_cog(event_handling.EventHandling(bot))
