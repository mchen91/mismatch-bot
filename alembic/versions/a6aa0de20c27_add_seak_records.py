"""add seak records

Revision ID: a6aa0de20c27
Revises: 5354abe696b4
Create Date: 2021-02-16 00:47:16.622183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a6aa0de20c27"
down_revision = "5354abe696b4"
branch_labels = None
depends_on = None


def upgrade():
    from models import Character
    from use_cases.character import guess_character_by_name
    from use_cases.player import get_player_by_name
    from use_cases.records import add_record, get_record
    from use_cases.stage import guess_stage_by_name

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)

    seak_frames_raw = """78
64
94
143
91
95
124
80
140
26
16
138
68
114
69
79
57
78
85
66
140
67
101
99
107
143"""
    seak_videos_raw = """https://www.youtube.com/watch?v=-3inAWjmE5Y
https://www.youtube.com/watch?v=n83NEPde0mw
https://www.youtube.com/watch?v=w2X7e_QZ60U
https://www.youtube.com/watch?v=RrFGIKqy1Yg
https://www.youtube.com/watch?v=Jcng1uJ0gCY
https://www.youtube.com/watch?v=3l7Vlxjss4s
https://www.youtube.com/watch?v=oY9QfyqPcvA
https://www.youtube.com/watch?v=zNGbOXfCoIw
https://www.youtube.com/watch?v=9BnAsYI0O30
https://www.youtube.com/watch?v=fLyYB8pbIlY
https://www.youtube.com/watch?v=Dvh29UZFgGI
https://www.youtube.com/watch?v=FjPbapyDpQE
https://www.youtube.com/watch?v=SAfhfr7nUfY
https://www.youtube.com/watch?v=sIDHZn-vTQ8
https://www.youtube.com/watch?v=lbtI05_WBPg
https://www.youtube.com/watch?v=kYdFclLF3cA
https://www.youtube.com/watch?v=coEEzk1EKJQ
https://www.youtube.com/watch?v=XOxIXN-meLU
https://www.youtube.com/watch?v=kzxqd1jcu-8
https://www.youtube.com/watch?v=SbCe3xKJ3aY
https://www.youtube.com/watch?v=AtAZbe1nUvk
https://www.youtube.com/watch?v=YilO7jKCMA8
https://www.youtube.com/watch?v=nB2EQp_rElU
https://www.youtube.com/watch?v=AwAB3U0Okos
https://www.youtube.com/watch?v=-JA9aEPs12s
https://www.youtube.com/watch?v=5r4TpOIY9AE"""
    seak_players_raw = """jenkem66
jenkem66
Hawk
sockdude1
sockdude1
hotdogturtle
sockdude1
sockdude1
jenkem66
Hawk
2 people
megaqwertification
sockdude1
megaqwertification
jenkem66
hotdogturtle
Savestate
megaqwertification
sockdude1
jenkem66
sockdude1
hotdogturtle
sockdude1
jenkem66
jenkem66
jenkem66"""

    frames = seak_frames_raw.split("\n")
    videos = seak_videos_raw.split("\n")
    players = seak_players_raw.split("\n")
    seak_stage = guess_stage_by_name(session=session, name="Seak")
    for (char_index, (frame_string, video_link, player_string)) in enumerate(
        zip(frames, videos, players)
    ):
        character = (
            session.query(Character).filter(Character.position == char_index).one()
        )
        try:
            player = get_player_by_name(session=session, name=player_string)
        except ValueError:
            player = None
        if "target" in player_string:
            time = None
            partial_targets = int(player_string[0])
        else:
            time = int(frame_string)
            partial_targets = None
        video_link = video_link if video_link != "N/A" else None
        add_record(
            session=session,
            character=character,
            stage=seak_stage,
            player=player,
            time=time,
            partial_targets=partial_targets,
            video_link=video_link,
        )
    fox_seak_record = get_record(
        session=session,
        character=guess_character_by_name(session=session, name="Fox"),
        stage=seak_stage,
    )
    for player_string in ["Zampa", "jenkem66"]:
        player = get_player_by_name(session=session, name=player_string)
        fox_seak_record.players.append(player)
    session.commit()


def downgrade():
    pass
