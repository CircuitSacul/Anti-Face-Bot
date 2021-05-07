import os
import io
from PIL import Image
import typing

import discord
import face_recognition
from discord.ext import commands

if typing.TYPE_CHECKING:
    from app.bot import FaceBot


class Base(commands.Cog):
    def __init__(self, bot: "FaceBot"):
        self.bot = bot

        _, _, face_paths = next(os.walk("app/bad_faces/"))
        face_paths = ["app/bad_faces/" + path for path in face_paths]
        bad_faces = []
        for path in face_paths:
            bad_faces.append(face_recognition.load_image_file(path))

        self.encodings = []
        for face in bad_faces:
            self.encodings.append(face_recognition.face_encodings(face, num_jitters=10, model="large")[0])

    async def does_match_any(self, attachment: discord.Attachment):
        as_image = face_recognition.load_image_file(io.BytesIO(await attachment.read()))
        _encodings = face_recognition.face_encodings(as_image, num_jitters=10)
        if not _encodings:
            return []

        encoding = _encodings[0]
        matches = []
        matches.extend(face_recognition.compare_faces(self.encodings, encoding))
        return matches

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.attachments:
            return
        for attachment in message.attachments:
            if any(await self.does_match_any(attachment)):
                await message.delete()
                await message.channel.send(
                    f"A message by {message.author} was deleted for containing a forbidden face."
                )
                break


def setup(bot: "FaceBot"):
    bot.add_cog(Base(bot))
