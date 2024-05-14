"""replace prkey in other tables

Revision ID: b508c4bb9561
Revises: 5d3779d5f5cf
Create Date: 2024-05-14 10:26:53.488232

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b508c4bb9561'
down_revision = '5d3779d5f5cf'
branch_labels = None
depends_on = None


def upgrade():
    # Check if the sequence exists and create if it does not
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_class WHERE relkind = 'S' AND relname = 'request_texts_id_seq') THEN
                CREATE SEQUENCE request_texts_id_seq;
            END IF;
        END
        $$;
    """)

    # Add the new column 'id', initially allowing NULL to avoid conflicts with existing rows
    op.add_column('request_texts', sa.Column('id', sa.BigInteger(), nullable=True))

    # Manually set the sequence as the default value for the 'id' column
    op.execute("""
        ALTER TABLE request_texts ALTER COLUMN id SET DEFAULT nextval('request_texts_id_seq');
    """)

    # Set the 'id' values where currently NULL
    op.execute("""
        UPDATE request_texts
        SET id = nextval('request_texts_id_seq')
        WHERE id IS NULL;
    """)

    # Set the column to NOT NULL now that it has values
    op.alter_column('request_texts', 'id', nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('request_texts', 'id')
    # ### end Alembic commands ###