"""Rename creation date to modification date in ShortenedURL model

Revision ID: 858d5f1a94c6
Revises: d945035ff4c9
Create Date: 2022-05-03 13:34:55.923957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '858d5f1a94c6'
down_revision = 'd945035ff4c9'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('shortenedURL', 'creation_date', new_column_name='modification_date')


def downgrade():
    op.alter_column('shortenedURL', 'modification_date', new_column_name='creation_date')
