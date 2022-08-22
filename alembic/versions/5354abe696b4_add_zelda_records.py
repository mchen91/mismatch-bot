"""add zelda records

Revision ID: 5354abe696b4
Revises: 554365813a89
Create Date: 2021-02-16 00:39:00.228884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5354abe696b4"
down_revision = "554365813a89"
branch_labels = None
depends_on = None


def upgrade():
    from models import Stage
    from use_cases.character import guess_character_by_name
    from use_cases.player import get_player_by_name
    from use_cases.records import add_record

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)

    zelda_frames_raw = "1117	876	293	642	753	718	690	852	320	537	909	1194	1163	801	928	513	527	0	737	824	969	485	265	804	475"
    zelda_videos_raw = "https://www.youtube.com/watch?v=DDf5D_zjHP0	https://www.youtube.com/watch?v=-mRpfWGZLUs	https://www.youtube.com/watch?v=OmEsiFzfryg	https://www.youtube.com/watch?v=3v4ubb36oZc	https://www.youtube.com/watch?v=-4dD_2burUs	https://www.youtube.com/watch?v=WPGAEB_n9nA	https://www.youtube.com/watch?v=j-PspMLrdQ4	https://www.youtube.com/watch?v=t5oOF4j3fro	https://www.youtube.com/watch?v=lzhHxZVS4eo	https://www.youtube.com/watch?v=ciI7vPRWlZE	https://www.youtube.com/watch?v=sG8wlXZmwOE	https://www.youtube.com/watch?v=yIQto9LzB10	https://www.youtube.com/watch?v=EHUj-UHsXPM	https://www.youtube.com/watch?v=8DSzjYtwGQA	https://www.youtube.com/watch?v=CzEDuC7RfP4	https://www.youtube.com/watch?v=xydkaVW6Fjw	https://www.youtube.com/watch?v=8VPscCJY0hU	N/A	https://www.youtube.com/watch?v=0mVy88vlxRg	https://www.youtube.com/watch?v=mCQsrv-7iCE	https://www.youtube.com/watch?v=2vljcuawHwo	https://www.youtube.com/watch?v=Vtri4v_xydk	https://www.youtube.com/watch?v=NhyWcBUJcgE	https://www.youtube.com/watch?v=8-4Jw_Rv0Cs	https://www.youtube.com/watch?v=uvZBHK5Ldxo"
    zelda_players_raw = "1221	megaqwertification	Samplay	sockdude1	Judge9	sockdude1	megaqwertification	jenkem66	sockdude1	megaqwertification	muny	muny	megaqwertification	megaqwertification	muny	Samplay	sockdude1	0 targets	megaqwertification	megaqwertification	sockdude1	megaqwertification	jenkem66	megaqwertification	jenkem66"

    zelda_frames = zelda_frames_raw.split("\t")
    zelda_videos = zelda_videos_raw.split("\t")
    zelda_players = zelda_players_raw.split("\t")
    character = guess_character_by_name(session=session, name="Zelda")
    for (stage_index, (frame_string, video_link, player_string)) in enumerate(
        zip(zelda_frames, zelda_videos, zelda_players)
    ):
        stage = session.query(Stage).filter(Stage.position == stage_index).one()
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
            stage=stage,
            player=player,
            time=time,
            partial_targets=partial_targets,
            video_link=video_link,
        )


def downgrade():
    pass
