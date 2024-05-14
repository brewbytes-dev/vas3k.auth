"""Put False to requests

Revision ID: 90b4fce7b615
Revises: 79092a5bfdc6
Create Date: 2024-05-13 13:17:27.639507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90b4fce7b615'
down_revision = '79092a5bfdc6'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE chats SET follow_up_requests = FALSE")
    pass


def downgrade():
    pass
