import os

COMMAND_PREFIX = "-mm "

CHARACTERS = [
    "Dr. Mario",
    "Mario",
    "Luigi",
    "Bowser",
    "Peach",
    "Yoshi",
    "DK",
    "Falcon",
    "Ganondorf",
    "Falco",
    "Fox",
    "Ness",
    "Popo",
    "Kirby",
    "Samus",
    "Sheik",
    "Link",
    "Young Link",
    "Pichu",
    "Pikachu",
    "Jigglypuff",
    "Mewtwo",
    "Mr. G&W",
    "Marth",
    "Roy",
    "Zelda",
    "Ice Climbers",
    "M. Wireframe",
    "F. Wireframe",
    "Giga Bowser",
    "Master Hand",
    "Crazy Hand",
]

STAGES = [
    "Dr. Mario",
    "Mario",
    "Luigi",
    "Bowser",
    "Peach",
    "Yoshi",
    "DK",
    "Falcon",
    "Ganondorf",
    "Falco",
    "Fox",
    "Ness",
    "Ice Climbers",
    "Kirby",
    "Samus",
    "Sheik",
    "Link",
    "Young Link",
    "Pichu",
    "Pikachu",
    "Jigglypuff",
    "Mewtwo",
    "Mr. G&W",
    "Marth",
    "Roy",
    "Seak",
]

stadium_guild_id = 132025591770644480
personal_server_guild_id = 691372285080109086
GUILD_IDS = [personal_server_guild_id]
if os.environ.get("IS_PROD"):
    GUILD_IDS.append(stadium_guild_id)
