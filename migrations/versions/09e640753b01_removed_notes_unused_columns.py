"""Removed notes unused columns

Revision ID: 09e640753b01
Revises: ad21b8c6b4fe
Create Date: 2025-04-01 01:38:37.159952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09e640753b01'
down_revision = 'ad21b8c6b4fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.drop_column('likes')
        batch_op.drop_column('desc')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('desc', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('likes', sa.INTEGER(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###
