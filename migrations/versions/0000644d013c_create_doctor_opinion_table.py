"""create doctor opinion table

Revision ID: 0000644d013c
Revises: a67c4184860d
Create Date: 2024-02-05 16:42:45.772207

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0000644d013c"
down_revision: Union[str, None] = "a67c4184860d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "doctor_opinions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "short_opinion",
            sa.String(),
            nullable=False,
            comment="The short text opinion",
        ),
        sa.Column("opinion", sa.String(), nullable=False),
        sa.Column("record_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["record_id"],
            ["records.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("doctor_opinions")
    # ### end Alembic commands ###
