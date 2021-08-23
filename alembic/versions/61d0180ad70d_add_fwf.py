"""add fwf

Revision ID: 61d0180ad70d
Revises: 26593eccc0a7
Create Date: 2021-08-22 22:07:38.203705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "61d0180ad70d"
down_revision = "26593eccc0a7"
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
    create_character(session=session, name="F. Wireframe", position=28)
    # create aliases
    add_char_stage_alias(
        session=session, aliased_name="fwf", known_name="F. Wireframe", char_only=True
    )
    add_char_stage_alias(
        session=session,
        aliased_name="female wireframe",
        known_name="F. Wireframe",
        char_only=True,
    )
    # add records
    frames_raw = "970	773	238	577	742	712	554	659	234	570	742	905	755	778	680	540	451	0	529	748	0	419	189	729	403	136"
    videos_raw = "https://www.youtube.com/watch?v=lBQ3Nc7V4_Y	https://www.youtube.com/watch?v=D2GOwGVLYKA	https://www.youtube.com/watch?v=nxnue4YYUGs	https://www.youtube.com/watch?v=XM9ok38sVrk	https://www.youtube.com/watch?v=PRgCJvSD0Q8	https://www.youtube.com/watch?v=gBRPwHFkeGY	https://www.youtube.com/watch?v=sLmlTKh4k7Q	https://www.youtube.com/watch?v=e1whT31dF18	https://www.youtube.com/watch?v=awtJOcomV4E	https://www.youtube.com/watch?v=A4upRoDegHA	https://www.youtube.com/watch?v=lJP8S9B6afk	https://www.youtube.com/watch?v=FcKP7RM-oI4	https://www.youtube.com/watch?v=XntjsxZi-OM	https://www.youtube.com/watch?v=wvPAGMrFgDQ	https://www.youtube.com/watch?v=7crgrxMIbEA	https://www.youtube.com/watch?v=I_ngvU-roA4	https://www.youtube.com/watch?v=ZwqP2cbilOs&	N/A	https://www.youtube.com/watch?v=c3Y8dV7nnsM	https://www.youtube.com/watch?v=zcD6zvGalQY	N/A	https://www.youtube.com/watch?v=MsctCB47Zr8	https://www.youtube.com/watch?v=paw3A6itVI8	https://www.youtube.com/watch?v=pMr8sGzN9RA	https://www.youtube.com/watch?v=psXfQ0KNuwY	https://www.youtube.com/watch?v=-8sRMyGSbTU"
    players_raw = "sockdude1	sockdude1	Samplay	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1	1 target	sockdude1	sockdude1	8 targets	sockdude1	sockdude1	sockdude1	sockdude1	sockdude1"

    frames = frames_raw.split("\t")
    videos = videos_raw.split("\t")
    players = players_raw.split("\t")
    character = get_character_by_name(session=session, name="F. Wireframe")
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
