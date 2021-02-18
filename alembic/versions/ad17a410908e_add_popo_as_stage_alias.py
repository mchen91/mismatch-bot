"""add popo as stage alias

Revision ID: ad17a410908e
Revises: 1a0c13c52442
Create Date: 2021-02-17 21:37:18.852227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ad17a410908e"
down_revision = "1a0c13c52442"
branch_labels = None
depends_on = None


def upgrade():
    from use_cases.aliases import add_char_stage_alias

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)

    add_char_stage_alias(
        session=session, aliased_name="Popo", known_name="Ice Climbers", stage_only=True
    )


def downgrade():
    pass
