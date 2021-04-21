import os

from dotenv import load_dotenv

from app.bot import FaceBot

load_dotenv()

bot = FaceBot()


def run():
    bot.run(os.getenv("TOKEN"))
