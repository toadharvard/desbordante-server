"""add task

Revision ID: 7dc9a3441d07
Revises: 6a59d47fe978
Create Date: 2024-04-02 04:04:09.759025

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7dc9a3441d07"
down_revision: Union[str, None] = "6a59d47fe978"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "task",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("FAILED", "CREATED", "RUNNING", "COMPLETED", name="taskstatus"),
            nullable=False,
        ),
        sa.Column("config", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("result", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("dataset_id", sa.Uuid(), nullable=False),
        sa.Column("raised_exception_name", sa.String(), nullable=True),
        sa.Column(
            "failure_reason",
            sa.Enum(
                "MEMORY_LIMIT_EXCEEDED",
                "TIME_LIMIT_EXCEEDED",
                "WORKER_KILLED_BY_SIGNAL",
                "OTHER",
                name="taskfailurereason",
            ),
            nullable=True,
        ),
        sa.Column("traceback", sa.String(), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


# ADJUSTED! See: https://github.com/sqlalchemy/alembic/issues/278#issuecomment-907283386
def downgrade() -> None:
    op.drop_table("task")

    taskfailurereason = sa.Enum(name="taskfailurereason")
    taskfailurereason.drop(op.get_bind(), checkfirst=True)

    taskstatus = sa.Enum(name="taskstatus")
    taskstatus.drop(op.get_bind(), checkfirst=True)
