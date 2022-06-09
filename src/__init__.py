from discord.ext import commands

from . import config, etc, fact, help, quiz, unsplash


async def setup(bot: commands.Bot):
    await bot.load_extension("jishaku")
    await bot.add_cog(help.Help(bot))
    await bot.add_cog(config.Config(bot))
    await bot.add_cog(etc.Etc(bot))
    await bot.add_cog(unsplash.Unsplash(bot))
    await bot.add_cog(quiz.Quiz(bot))
    await bot.add_cog(fact.Fact(bot))
