"""add mwf

Revision ID: 26593eccc0a7
Revises: 8692589f3170
Create Date: 2021-08-22 21:59:37.976016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "26593eccc0a7"
down_revision = "8692589f3170"
branch_labels = None
depends_on = None


def upgrade():
    from models import Stage
    from use_cases.aliases import add_char_stage_alias
    from use_cases.character import create_character, guess_character_by_name
    from use_cases.player import get_player_by_name
    from use_cases.records import add_record

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)
    # create character
    create_character(session=session, name="M. Wireframe", position=27)
    # create aliases
    add_char_stage_alias(
        session=session, aliased_name="mwf", known_name="M. Wireframe", char_only=True
    )
    add_char_stage_alias(
        session=session,
        aliased_name="male wireframe",
        known_name="M. Wireframe",
        char_only=True,
    )
    # add records
    frames_raw = "926	836	226	700	681	711	567	595	230	598	713	887	796	718	557	474	408	0	473	807	0	431	184	683	430	128"
    videos_raw = "https://www.youtube.com/watch?v=_j94tC0Xm6I	https://www.youtube.com/watch?v=naMahMwMq2s	https://www.youtube.com/watch?v=tJB-QiVY6ZU	https://www.youtube.com/watch?v=ie-F6rUyWsI	https://www.youtube.com/watch?v=pIOlUmkmOAQ	https://www.youtube.com/watch?v=cefXy9ajr0Y	https://www.youtube.com/watch?v=3x7hNBESp1o	https://www.youtube.com/watch?v=zXNRnp1CYGA	https://www.youtube.com/watch?v=ouf6CbAe8zE	https://www.youtube.com/watch?v=-lfsgQMiU6U	https://www.youtube.com/watch?v=bcT6S4syg-E	https://www.youtube.com/watch?v=I1VnWUIrkXc	https://www.youtube.com/watch?v=Vt5U7ILj5Mk	https://www.youtube.com/watch?v=MCld-hCtdbc	https://www.youtube.com/watch?v=VyhPOju74cs	https://www.youtube.com/watch?v=JMFi4PAAq6s	https://www.youtube.com/watch?v=pqbiagw8g2Q	N/A	https://www.youtube.com/watch?v=Afwja0N5M-g	https://www.youtube.com/watch?v=1DHNPOwxK7k	N/A	https://www.youtube.com/watch?v=r9Z--uW-vZw	https://www.youtube.com/watch?v=AjluN4NODao	https://www.youtube.com/watch?v=dsXCL5fdh8c	https://www.youtube.com/watch?v=QI0HBBO5zZk	https://www.youtube.com/watch?v=LcLk_hcTYVg"
    players_raw = "hotdogturtle	hotdogturtle	Samplay	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	1 target	hotdogturtle	hotdogturtle	9 targets	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle	hotdogturtle"

    frames = frames_raw.split("\t")
    videos = videos_raw.split("\t")
    players = players_raw.split("\t")
    character = guess_character_by_name(session=session, name="M. Wireframe")
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
