"""change genres column to array type

Revision ID: a1b2c3d4e5f6
Revises: 6c11e6a80d2b
Create Date: 2026-09-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '6c11e6a80d2b'
branch_labels = None
depends_on = None


def upgrade():
    # Change genres column from String to ARRAY(String) on Venue
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.String(length=120),
               type_=sa.ARRAY(sa.String()),
               existing_nullable=True)

    # Change genres column from String to ARRAY(String) on Artist
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.String(length=120),
               type_=sa.ARRAY(sa.String()),
               existing_nullable=True)


def downgrade():
    # Revert genres column from ARRAY(String) to String on Artist
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.ARRAY(sa.String()),
               type_=sa.String(length=120),
               existing_nullable=True)

    # Revert genres column from ARRAY(String) to String on Venue
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.alter_column('genres',
               existing_type=sa.ARRAY(sa.String()),
               type_=sa.String(length=120),
               existing_nullable=True)
