"""add stages

Revision ID: d47b9f23284c
Revises: f1a4c52f2563
Create Date: 2021-02-13 22:33:33.061314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd47b9f23284c'
down_revision = 'f1a4c52f2563'
branch_labels = None
depends_on = None


def upgrade():
    from models import Stage

    op.bulk_insert(
        Stage.__table__,
        [
            {
                "position": position,
                "name": name,
            }
            for position, name in enumerate(
                [
                    "Dr. Mario",
                    "Mario",
                    "Luigi",
                    "Bowser",
                    "Peach",
                    "Yoshi",
                    "Donkey Kong",
                    "Captain Falcon",
                    "Ganondorf",
                    "Falco",
                    "Fox",
                    "Ness",
                    "Ice Climbers",
                    "Kirby",
                    "Samus",
                    "Zelda",
                    "Link",
                    "Young Link",
                    "Pichu",
                    "Pikachu",
                    "Jigglypuff",
                    "Mewtwo",
                    "Mr. Game & Watch",
                    "Marth",
                    "Roy",
                ]
            )
        ],
    )


def downgrade():
    pass
