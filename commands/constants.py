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

STADIUM_GUILD_ID = 132025591770644480
PERSONAL_SERVER_GUILD_ID = 691372285080109086
GUILD_IDS = [PERSONAL_SERVER_GUILD_ID]
if os.environ.get("IS_PROD"):
    GUILD_IDS.append(STADIUM_GUILD_ID)
