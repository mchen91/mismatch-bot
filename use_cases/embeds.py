from typing import List
from discord import Embed
from discord.ext.commands.context import Context

MAX_DESCRIPTION_LENGTH = 2048


def create_embeds(lines: List[str]):
    embeds: List[Embed] = []
    embed = Embed()
    cur_description_lines = []
    cur_description_length = 0
    for line in lines:
        line_length = len(line) + 1
        if cur_description_length + line_length > MAX_DESCRIPTION_LENGTH:
            embed.description = "\n".join(cur_description_lines)
            embeds.append(embed)
            embed = Embed()
            cur_description_lines = []
            cur_description_length = 0
        cur_description_lines.append(line)
        cur_description_length += line_length
    embed.description = "\n".join(cur_description_lines)
    embeds.append(embed)
    return embeds


async def send_embeds(description_lines: List[str], ctx: Context):
    embeds = create_embeds(description_lines)
    for embed in embeds:
        await ctx.send(embed=embed)
