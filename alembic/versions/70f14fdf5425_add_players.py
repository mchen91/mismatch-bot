"""add players

Revision ID: 70f14fdf5425
Revises: d47b9f23284c
Create Date: 2021-02-13 22:38:23.178118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70f14fdf5425'
down_revision = 'd47b9f23284c'
branch_labels = None
depends_on = None


def upgrade():
    from models import Player

    op.bulk_insert(
        Player.__table__,
        [
            {
                "name": name,
            }
            for name in [
                "Samplay",
                "sockdude1",
                "Jerry3333",
                "jenkem66",
                "Bobby",
                "pokefantom",
                "megaqwertification",
                "djwang88",
                "hotdogturtle",
                "Savestate",
                "LinksDarkArrows",
                "Hawk",
                "Judge9",
                "1221",
                "samthedigital",
                "mimorox",
                "mudi",
                "muny",
                "Zampa",
                "Ravenyte",
                "moOonstermunch",
                "AMGTurtle",
                "Mario 64 Master",
                "aMSa",
                "chaos6",
                "demon9",
                "Freezard",
                "airr8897",
                "marth1",
                "U3TY",
                "Hanky Panky",
                "Dr.M",
            ]
        ]
    )


def downgrade():
    pass
