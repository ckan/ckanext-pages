"""add_header_and_footer_tables

Revision ID: c5400491351a
Revises: a756dbd73ead
Create Date: 2025-01-25 14:34:15.801131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5400491351a'
down_revision = 'a756dbd73ead'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "header",
        sa.Column("id", sa.UnicodeText, primary_key=True),
        sa.Column("title_en", sa.UnicodeText, nullable=False),
        sa.Column("title_ar", sa.UnicodeText, nullable=False),
        sa.Column("link_en", sa.UnicodeText, nullable=False),
        sa.Column("link_ar", sa.UnicodeText, nullable=False),
        sa.Column("type", sa.UnicodeText, nullable=False),
        sa.Column("parent_id", sa.UnicodeText, sa.ForeignKey("header.id"), nullable=True),  # Recursive foreign key
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("is_visible", sa.Boolean, default=True),
        sa.Column("extras", JSONB, nullable=False, default=dict),
        sa.Column("created", sa.DateTime, default=sa.func.now()),
        sa.Column("modified", sa.DateTime, default=sa.func.now()),
    )

    op.create_table(
        "footer",
        sa.Column("id", sa.UnicodeText, primary_key=True),
        sa.Column("column", sa.Integer, nullable=False),
        sa.Column("title_en", sa.UnicodeText, nullable=False),
        sa.Column("title_ar", sa.UnicodeText, nullable=False),
        sa.Column("link_en", sa.UnicodeText, nullable=True),
        sa.Column("link_ar", sa.UnicodeText, nullable=True),
        sa.Column("target", sa.UnicodeText, nullable=True),
        sa.Column("order", sa.Integer, nullable=False),
        sa.Column("is_visible", sa.Boolean, default=True),
        sa.Column("created", sa.DateTime, default=sa.func.now()),
        sa.Column("modified", sa.DateTime, default=sa.func.now()),
    )


def downgrade():
    op.drop_table("header")
    op.drop_table("footer")


