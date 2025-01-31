"""Add ckanext-pages table

Revision ID: a756dbd73ead
Revises:
Create Date: 2024-07-11 16:22:41.698582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a756dbd73ead"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    engine = op.get_bind()
    inspector = sa.inspect(engine)
    tables = inspector.get_table_names()
    if "ckanext_pages" not in tables:
        op.create_table(
            "ckanext_pages",
            sa.Column("id", sa.UnicodeText, primary_key=True),
            sa.Column("title", sa.UnicodeText, default=""),
            sa.Column("name", sa.UnicodeText, default=""),
            sa.Column("content", sa.UnicodeText, default=""),
            sa.Column("lang", sa.UnicodeText, default=""),
            sa.Column("order", sa.UnicodeText, default=""),
            sa.Column("private", sa.Boolean, default=True),
            sa.Column("group_id", sa.UnicodeText, default=None),
            sa.Column("user_id", sa.UnicodeText, default=""),
            sa.Column("publish_date", sa.DateTime),
            sa.Column("page_type", sa.UnicodeText),
            sa.Column("created", sa.DateTime),
            sa.Column("modified", sa.DateTime),
            sa.Column("extras", sa.UnicodeText, default="{}"),
        )


def downgrade():
    op.drop_table("ckanext_pages")
