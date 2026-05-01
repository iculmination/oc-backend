"""game_runtime_schema

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-01 16:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=True),
        sa.Column("first_name", sa.String(length=255), nullable=True),
        sa.Column("last_name", sa.String(length=255), nullable=True),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "INACTIVE", "BLOCKED", "DELETED", name="userstatus"),
            nullable=False,
        ),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )

    op.create_table(
        "event",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "rarity",
            sa.Enum(
                "COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", name="eventrarity"
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "ONGOING",
                "PAUSED",
                "FINISHED",
                "CANCELLED",
                "ABORTED",
                name="eventstatus",
            ),
            nullable=False,
        ),
        sa.Column(
            "source",
            sa.Enum(
                "RANDOM", "CALLED", "TRIGGERED", "IMMEDIATE", "DELAYED", name="eventsource"
            ),
            nullable=False,
        ),
        sa.Column("effect", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "game",
        sa.Column("turn", sa.Integer(), nullable=False),
        sa.Column("turn_player_id", sa.UUID(), nullable=True),
        sa.Column("winner_player_id", sa.UUID(), nullable=True),
        sa.Column("state_snapshot", sa.JSON(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "ONGOING",
                "PAUSED",
                "FINISHED",
                "CANCELLED",
                "ABORTED",
                name="gamestatus",
            ),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "player",
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("game_id", sa.UUID(), nullable=False),
        sa.Column("is_bot", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("seat", sa.Integer(), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("HOST", "GUEST", name="playerrole"), nullable=False),
        sa.Column(
            "status",
            sa.Enum("CONNECTED", "DISCONNECTED", "LEFT", name="playerstatus"),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["game.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("game_id", "seat", name="uq_player_game_seat"),
    )

    op.create_foreign_key(
        "fk_game_turn_player_id", "game", "player", ["turn_player_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_game_winner_player_id", "game", "player", ["winner_player_id"], ["id"]
    )

    op.create_table(
        "game_card",
        sa.Column("game_id", sa.UUID(), nullable=False),
        sa.Column("player_id", sa.UUID(), nullable=False),
        sa.Column("card_definition_id", sa.UUID(), nullable=True),
        sa.Column("zone", sa.String(length=32), nullable=False),
        sa.Column("position", sa.Integer(), nullable=True),
        sa.Column("attack_current", sa.Integer(), nullable=False),
        sa.Column("health_current", sa.Integer(), nullable=False),
        sa.Column("max_health_current", sa.Integer(), nullable=False),
        sa.Column("is_alive", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("statuses", sa.JSON(), nullable=False),
        sa.Column("last_action", sa.String(length=255), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["card_definition_id"], ["card.id"]),
        sa.ForeignKeyConstraint(["game_id"], ["game.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["player_id"], ["player.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_game_card_game_player", "game_card", ["game_id", "player_id"], unique=False
    )
    op.create_index("ix_game_card_game_zone", "game_card", ["game_id", "zone"], unique=False)

    op.create_table(
        "game_event",
        sa.Column("game_id", sa.UUID(), nullable=False),
        sa.Column("event_id", sa.UUID(), nullable=False),
        sa.Column("duration_left", sa.Integer(), nullable=False),
        sa.Column("applied_at_round", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "ONGOING",
                "PAUSED",
                "FINISHED",
                "CANCELLED",
                "ABORTED",
                name="eventstatus",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["event.id"]),
        sa.ForeignKeyConstraint(["game_id"], ["game.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_game_event_game_status", "game_event", ["game_id", "status"], unique=False
    )

    op.create_table(
        "game_log",
        sa.Column("game_id", sa.UUID(), nullable=False),
        sa.Column("round_number", sa.Integer(), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("actor_type", sa.String(length=32), nullable=False),
        sa.Column("actor_player_id", sa.UUID(), nullable=True),
        sa.Column("actor_card_id", sa.UUID(), nullable=True),
        sa.Column("action_type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("message", sa.String(length=255), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["actor_card_id"], ["game_card.id"]),
        sa.ForeignKeyConstraint(["actor_player_id"], ["player.id"]),
        sa.ForeignKeyConstraint(["game_id"], ["game.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_game_log_game_round_seq",
        "game_log",
        ["game_id", "round_number", "sequence"],
        unique=False,
    )
    op.create_index("ix_game_log_game_created", "game_log", ["game_id", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_game_log_game_created", table_name="game_log")
    op.drop_index("ix_game_log_game_round_seq", table_name="game_log")
    op.drop_table("game_log")

    op.drop_index("ix_game_event_game_status", table_name="game_event")
    op.drop_table("game_event")

    op.drop_index("ix_game_card_game_zone", table_name="game_card")
    op.drop_index("ix_game_card_game_player", table_name="game_card")
    op.drop_table("game_card")

    op.drop_constraint("fk_game_winner_player_id", "game", type_="foreignkey")
    op.drop_constraint("fk_game_turn_player_id", "game", type_="foreignkey")
    op.drop_table("player")
    op.drop_table("game")
    op.drop_table("event")
    op.drop_table("users")
