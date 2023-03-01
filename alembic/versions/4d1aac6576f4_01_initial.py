"""01. Initial

Revision ID: 4d1aac6576f4
Revises: 
Create Date: 2023-03-01 23:28:02.184334
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d1aac6576f4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('chats')


def downgrade():
    pass
