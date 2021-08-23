"""add gb

Revision ID: 40131c373081
Revises: 61d0180ad70d
Create Date: 2021-08-22 22:11:31.606242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "40131c373081"
down_revision = "61d0180ad70d"
branch_labels = None
depends_on = None


def upgrade():
    from models import Stage
    from use_cases.aliases import add_char_stage_alias
    from use_cases.character import create_character, get_character_by_name
    from use_cases.player import get_player_by_name
    from use_cases.records import add_record

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)
    # create character
    create_character(session=session, name="Giga Bowser", position=29)
    # create aliases
    add_char_stage_alias(
        session=session, aliased_name="gb", known_name="Giga Bowser", char_only=True
    )
    # add records
    frames_raw = "660	495	160	461	461	474	325	404	218	432	491	543	565	510	397	418	349	0	342	475	988	259	107	524	321	107"
    videos_raw = "https://www.youtube.com/watch?v=8M6Hbb9wU40	https://www.youtube.com/watch?v=GCZXqxjzk3s	https://www.youtube.com/watch?v=6miSWkTcXnc	https://youtu.be/CbsJgjLoQuQ	https://www.youtube.com/watch?v=8reop0RKCB0	https://youtu.be/YAPH8Q7dZeo	https://www.youtube.com/watch?v=I87iD_67DVQ	https://youtu.be/wfjuWK-1n3A	https://www.youtube.com/watch?v=30RDH6IUdWs	https://www.youtube.com/watch?v=dDy6pg-o3gY	https://www.youtube.com/watch?v=AsqZyCEfQl4	https://youtu.be/jFvRi8cgoac	https://youtu.be/lEU4mCKii74	https://www.youtube.com/watch?v=4q2iiiqgeQE	https://www.youtube.com/watch?v=F712EzeLwpU	https://youtu.be/BhhZzxWYG1M	https://youtu.be/9ibWwg1cmMM	N/A	https://www.youtube.com/watch?v=Ne89DO3yiVA	https://www.youtube.com/watch?v=KtwI-EpdFos	https://www.youtube.com/watch?v=JApEOK3yE74	https://www.youtube.com/watch?v=XbkxAULsL_g	https://www.youtube.com/watch?v=BV6vBBg7vOM	https://www.youtube.com/watch?v=g27marb211s	https://www.youtube.com/watch?v=lLZuOVO6FXQ	https://youtu.be/pgl6roqPgxg"
    players_raw = "pokefantom	pokefantom	Samplay	pokefantom	pokefantom	pokefantom	pokefantom	pokefantom	pokefantom	pokefantom	pokefantom	pokefantom	pokefantom	pokefantom	pokefantom	pokefantom	pokefantom	1 target	pokefantom	pokefantom	pokefantom	pokefantom	LinksDarkArrows	pokefantom	pokefantom	pokefantom"

    frames = frames_raw.split("\t")
    videos = videos_raw.split("\t")
    players = players_raw.split("\t")
    character = get_character_by_name(session=session, name="Giga Bowser")
    for (stage_index, (frame_string, video_link, player_string)) in enumerate(
        zip(frames, videos, players)
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
    session.close()


def downgrade():
    pass
