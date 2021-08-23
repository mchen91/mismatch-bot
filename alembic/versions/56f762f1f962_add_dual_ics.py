"""add dual ICs

Revision ID: 56f762f1f962
Revises: ad17a410908e
Create Date: 2021-08-22 21:31:49.792965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "56f762f1f962"
down_revision = "ad17a410908e"
branch_labels = None
depends_on = None


def upgrade():
    from use_cases.character import create_character

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)
    create_character(session=session, name="Ice Climbers", position=26)
    session.close()


def downgrade():
    pass
