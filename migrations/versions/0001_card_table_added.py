"""card_table_added

Revision ID: 0001
Revises:
Create Date: 2026-03-17 18:29:32.108087

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "card",
        sa.Column("max_health", sa.Integer(), nullable=False),
        sa.Column("attack", sa.Integer(), nullable=False),
        sa.Column(
            "ability",
            sa.Enum("ATTACK", "HEAL", "BUFF", "HIDE", name="cardabilities"),
            nullable=False,
        ),
        sa.Column(
            "nature",
            sa.Enum(
                "HUMAN",
                "ANIMAL",
                "CREATURE",
                "PLANT",
                "RESOURCE",
                "ROBOT",
                name="cardnature",
            ),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("card")
