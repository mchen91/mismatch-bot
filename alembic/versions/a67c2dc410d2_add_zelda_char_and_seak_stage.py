"""add zelda (char) and seak (stage)

Revision ID: a67c2dc410d2
Revises: 53f2d6bb7cff
Create Date: 2021-02-15 14:12:32.749478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a67c2dc410d2"
down_revision = "53f2d6bb7cff"
branch_labels = None
depends_on = None


def upgrade():
    from use_cases.aliases import add_char_stage_alias
    from use_cases.character import create_character
    from use_cases.stage import create_stage

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)
    create_stage(session=session, name="Seak", position=25)
    create_character(session=session, name="Zelda", position=25)
    add_char_stage_alias(
        session=session, aliased_name="Sheik", known_name="Zelda", stage_only=True
    )
    session.close()


def downgrade():
    pass
