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

        if message.author.bot:
            return
        
        author_perms = message.author.permissions_in(message.channel)

        if author_perms.kick_members or author_perms.ban_members:
            return
        
        for url in message_urls:
            invite = await bot.get_invite(url)
            if invite.guild.id == message.guild.id:
                    return

            await message.delete()
            # Give the offender a warning first. If they're a repeat offender, then ban them.
            if message.author.id in repeat_offenders:
                response = (f"{message.author.mention}, I told you not to test me. SEE YA LATER,~~SHEUSHEUSHEU~~")
                await message.channel.send(response)
                repeat_offenders.remove(message.author.id)
                await message.channel.guild.kick(message.author)
            else:
                response = (f"{message.author.mention}, don't post invite links you IDIOTA!.")
                await message.channel.send(response)
                repeat_offenders.append(message.author.id)
            break
