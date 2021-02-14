"""add characters

Revision ID: 857aad2f6c01
Revises: d237f5738423
Create Date: 2021-02-13 20:16:29.457057

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "857aad2f6c01"
down_revision = "d237f5738423"
branch_labels = None
depends_on = None


def upgrade():
    from models import Character

    op.bulk_insert(
        Character.__table__,
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
                    "Popo",
                    "Kirby",
                    "Samus",
                    "Sheik",
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
