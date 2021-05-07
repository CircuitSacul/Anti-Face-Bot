import os

from discord.ext import commands


class FaceBot(commands.Bot):
    def __init__(self):
        super().__init__("f!")

    async def on_command_error(self, ctx: commands.Context, exc: Exception):
        await ctx.send(exc)

    async def on_ready(self):
        print(
            f"Logged in as {self.user} in {len(self.guilds)} guilds."
        )

    async def start(self, *args, **kwargs):
        for root, _, files in os.walk("app/cogs"):
            for f in files:
                if not f.endswith(".py"):
                    continue
                f = f.replace(".py", "").replace("/", ".")
                self.load_extension(os.path.join(root, f).replace("/", "."))
        return await super().start(*args, **kwargs)
