"""Add header management table

Revision ID: 288e11bde140
Revises: a756dbd73ead
Create Date: 2025-01-31 14:15:44.764842

"""
from alembic import op
import sqlalchemy as sa

import datetime

from ckanext.pages.db import make_uuid


# revision identifiers, used by Alembic.
revision = '288e11bde140'
down_revision = 'a756dbd73ead'
branch_labels = None
depends_on = None


def upgrade():
    """Apply the migration: Create header tables"""

    # Create header_logo table
    op.create_table(
        "header_logo",
        sa.Column("id", sa.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column("logo_en", sa.UnicodeText, nullable=False),
        sa.Column("logo_ar", sa.UnicodeText, nullable=False),
        sa.Column("created", sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column("modified", sa.DateTime, default=datetime.datetime.utcnow),
    )

    # Create header_main_menu table
    op.create_table(
        "header_main_menu",
        sa.Column("id", sa.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column("title_en", sa.UnicodeText, nullable=False),
        sa.Column("title_ar", sa.UnicodeText, nullable=False),
        sa.Column("link_en", sa.UnicodeText, nullable=False),
        sa.Column("link_ar", sa.UnicodeText, nullable=False),
        sa.Column("menu_type", sa.UnicodeText, nullable=False),  # Type: link/menu
        sa.Column("parent_id", sa.UnicodeText, sa.ForeignKey("header_main_menu.id")),
        sa.Column("order", sa.Integer, default=0),
        sa.Column("is_visible", sa.Boolean, default=True),
        sa.Column("created", sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column("modified", sa.DateTime, default=datetime.datetime.utcnow),
    )

    # Create header_secondary_menu table
    op.create_table(
        "header_secondary_menu",
        sa.Column("id", sa.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column("title_en", sa.UnicodeText, nullable=False),
        sa.Column("title_ar", sa.UnicodeText, nullable=False),
        sa.Column("link_en", sa.UnicodeText, nullable=False),
        sa.Column("link_ar", sa.UnicodeText, nullable=False),
        sa.Column("order", sa.Integer, default=0),
        sa.Column("is_visible", sa.Boolean, default=True),
        sa.Column("created", sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column("modified", sa.DateTime, default=datetime.datetime.utcnow),
    )

def downgrade():
    """Rollback the migration: Drop header tables"""
    op.drop_table("header_secondary_menu")
    op.drop_table("header_main_menu")
    op.drop_table("header_logo")