#!/usr/bin/env python3

"""A simple cog that deletes invite links and bans repeat offenders."""

import re

REGEX_URL = r"discord\S*\..*/\S*"

repeat_offenders = []  # This list keeps track of repeat offenders.


def setup(bot):
    """Set up the extension."""

    @bot.listen("on_message")
    async def remove_invites(message):
        """When people post invite links, deal with them accordingly."""
        message_urls = re.findall(REGEX_URL, message.content)
        for url in message_urls:
            if await bot.get_invite(url):
                await message.delete()
                # Give the offender a warning first. If they're a repeat offender, then ban them.
                if message.author.id in repeat_offenders:
                    response = (f"{message.author.mention}, you were warned. See you later.")
                    await message.channel.send(response)
                    repeat_offenders.remove(message.author.id)
                    await message.channel.guild.ban(message.author, reason="Invite links")
                else:
                    response = (f"{message.author.mention}, please do not post invite links.")
                    await message.channel.send(response)
                    repeat_offenders.append(message.author.id)
                break
