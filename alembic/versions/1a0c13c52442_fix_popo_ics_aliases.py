"""fix popo/ics aliases

Revision ID: 1a0c13c52442
Revises: a6aa0de20c27
Create Date: 2021-02-17 21:21:04.838876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1a0c13c52442"
down_revision = "a6aa0de20c27"
branch_labels = None
depends_on = None


def upgrade():
    from models import CharacterStageAlias
    from use_cases.aliases import add_char_stage_alias

    connection = op.get_bind()
    Session = sa.orm.sessionmaker()
    session = Session(bind=connection)

    session.query(CharacterStageAlias).filter(
        CharacterStageAlias.name.ilike("ics")
    ).delete(synchronize_session=False)
    session.query(CharacterStageAlias).filter(
        CharacterStageAlias.name.ilike("ic")
    ).delete(synchronize_session=False)

    add_char_stage_alias(
        session=session, aliased_name="ic", known_name="Popo", char_only=True
    )
    add_char_stage_alias(
        session=session, aliased_name="ic", known_name="Ice Climbers", stage_only=True
    )
    add_char_stage_alias(
        session=session, aliased_name="ics", known_name="Ice Climbers", stage_only=True
    )


def downgrade():
    pass
