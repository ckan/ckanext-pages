"""Create revisions column

Revision ID: 1725892d1d94
Revises: a756dbd73ead
Create Date: 2024-10-13 12:09:25.372524

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '1725892d1d94'
down_revision = 'a756dbd73ead'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'ckanext_pages',
        sa.Column(
            u'revisions',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True)
    )


def downgrade():
    op.drop_column(u'ckanext_pages', u'revisions')
