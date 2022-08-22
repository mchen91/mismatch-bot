"""add master hand

Revision ID: 73eab69e748c
Revises: 40131c373081
Create Date: 2021-08-22 22:17:56.037262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "73eab69e748c"
down_revision = "40131c373081"
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
    create_character(session=session, name="Master Hand", position=30)
    # create aliases
    add_char_stage_alias(
        session=session, aliased_name="mh", known_name="Master Hand", char_only=True
    )
    # add records
    frames_raw = "0	0	1051	0	0	0	0	0	1618	0	0	0	0	0	0	0	0	0	3220	0	0	0	1085	0	0	557"
    videos_raw = "N/A	N/A	https://www.youtube.com/watch?v=YXYdE6SdkCQ	N/A	N/A	N/A	N/A	N/A	https://www.youtube.com/watch?v=eYuuXP7VGi4	N/A	N/A	N/A	N/A	N/A	N/A	N/A	N/A	N/A	https://www.youtube.com/watch?v=Fx0qGk7sssw	N/A	N/A	N/A	https://www.youtube.com/watch?v=KnchGUzcwkY	N/A	N/A	https://www.youtube.com/watch?v=FrHWpusVopA"
    players_raw = "4 targets	6 targets	Samplay	3 targets	6 targets	4 targets	7 targets	7 targets	AMGTurtle	7 targets	4 targets	3 targets	4 targets	4 targets	5 targets	7 targets	7 targets	4 targets	1221	5 targets	3 targets	9 targets	sockdude1	5 targets	6 targets	1221"

    frames = frames_raw.split("\t")
    videos = videos_raw.split("\t")
    players = players_raw.split("\t")
    character = guess_character_by_name(session=session, name="Master Hand")
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
