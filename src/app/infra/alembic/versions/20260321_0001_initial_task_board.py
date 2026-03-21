"""initial task board schema

Revision ID: 20260321_0001
Revises:
Create Date: 2026-03-21 22:55:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260321_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    op.create_table(
        "mentor_intern_links",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("mentor_id", sa.UUID(), nullable=False),
        sa.Column("intern_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("intern_id", name="uq_intern_single_mentor"),
    )
    op.create_table(
        "task_statuses",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_system", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_by", sa.UUID(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=sa.text("''")),
        sa.Column("mentor_id", sa.UUID(), nullable=False),
        sa.Column("intern_id", sa.UUID(), nullable=False),
        sa.Column("status_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["status_id"], ["task_statuses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task_attachments",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("task_id", sa.UUID(), nullable=False),
        sa.Column("author_id", sa.UUID(), nullable=False),
        sa.Column("file_ref", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("source_type", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task_comments",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("task_id", sa.UUID(), nullable=False),
        sa.Column("author_id", sa.UUID(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task_links",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("task_id", sa.UUID(), nullable=False),
        sa.Column("author_id", sa.UUID(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    statuses = sa.table(
        "task_statuses",
        sa.column("name", sa.String()),
        sa.column("code", sa.String()),
        sa.column("order_index", sa.Integer()),
        sa.column("is_default", sa.Boolean()),
        sa.column("is_system", sa.Boolean()),
        sa.column("created_by", sa.UUID()),
    )
    op.bulk_insert(
        statuses,
        [
            {
                "name": "Рассмотрение",
                "code": "REVIEW",
                "order_index": 10,
                "is_default": True,
                "is_system": True,
                "created_by": None,
            },
            {
                "name": "Выполняется",
                "code": "IN_PROGRESS",
                "order_index": 20,
                "is_default": False,
                "is_system": True,
                "created_by": None,
            },
            {
                "name": "На проверке",
                "code": "ON_CHECK",
                "order_index": 30,
                "is_default": False,
                "is_system": True,
                "created_by": None,
            },
            {
                "name": "Выполнено",
                "code": "DONE",
                "order_index": 40,
                "is_default": False,
                "is_system": True,
                "created_by": None,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("task_links")
    op.drop_table("task_comments")
    op.drop_table("task_attachments")
    op.drop_table("tasks")
    op.drop_table("task_statuses")
    op.drop_table("mentor_intern_links")
