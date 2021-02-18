from discord import Embed

MAX_DESCRIPTION_LENGTH = 2048


def create_embeds(lines):
    embeds = []
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
