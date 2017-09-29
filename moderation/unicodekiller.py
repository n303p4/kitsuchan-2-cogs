#!/usr/bin/env python3

"""A simple Discord bot that deletes invite links and bans repeat offenders."""

import re

VALID_UNICODE = [
]

repeat_offenders = []  # This list keeps track of repeat offenders.


def setup(bot):
    """Set up the extension."""

    @bot.listen("on_message")
    async def remove_unicode(message):
        """When people post invite links, deal with them accordingly."""
        for character in message.content:
            code = ord(character)
            print(code)
            if code > 255 and code not in VALID_UNICODE:
                await message.delete()
                # Give the offender a warning first. If they're a repeat offender, then ban them.
                if message.author.id in repeat_offenders:
                    response = (f"{message.author.mention}, you were warned. See you later.")
                    await message.channel.send(response)
                    repeat_offenders.remove(message.author.id)
                    await message.channel.guild.ban(message.author)
                else:
                    response = (f"{message.author.mention}, please do not spampost.")
                    await message.channel.send(response)
                    repeat_offenders.append(message.author.id)
