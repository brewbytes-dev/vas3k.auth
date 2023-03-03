"""04. chat_id upgrade to BigInteger

Revision ID: c155354c1ae6
Revises: 522917dc5568
Create Date: 2023-03-03 21:58:06.038197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c155354c1ae6'
down_revision = '522917dc5568'
branch_labels = None
depends_on = None


def upgrade():
    # Alter the data type of the column to a BigInt that can accept "-999041300032"
    op.alter_column('chats', 'chat_id', type_=sa.BigInteger(), postgresql_using='chat_id::bigint', nullable=False)


def downgrade():
    # Alter the data type of the column back to an Integer
    op.alter_column('chats', 'chat_id', type_=sa.Integer(), postgresql_using='chat_id::int', nullable=False)
