"""add dual ICs records

Revision ID: 862064aea98d
Revises: 56f762f1f962
Create Date: 2021-08-22 21:34:45.067534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "862064aea98d"
down_revision = "56f762f1f962"
branch_labels = None
depends_on = None


def upgrade():
    from models import Stage
    from use_cases.character import get_character_by_name
    from use_cases.player import get_player_by_name
    from use_cases.records import add_record

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)

    ics_frames_raw = "1012	568	179	587	635	580	478	539	225	524	593	810	594	609	561	413	444	892	472	701	0	278	158	512	336	32"
    ics_videos_raw = "https://www.youtube.com/watch?v=x6H089r-C2I	https://youtu.be/c2ASqgzhPKw?t=26	https://www.youtube.com/watch?v=XkZdgl8hsQc	https://youtu.be/c2ASqgzhPKw?t=45	https://www.youtube.com/watch?v=E6FXcC-O_HA	https://www.youtube.com/watch?v=ukr09aL_RfA	https://www.youtube.com/watch?v=hmJ_vNiq6uY	https://www.youtube.com/watch?v=mCaBAcKhOoU	https://www.youtube.com/watch?v=nlLKFQQ4ujQ	https://www.youtube.com/watch?v=hIA7OYeAn4E	https://www.youtube.com/watch?v=--HoZ4Fuaxo	https://www.youtube.com/watch?v=f_SU50XZV7Y	https://www.youtube.com/watch?v=5J3Ugcb-QLg	https://www.youtube.com/watch?v=5_OvRctC7GE	https://www.youtube.com/watch?v=e0NQnDQplR0	https://www.youtube.com/watch?v=SiQrh3UcANI	https://www.youtube.com/watch?v=2wHReMJRTIY	https://youtu.be/c2ASqgzhPKw?t=214	https://www.youtube.com/watch?v=HUR0UUmtuYU	https://www.youtube.com/watch?v=fNXGJ6RsSUY	N/A	https://www.youtube.com/watch?v=0q9KAfYP2iE	https://www.youtube.com/watch?v=zJW9mSWVFP4	https://www.youtube.com/watch?v=QioY9Nn2XMM	https://www.youtube.com/watch?v=hFt1obby8os	https://www.youtube.com/watch?v=N1Bf9TyZs5Y"
    ics_players_raw = "Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	Samplay	9 targets	Samplay	Samplay	Samplay	Samplay	hotdogturtle"

    ics_frames = ics_frames_raw.split("\t")
    ics_videos = ics_videos_raw.split("\t")
    ics_players = ics_players_raw.split("\t")
    character = get_character_by_name(session=session, name="Ice Climbers")
    for (stage_index, (frame_string, video_link, player_string)) in enumerate(
        zip(ics_frames, ics_videos, ics_players)
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
