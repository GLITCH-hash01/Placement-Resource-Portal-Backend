"""Added department to Notes table

Revision ID: 1a8948364f92
Revises: fe6daba70997
Create Date: 2025-03-24 11:50:50.037264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a8948364f92'
down_revision = 'fe6daba70997'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('academic_notes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('department', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('academic_notes', schema=None) as batch_op:
        batch_op.drop_column('department')

    # ### end Alembic commands ###
