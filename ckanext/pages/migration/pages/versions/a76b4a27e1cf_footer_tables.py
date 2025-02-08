"""footer_tables

Revision ID: a76b4a27e1cf
Revises: 288e11bde140
Create Date: 2025-02-04 17:48:00.619394

"""
from alembic import op
import sqlalchemy as sa
from ckanext.pages.db import make_uuid
import datetime


# revision identifiers, used by Alembic.
revision = 'a76b4a27e1cf'
down_revision = '288e11bde140'
branch_labels = None
depends_on = None


def upgrade():

        # Create header_logo table
    op.create_table(
        "cms_footer_main",
        sa.Column("id", sa.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column("logo_en", sa.UnicodeText, nullable=True, default=''),
        sa.Column("logo_ar", sa.UnicodeText, nullable=True, default=''),
        sa.Column("phone_number", sa.UnicodeText, nullable=True, default=''),
        sa.Column("modified", sa.DateTime, default=datetime.datetime.utcnow),
    )

    op.create_table(
        "cms_footer_column_titles",
        sa.Column("id", sa.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column("column2_en", sa.UnicodeText, nullable=True, default=''),
        sa.Column("column2_ar", sa.UnicodeText, nullable=True, default=''),
        sa.Column("column3_en", sa.UnicodeText, nullable=True, default=''),
        sa.Column("column3_ar", sa.UnicodeText, nullable=True, default=''),
        sa.Column("modified", sa.DateTime, default=datetime.datetime.utcnow),
    )

    op.create_table(
        "cms_footer_column_links",
        sa.Column("id", sa.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column("title_en", sa.UnicodeText, nullable=False, default=''),
        sa.Column("title_ar", sa.UnicodeText, nullable=False, default=''),
        sa.Column("link_en", sa.UnicodeText, nullable=False, default=''),
        sa.Column("link_ar", sa.UnicodeText, nullable=False, default=''),
        sa.Column("target", sa.Integer, nullable=False, default=0),
        sa.Column("order", sa.UnicodeText, nullable=False, default=''),
        sa.Column("column_number", sa.Integer, nullable=False, default=2),
        sa.Column("modified", sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column("created", sa.DateTime, default=datetime.datetime.utcnow),
    )

    op.create_table(
        "cms_footer_social_media",
        sa.Column("id", sa.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column("title_en", sa.UnicodeText, nullable=False, default=''),
        sa.Column("title_ar", sa.UnicodeText, nullable=False, default=''),
        sa.Column("link_en", sa.UnicodeText, nullable=False, default=''),
        sa.Column("link_ar", sa.UnicodeText, nullable=False, default=''),
        sa.Column("image_url", sa.UnicodeText, nullable=False, default=''),
        sa.Column("order", sa.UnicodeText, nullable=False, default=''),
        sa.Column("modified", sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column("created", sa.DateTime, default=datetime.datetime.utcnow),
    )


    op.create_table(
        "cms_footer_banner",
        sa.Column("id", sa.UnicodeText, primary_key=True, default=make_uuid),
        sa.Column("title_en", sa.UnicodeText, nullable=False, default=''),
        sa.Column("title_ar", sa.UnicodeText, nullable=False, default=''),
        sa.Column("link_en", sa.UnicodeText, nullable=False, default=''),
        sa.Column("link_ar", sa.UnicodeText, nullable=False, default=''),
        sa.Column("image_url", sa.UnicodeText, nullable=False, default=''),
        sa.Column("order", sa.UnicodeText, nullable=False, default=''),
        sa.Column("modified", sa.DateTime, default=datetime.datetime.utcnow),
        sa.Column("created", sa.DateTime, default=datetime.datetime.utcnow),
    )

def downgrade():
    op.drop_table("cms_footer_main")
    op.drop_table("cms_column_titles")
    op.drop_table("cms_footer_column_links")
    op.drop_table("cms_footer_social_media")
    op.drop_table("cms_footer_banner")

