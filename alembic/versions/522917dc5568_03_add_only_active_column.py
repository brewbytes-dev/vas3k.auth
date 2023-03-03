"""03. Add only_active column

Revision ID: 522917dc5568
Revises: 526031485840
Create Date: 2023-03-03 21:40:37.147617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '522917dc5568'
down_revision = '526031485840'
branch_labels = None
depends_on = None


def upgrade():
    # Add the new column to the table
    op.add_column('chats', sa.Column('only_active', sa.BOOLEAN(), nullable=True))


def downgrade():
    # Remove the column from the table
    op.drop_column('chats', 'only_active')
