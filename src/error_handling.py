from discord.ext import commands


class ErrorHandling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @property
    def display_emoji(self):
        return "💭"

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"{self.display_emoji} You are on cooldown for {error.retry_after:.2f} seconds."
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"{self.display_emoji} Missing required argument {error.param.name}."
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"{self.display_emoji} Bad argument {error.param.name}.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"{self.display_emoji} You are missing permissions to use this command."
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(
                f"{self.display_emoji} I am missing permissions to use this command."
            )
