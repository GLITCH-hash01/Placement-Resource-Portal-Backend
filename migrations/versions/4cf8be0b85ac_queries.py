"""Queries

Revision ID: 4cf8be0b85ac
Revises: 76a5839372cc
Create Date: 2025-03-08 20:09:58.375530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cf8be0b85ac'
down_revision = '76a5839372cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queries', schema=None) as batch_op:
        batch_op.alter_column('stack',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('queries', schema=None) as batch_op:
        batch_op.alter_column('stack',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###
