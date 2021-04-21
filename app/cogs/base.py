import typing

from discord.ext import commands

if typing.TYPE_CHECKING:
    from app.bot import FaceBot


class Base(commands.Cog):
    def __init__(self, bot: "FaceBot"):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"Logged in as {self.bot.user.name} in "
            f"{len(self.bot.guilds)} guilds!"
        )


def setup(bot: "FaceBot"):
    bot.add_cog(Base(bot))
