"""populate char/stage aliases

Revision ID: fd1887d63362
Revises: c9264a2bbb80
Create Date: 2021-02-15 12:12:51.804655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fd1887d63362"
down_revision = "c9264a2bbb80"
branch_labels = None
depends_on = None


def upgrade():
    from itertools import chain

    from models import Character, Stage
    from use_cases.aliases import add_char_stage_alias

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)
    for obj in chain(session.query(Character).all(), session.query(Stage).all()):
        try:
            add_char_stage_alias(
                session=session, aliased_name=obj.name, known_name=obj.name
            )
        except ValueError:
            continue
    session.close()


def downgrade():
    pass
