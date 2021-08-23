"""add dual ICs character alias

Revision ID: 8692589f3170
Revises: 862064aea98d
Create Date: 2021-08-22 21:40:33.031924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8692589f3170"
down_revision = "862064aea98d"
branch_labels = None
depends_on = None


def upgrade():
    from use_cases.aliases import add_char_stage_alias

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)
    add_char_stage_alias(
        session=session, aliased_name="ics", known_name="Ice Climbers", char_only=True
    )
    session.close()


def downgrade():
    pass
