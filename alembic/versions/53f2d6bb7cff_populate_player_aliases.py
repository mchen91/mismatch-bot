"""populate player aliases

Revision ID: 53f2d6bb7cff
Revises: fd1887d63362
Create Date: 2021-02-15 13:39:29.732993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "53f2d6bb7cff"
down_revision = "fd1887d63362"
branch_labels = None
depends_on = None


def upgrade():
    from models import Player
    from use_cases.aliases import add_player_alias

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)
    for player in session.query(Player).all():
        try:
            add_player_alias(
                session=session, aliased_name=player.name, known_name=player.name
            )
        except ValueError:
            continue
    session.close()


def downgrade():
    pass
