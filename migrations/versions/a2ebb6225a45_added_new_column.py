"""Added new column

Revision ID: a2ebb6225a45
Revises: ef577b77fdb0
Create Date: 2025-03-31 10:51:45.905537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2ebb6225a45'
down_revision = 'ef577b77fdb0'
branch_labels = None
depends_on = None


def upgrade():
    # Create the 'event_categories' enum type
    event_categories = sa.Enum('event', 'internship', name='event_categories')
    event_categories.create(op.get_bind(), checkfirst=True)

    # Add the 'category' column to the 'events' table
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', event_categories, nullable=False, server_default='event'))

    # Set default value for existing rows
    op.execute("UPDATE events SET category = 'event' WHERE category IS NULL")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###
